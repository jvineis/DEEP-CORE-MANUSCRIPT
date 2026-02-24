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


## 2. fix the deflines of each assembly fasta, build a contigs database, and run hmms on the datbase. The x_samples.txt file can be found in this git. I call the sbatch script below "x_gen-contigs-and-bowtie.shx".

    #!/bin/bash
    #SBATCH --nodes=1
    #SBATCH --time=01:00:00
    #SBATCH --partition=express
    #SBATCH --array=1-55
    ASSEMBLY=$(sed -n "$SLURM_ARRAY_TASK_ID"p x_samples.txt)
 
    anvi-script-reformat-fasta ${ASSEMBLY}-final.contigs.fasta --simplify-names -o ${ASSEMBLY}_filter_contigs.fa -l 2500
    anvi-gen-contigs-database -f ASSEMBLIES/${ASSEMBLY}_filter_contigs.fa -o ASSEMBLIES/${ASSEMBLY}.db
    anvi-run-hmms -c ASSEMBLIES/${ASSEMBLY}.db -T 30
    anvi-run-scg-taxonomy -c SW1601-110/SW1601-110-new.db -T 30
    anvi-run-ncbi-cogs -c ${SAMPLE}/${SAMPLE}.db -T 40 --cog-data-dir /work/jennifer.bowen/JOE/DBs/ANVIO-COG-db/
    anvi-run-pfams -c ${SAMPLE}/${SAMPLE}.db -T 40 --pfam-data-dir /work/jennifer.bowen/JOE/DBs/ANVIO-Pfam-db/
    anvi-run-kegg-kofams -c ${SAMPLE}/${SAMPLE}.db --kegg-data-dir /work/jennifer.bowen/JOE/DBs/ANVIO-KEGG-kofams-db/ -T 20
    bowtie2-build -f ASSEMBLIES/${ASSEMBLY}_filter_contigs.fa ASSEMBLIES/${ASSEMBLY}_filter_contigs

### execute the script using your slurm scheduler "shown below". If you don't have a slurm scheduler, you will need to alter pretty much everyting in this document.

    sbatch x_gen-contigs-and-bowtie.shx

##  3. Map the reads from each of the metagenomic samples to each of the assemblies using bowtie, generate a filtered bam file that includes only the reads that mapped, and generate a profile database. To accomplish this, I generate a script for each of the samples and then run them in a way that doesn't overwhelm the server. 

#### a. generate the scripts

    for i in `cat samples.txt`; do python create-deep-core-mapping-bowtie-mags.py ${i}; done
   
#### b. run each of the bash scripts created by the above script. NOTE: This will likely take up a lot of disk space, so be conscious of this and delete intermediate files as needed. Here is how to run one of the scripts created above

    sbatch SW1601-10_mapping.shx

