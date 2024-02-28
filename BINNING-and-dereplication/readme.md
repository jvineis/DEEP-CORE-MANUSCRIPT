# Here are  the steps to reconstruct genomes from each sample and create a dereplicated set of genomes
## 1. Download the data from JGI using Globus and place the data in a directory of your choice.
####  JGI PROJECT: Combining high resolution organic matter characterization and microbial meta-omics to assess the effects of nutrient loading on salt marsh carbon sequestration JGI LINK: https://genome.jgi.doe.gov/portal/Comhiguestration/Comhiguestration.info.html JGI PROJECT ID: 503576

## 2. fix the assemblies so that we are dealing with contig names that makes downstream programs happy and filter contigs that are below 2500 nt.
 #!/bin/bash
 #SBATCH --nodes=1
 #SBATCH --time=01:00:00
 #SBATCH --partition=express
 #SBATCH --array=1-55
 ASSEMBLY=$(sed -n "$SLURM_ARRAY_TASK_ID"p samples.txt)
 
 anvi-script-reformat-fasta ${ASSEMBLY}-final.contigs.fasta --simplify-names -o ${ASSEMBLY}_filter_contigs.fa -l 2500
