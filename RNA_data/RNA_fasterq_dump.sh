#!/bin/bash

#SBATCH -J DataDownload
#SBATCH -o Log.%j.out 
#SBATCH --nodelist=node03
#SBATCH -n 12

# Specify the range of SRA accession numbers
start_index=13085374
end_index=13085577

# Path to the SRA Toolkit's fastq-dump tool
fasterq_dump_tool=/Bioinformatics/00.Tools/sratoolkit.3.0.2-ubuntu64/bin/fasterq-dump

# Loop through the range of indices and download/convert to FASTQ
for ((i = start_index; i <= end_index; i++)); do
    accession=SRR$(printf "%08d" $i)
    mkdir $accession
		cd $accession
    echo "Downloading and converting $accession to FASTQ..."
    $fasterq_dump_tool --outdir ./ --split-files $accession
		cd ..
done

# There were additional numbers that were not continuous with the previous index
start_index=13086101
end_index=13086103

for ((i = start_index; i <= end_index; i++)); do
    accession=SRR$(printf "%08d" $i)
    mkdir $accession
    cd $accession
    echo "Downloading and converting $accession to FASTQ..."
    $fasterq_dump_tool --outdir ./ --split-files $accession
    echo "Downloading $accession complete!"
    cd ..
done

echo "Download and conversion to FASTQ complete!"
