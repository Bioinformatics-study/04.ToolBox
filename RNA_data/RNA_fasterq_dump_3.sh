#!/bin/bash

#SBATCH -J RNA-fasterq-dump
#SBATCH -o Log.%j.out
#SBATCH --nodelist=node03
#SBATCH -n 12

#Downloading samples that were failed at the previous script
#Check the Log file to get failed SRR ids
fasterq_dump_tool=/Bioinformatics/00.Tools/sratoolkit.3.0.2-ubuntu64/bin/fasterq-dump
accession=("SRR13085450" "SRR13085514")

for accession in ${accession[@]}; do
    mkdir $accession
    cd $accession
    echo "Downloading and converting $accession to FASTQ..."
    $fasterq_dump_tool --outdir ./ --split-files $accession
    echo "Downloading $accession complete!"
    cd ..
done

echo "Download and conversion to FASTQ complete!"
