# Here are  the steps to reconstruct genomes from each sample and create a dereplicated set of genomes
## 1. Download the data from JGI using Globus and place the data in a directory of your choice. I moved all the data to more accessible locations to make it easier for me to script using sample names.

    #!/bin/bash

    # To move the directories downloaded from JGI to a more easily accessible location
    #for i in `cat x_sample-names.txt`; do mv 60224/53/Comhiguestration/Combining_high_resolution_organic_matter_characterization_and_microbial_meta-omics_to_assess_the_effects_of_nutrient_loading_on_salt_marsh_carbon_sequestration__Salt_Marsh_Sediment_${i}* ${i}; done

    # To move the assemblies to a more easily accessible location
    #for i in `cat x_sample-names.txt`; do mv ${i}/QC_and_Genome_Assembly/Salt_Marsh_Sediment_${i}_MG*/final.contigs.fasta ${i}/final.contigs.fasta; done

    # To move the fastq files to a more easily accessible location
    for i in `cat x_sample-names.txt`; do mv ${i}/Filtered_Raw_Data/*METAGENOME.fastq.gz ${i}/Filtered_Raw_Data/${i}.fastq.gz; done

####  JGI PROJECT: Combining high resolution organic matter characterization and microbial meta-omics to assess the effects of nutrient loading on salt marsh carbon sequestration JGI LINK: https://genome.jgi.doe.gov/portal/Comhiguestration/Comhiguestration.info.html JGI PROJECT ID: 503576


## 2. fix the deflines of each assembly fasta, build a contigs database, and run hmms on the datbase. The samples.txt file can be found in this git.

    #!/bin/bash
    #SBATCH --nodes=1
    #SBATCH --time=01:00:00
    #SBATCH --partition=express
    #SBATCH --array=1-55
    ASSEMBLY=$(sed -n "$SLURM_ARRAY_TASK_ID"p samples.txt)
 
    anvi-script-reformat-fasta ${ASSEMBLY}-final.contigs.fasta --simplify-names -o ${ASSEMBLY}_filter_contigs.fa -l 2500
    anvi-gen-contigs-database -f ASSEMBLIES/${ASSEMBLY}_filter_contigs.fa -o ASSEMBLIES/${ASSEMBLY}.db
    anvi-run-hmms -c ASSEMBLIES/${ASSEMBLY}.db -T 30
    anvi-run-ncbi-cogs -c ${SAMPLE}/${SAMPLE}.db -T 40 --cog-data-dir /work/jennifer.bowen/JOE/DBs/ANVIO-COG-db/
    anvi-run-pfams -c ${SAMPLE}/${SAMPLE}.db -T 40 --pfam-data-dir /work/jennifer.bowen/JOE/DBs/ANVIO-Pfam-db/
    anvi-run-kegg-kofams -c ${SAMPLE}/${SAMPLE}.db --kegg-data-dir /work/jennifer.bowen/JOE/DBs/ANVIO-KEGG-kofams-db/ -T 20
    bowtie2-build -f ASSEMBLIES/${ASSEMBLY}_filter_contigs.fa ASSEMBLIES/${ASSEMBLY}_filter_contigs

##  3. Map the reads from each of the metagenomic samples to each of the assemblies using bowtie, generate a filtered bam file that includes only the reads that mapped, and generate a profile database. To accomplish this, I generate a script for each of the samples and then run them in a way that doesn't overwhelm the server. 

#### a. generate the scripts

    python 
#### b. run the 



    

