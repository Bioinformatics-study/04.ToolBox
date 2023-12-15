#!/usr/bin/python3

import pandas as pd
import argparse
import sys
import os
#-------------------------------------------------------#
parser = argparse.ArgumentParser(description='Code Usage')
parser.add_argument('1', metavar='<xlsx>', help='set xlsx file')
args = parser.parse_args()
#-------------------------------------------------------#
SRA = pd.read_excel(sys.argv[1],
                    header=0)
SRA = SRA.ffill()
#-------------------------------------------------------#
SRA_WGBS = SRA[SRA['Assay type'] == 'Bisulfite-Seq']
#-------------------------------------------------------#
SRA_WGBS = SRA_WGBS.groupby('ID')['acc'].agg(lambda x: list(x)).to_dict()
#-------------------------------------------------------#
for sample in SRA_WGBS.keys():
    Prefix = sample.split(' ')[1]

    if len(SRA_WGBS[sample]) > 1:
        Forward = [ID + '_1.fastq' for ID in SRA_WGBS[sample]]
        Forward = ' '.join(Forward)
        command = f'cat {Forward} >> {Prefix}_1.fastq'
        os.system(command)

        Reverse = [ID+'_1.fastq' for ID in SRA_WGBS[sample]]
        Reverse = ' '.join(Reverse)
        command = f'cat {Reverse} >> {Prefix}_2.fastq'
        os.system(command)
    else:
        Sample = ''.join(SRA_WGBS[sample])

        if os.path.exists(f'{Sample}_1.fastq') and os.path.exists(f'{Sample}_2.fastq'):
            command = f'mv {Sample}_1.fastq {Prefix}_1.fastq'
            os.system(command)

            command = f'mv {Sample}_2.fastq {Prefix}_2.fastq'
            os.system(command)
# -------------------------------------------------------#