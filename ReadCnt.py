#!/home/lsy/anaconda3/bin/python

import pandas as pd
import os
import sys
#-----------------------------------------------------------------------------#
BATCH = {}
with open(f'/labmed/01.ALL/02.RNA/batchconfig.txt','r') as batch :
        for info in batch :
                info = info.strip()
                splitted = info.split('=')
                BATCH[splitted[0]] = splitted[1]
#-----------------------------------------------------------------------------#
Sample = pd.read_csv("/labmed/01.ALL/02.RNA/SampleSheet.txt", sep="\t", header=None)
Name = Sample.iloc[:, 0]
os.chdir(f'/labmed/01.ALL/02.RNA/{Name[0]}/03.Align')
with open(f'{Name[0]}_ReadsPerGene.out.tab', 'r') as f:
    lines = [line for line in f if not line.startswith('N')]
    column_list = ['ENSG_ID','Unstranded','Read1','Read2']
    df = pd.DataFrame([line.strip().split('\t') for line in lines], columns=column_list)
    df = df[['ENSG_ID',f'{column_list[int(BATCH["select_a_column"])-1]}']]
    df.columns = ['ENSG_ID', f'{Name[0]}']
    
    for name in Name[1:] :
        os.chdir(f'/labmed/01.ALL/02.RNA/{name}/03.Align')
        with open(f'{name}_ReadsPerGene.out.tab', 'r') as f:
            lines = [line for line in f if not line.startswith('N')]
            column_list = ['ENSG_ID','Unstranded','Read1','Read2']
            df2 = pd.DataFrame([line.strip().split('\t') for line in lines], columns=column_list)
            df2 = df2[['ENSG_ID',f'{column_list[int(BATCH["select_a_column"])-1]}']]
            df2.columns = ['ENSG_ID', f'{name}']
            df = pd.merge(df,df2,on='ENSG_ID',how='outer')
#     df.to_csv('/labmed/01.ALL/02.RNA/Total_ReadCnt.txt',sep='\t', index = False)
#-----------------------------------------------------------------------------#
with open(f'/media/src/{BATCH["Ref_ver"]}/00.RNA/STARidx/geneInfo.tab', 'r') as f:
    lines = [line for line in f if line.startswith('E')]
    column_list = ['ENSG_ID','GeneSymbol','Feature']
    gene_df = pd.DataFrame([line.strip().split('\t') for line in lines], columns=column_list)
    matrix = pd.merge(df,gene_df, on='ENSG_ID', how = 'left')
    columns = ['GeneSymbol'] + Name.tolist()
    matrix = matrix[columns]
    matrix.to_csv('/labmed/01.ALL/02.RNA/Total_ReadCnt.txt',sep='\t', index = False)
