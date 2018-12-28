'''
This module houses the functions needed to make and submit FireWorks rockets to
perform calculations of gases.
'''

__authors__ = ['Zachary W. Ulissi', 'Kevin Tran']
__emails__ = ['zulissi@andrew.cmu.edu', 'ktran@andrew.cmu.edu']

import pickle
import luigi
from fireworks import Workflow
from ..atoms_generators import GenerateGas
from ..core import make_task_output_object
from ... import defaults
from ...mongo import make_atoms_from_doc
from ...utils import unfreeze_dict, print_dict
from ...fireworks_helper_scripts import get_launchpad, make_firework

GAS_SETTINGS = defaults.GAS_SETTINGS


class MakeGasFW(luigi.Task):
    '''
    This class accepts a luigi.Task (e.g., relax a structure), then checks to
    see if this task is already logged in the Auxiliary vasp.mongo database. If
    it is not, then it submits the task to our Primary FireWorks database.
    '''
    gas_name = luigi.Parameter()
    vasp_settings = luigi.DictParameter(GAS_SETTINGS['vasp'])

    def requires(self):
        return GenerateGas(gas_name=self.gas_name)

    def run(self, _test=False):
        ''' Do not use `_test=True` unless you are unit testing '''
        # Parse the input atoms object
        with open(self.input().path, 'rb') as file_handle:
            doc = pickle.load(file_handle)
        atoms = make_atoms_from_doc(doc)

        # Create and package the FireWork
        fw_name = {'gasname': self.gas_name,
                   'vasp_settings': unfreeze_dict(self.vasp_settings),
                   'calculation_type': 'gas phase optimization'}
        fwork = make_firework(atoms=atoms,
                              fw_name=fw_name,
                              vasp_settings=unfreeze_dict(self.vasp_settings))
        wflow = Workflow([fwork], name='vasp optimization')

        # Submit the FireWork to our launch pad
        if _test is False:
            lpad = get_launchpad()
            lpad.add_wf(wflow)
        # If we are unit testing, then DO NOT submit the FireWork
        else:
            return wflow

        print('Just submitted the following Fireworks:')
        print_dict(fwork.name, indent=1)

    def output(self):
        return make_task_output_object(self)
