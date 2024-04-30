#!/home/yej/anaconda3/envs/yej/bin/python3
import pandas as pd
import os 
import sys
#---------------------------------------------------------------------------------------#
path = os.getcwd()
BATCH = {}
with open(f"{path}/batchconfig.txt", "r") as read : 
  for line in read:
    line = line.strip('\n').strip().split("=")
    key = line[0]
    value = line[1]
    BATCH[key] = value
#---------------------------------------------------------------------------------------#
if BATCH['Run_type'] == 'WGBS':
    Code = '/labmed/00.Code/BI.Study/00.Pipeline/WGBS.py'
elif BATCH['Run_type'] == 'RNA':
    Code = '/labmed/00.Code/BI.Study/00.Pipeline/RNA.py'
#---------------------------------------------------------------------------------------#
Sample = pd.read_csv("SampleSheet.txt", sep='\t', header=None)
total_sample_list = list(Sample.loc[:,0])
total_sample_path_list= list(Sample.loc[:,1])
#---------------------------------------------------------------------------------------#
for n in range(Sample.shape[0]):
    folder_name = str(Sample.loc[n,0]).strip()
    if os.path.isdir(folder_name):
        os.chdir(folder_name)
        with open("Run.sh", "w") as note:
          note.write("#!/bin/bash" + '\n' + 
                     f"#SBATCH -J " + folder_name + "\n" +
                     f"#SBATCH -o Log.%j.out" + '\n' + 
                     f"#SBATCH --time=UNLIMITED" + '\n'
                     f"#SBATCH --nodelist={BATCH['Node']}" +'\n' + 
                     f"#SBATCH -n " + "2" + '\n' +
                     '\n' + 
                     f"python3 {Code}" + '\n')

        with open(f"{folder_name}.batchconfig.txt", "w") as write_batch_config:
          for keys in BATCH.keys():
            write_batch_config.write(f"{keys}={BATCH[keys]}\n")
          write_batch_config.write(f"sample={total_sample_list}\n")
          write_batch_config.write(f"sample_dir={total_sample_path_list}\n")

        os.chdir("..")
#---------------------------------------------------------------------------------------#
with open("Total_run.sh", "w") as note:
    for n in range(Sample.shape[0]):
        folder_name = str(Sample.loc[n,0]).strip()
        note.write(f"cd {path}/{folder_name}; sbatch Run.sh" + '\n')
#---------------------------------------------------------------------------------------#