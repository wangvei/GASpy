#!/bin/sh

# Relaxations where we were not able to attach calculators when saving the atoms objects
# to the Primary DB
#for fwid in 24975 25036 25240 26446 27856 34826 38076 38306 38569 41306 48551 48574 50862 50919 53111 53676 54232 54774 54787 55182 55544 56326 56374 56682 56806 56956 57055 57056 57450 57493 57529 57573 57795 57992 58184 58617 58697 58698 58739 58767 58782 58813 58815 58829 59160 59166 60250 60265 60314 60432 60584 60773 60868 62090 62240 62600 62691 62723 62879 63244 63547 63551 63857 64114 64818 65727 66245 66467 66471 66600 66653 66683 66714 66755 66802 67077 67542 67650 68710 68933 69060 69171 69259 69385 69422 70211 70688 71217 72300 72446 75387 80642

# Fingerprinting failed to occur when being dumped to the Aux DB
for fwid in 57526 66985 67863 48535 58730 78824 71140 48802 78826 47798 61494
do
    # Purge the bad firework from the Primary DB
    #lpad -l /global/project/projectdirs/m2755/zu_vaspsurfaces_files/my_launchpad.yaml defuse_fws -i $fwid
    # Call the python script to purge the Aux DB
    python target_purge_fr_aux.py $fwid
done
