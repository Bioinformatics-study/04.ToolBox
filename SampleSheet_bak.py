#!/home/lsy/anaconda3/envs/NGS/bin/python

import sys
import os
import pandas as pd


LIST = sys.argv[1::2]

with open('SampleSheet.txt', 'w') as note1:
    for sample in LIST:
        if '_R1' in sample:
            Name = sample.split('/')[-1].split('_R1')[0]
            if os.path.isdir(f'{Name}'):
                pass
            else:
                os.mkdir(f'{Name}')
            Size = os.path.getsize(sample) / (1024 ** 2)
            read1 = sample
            read2 = read1.replace('_R1', '_R2')
            note1.write(f'{Name}\t{read1}\t{read2}\t{Size: .2f} MB\n')

            with open(f'{Name}/SampleSheet.txt', 'w') as note2:
                r1 = sample
                r2 = sample.replace('_R1', '_R2')
                note2.write(f'{Name}\t{r1}\t{r2}\t')

        elif '_1' in sample:
            Name = sample.split('/')[-1].split('_1')[0]
            if os.path.isdir(f'{Name}'):
                pass
            else:
                os.mkdir(f'{Name}')
            Size = os.path.getsize(sample) / (1024 ** 2)
            read1 = sample
            read2 = read1.replace('_1', '_2')
            note1.write(f'{Name}\t{read1}\t{read2}\t{Size: .2f} MB\n')

            with open(f'{Name}/SampleSheet.txt', 'w') as note2:
                r1 = sample
                r2 = sample.replace('_1', '_2')
                note2.write(f'{Name}\t{r1}\t{r2}\t')
               
