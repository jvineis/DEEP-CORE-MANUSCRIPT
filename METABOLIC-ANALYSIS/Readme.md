## These are the steps to analyze the metabolic potential of MAGs

### Estimate metabolism for each MAG using anvio-estimate-metabolism. The required files "z_high_quality_MAG_list.txt and z_external-genomes.txt
### are included in this directory.

    #!/bin/bash
    #
    #SBATCH --nodes=1
    #SBATCH --tasks-per-node=1
    #SBATCH --time=08:00:00
    #SBATCH --mem=20Gb
    #SBATCH --array=1-377

    ASSEMBLY=$(sed -n "$SLURM_ARRAY_TASK_ID"p z_high_quality_MAG_list.txt)
    anvi-gen-contigs-database -f dereplicated_genomes/${ASSEMBLY}_contigs.fa -o dereplicated_genomes/${ASSEMBLY}.db
    anvi-run-kegg-kofams -c dereplicated_genomes/${ASSEMBLY}.db -T 40
    anvi-run-hmms -c dereplicated_genomes/${ASSEMBLY}.db -T 40
    anvi-run-kegg-kofams -c dereplicated_genomes/${ASSEMBLY}.db -T 40
    anvi-export-functions -c dereplicated_genomes/${ASSEMBLY}.db -o dereplicated_genomes/${ASSEMBLY}-functions.txt
    
#### Then you can estimate metaboilsm for all of the collective MAGs and write it to a singular file. This is how we estimated the number of complete pathways shown in figure 4c.

    #!/bin/bash
    #
    #SBATCH --nodes=1
    #SBATCH --tasks-per-node=1
    #SBATCH --time=02:00:00
    #SBATCH --mem=10Gb
    
    anvi-estimate-metabolism -e z_external-genomes.txt --matrix-format --include-metadata -O z_ALL-derep-MAGs-METABOLISM

#### To identify the presence of 