## 4. Merge each of the profile dbs for each of the samples.

    #!/bin/bash
    #SBATCH --nodes=1
    #SBATCH --time=01:00:00
    #SBATCH --partition=express
    #SBATCH --array=1-55
    ASSEMBLY=$(sed -n "$SLURM_ARRAY_TASK_ID"p x_samples.txt)
 
    anvi-merge -c ${ASSEMBLY}/${ASSEMBLY}.db ${ASSEMBLY}/*PROFILE/PROFILE.db -o ${ASSEMBLY}/${ASSEMBLY}-MERGED

## 5. Estimate the number of genomes contained in each assembly and then run Concoct on the merged profile database using the extimated number of genomes in the "-c" parameter. This must be done separately for each sample. Below is the example for sample SW1601-110 

    anvi-display-contigs-stats SW1601-110/SW1601-110-new.db --report-as-text -o SW1601-110/SW1601-110-new-stats.txt

### This is what the "SW1601-110-new-stat.txt" file looks like. The last two lines of the file show that and evaluation of the bacteria_71 and archaea_76 single copy gene colletions indicate the presence of 116 MAGs in the assembly (99 bacteria and 17 archaea). 
    
    contigs_db	SW1601_110_filter_contigs
    Total Length	231389802
    Num Contigs	35536
    Num Contigs > 100 kb	40
    Num Contigs > 50 kb	255
    Num Contigs > 20 kb	1454
    Num Contigs > 10 kb	4535
    Num Contigs > 5 kb	13159
    Num Contigs > 2.5 kb	35536
    Longest Contig	221843
    Shortest Contig	2500
    Num Genes (prodigal)	236523
    L50	6788
    L75	17291
    L90	27114
    N50	7739
    N75	4166
    N90	3035
    Archaea_76	3902
    Bacteria_71	5936
    Protista_83	603
    Ribosomal_RNA_12S	0
    Ribosomal_RNA_16S	66
    Ribosomal_RNA_18S	0
    Ribosomal_RNA_23S	82
    Ribosomal_RNA_28S	0
    Ribosomal_RNA_5S	0
    eukarya (Protista_83)	0
    bacteria (Bacteria_71)	99
    archaea (Archaea_76)	17

### Now we are ready to run concoct, providing and estimate of 116 MAGs for the -c parameter 
   
    #!/bin/bash
    #SBATCH --nodes=1 
    #SBATCH --time=12:00:00
    #SBATCH --partition=short
    #SBATCH --tasks-per-node=20
    #SBATCH --mem=20GB
    
    concoct --composition_file SW1601-110-splits-and-coverage.txt/SW1601_110_MERGED-SPLITS.fa --coverage_file SW1601-110-splits-and-coverage.txt/SW1601_110_MERGED-COVs.txt -c 116 -b concoct_output/ --threads 20

### This is how we import the concoct collection into the contigs datbase to aid us in our ability to reconstruct genomes
### 1. first you need to remove the first line of the concoct clustering data and replace the commas with tabs
    
    cd concoct_output/
    grep -v "contig_id" clustering_gt1000.csv | tr "," '\t' > ../SW1601-110-concoct-clusters-for-anvio.txt
    awk 'BEGIN {OFS="\t";ORS="\n"} {
        if ($2 ~ /^[0-9]+(\.[0-9]+)?$/) {
            $2 = "cbin_" $2
        }
        print
    }' ../SW1601-110-concoct-clusters-for-anvio.txt > fix
    
### 2. make sure the file looks ok and then overwrite the original

    mv fix ../SW1601-110-concoct-clusters-for-anvio.txt

### 3. Import the collection. Keep in mind that this step was completed separately for each of the 55 assemblies.
    
    #!/bin/bash
    #SBATCH --nodes=1 
    #SBATCH --time=01:00:00
    #SBATCH --tasks-per-node=1
    #SBATCH --mem=1GB

    anvi-import-collection SW1601-110-concoct-clusters-for-anvio.txt -p SW1601-110-MERGED/PROFILE.db -c SW1601-110/SW1601-110-new.db -C CONCOCT

## 6. Now we are ready to manually bin each of the 55 assemblies. I have created a vidoe of this step to aid in the understanding of how I manually recruited the contings into bins. This process is very labor intensive and if there are more than 20 samples, it is generally advisable to use several automated binning tools followed by a method to integrate the individual tools into a single collection of bins. However, due to our interest in the potentially novel genomic structures that might exist and the desire to generate the highest quality bins possible, we endeavored to embark on this manual reconstruction process.

[Manual Binning with Anvi'o](https://www.youtube.com/watch?v=wNCTNkbmsag)
    
## 7. Dereplication. Following the manual reconstruction process, we migrated all MAGs to a single directory and used dREP to identify genome populations that were identified in multiple samples and to choose a representative MAG for each of the "duplicated" genomes in our collection.

    #!/bin/bash
    #
    #SBATCH --nodes=1
    #SBATCH --tasks-per-node=20
    #SBATCH --time=24:00:00
    #SBATCH --mem=50Gb
    #SBATCH --partition=short

    dRep dereplicate z_HIGH-QUALITY-DEREP-TEST-OUTPUT -g z_HIGH-QUALITY-FASTA/*.fa -p 40 --set_recursion 3000

## 8. Dereplication of Patescibacteria. Because the completion scores for all Patescibacteria are below the dRep threshold, we used the taxononmy (based on single copy gene calls) from Anvio to place all Patescibacteria into a single directory and run dereplication with relaxed completion scores. 

    #!/bin/bash
    #
    #SBATCH --nodes=1
    #SBATCH --tasks-per-node=20
    #SBATCH --time=01:00:00
    #SBATCH --mem=50Gb
    #SBATCH --partition=express

    dRep dereplicate z_HIGH-QUALITY-PATESCI-OUTPUT -g z_HIGH-QUALITY-PATESCI-FASTA/*.fa --ignoreGenomeQuality -p 40


    
    


    

