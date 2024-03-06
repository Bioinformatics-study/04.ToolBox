#!/home/lab/anaconda3/envs/NGS/bin/python3

import os
import sys
#---------------------------------------------------------------------------------#
PATH = os.getcwd()
Set_node = sys.argv[1]
#---------------------------------------------------------------------------------#
with open('Sample.txt', 'r') as samp:
    for line in samp:
        line = line.strip()
        with open(f'{line}/Run.sh', 'w') as note1:
            note1.write("#!/bin/bash" + '\n' + \
                       "#SBATCH -J WGBS" + '\n' + \
                        "#SBATCH -o Log.%j.out" + '\n' + \
                        f"#SBATCH --nodelist={Set_node}" + '\n' + \
                        "#SBATCH -n 2" + '\n'*2 + \
                        "python3 /labmed/00.Code/BI.Study/00.Pipeline/WGBS.py")
#---------------------------------------------------------------------------------#            
with open('Total_run.sh', 'w') as note2:
    with open('Sample.txt', 'r') as samp:
        for line in samp:
            line = line.strip()
            note2.write(f"cd {PATH}/{line}; sbatch Run.sh" + '\n')
#---------------------------------------------------------------------------------#