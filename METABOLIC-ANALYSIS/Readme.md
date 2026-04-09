## These are the steps to analyze the metabolic potential of MAGs

### Estimate metabolism for each MAG using anvio-estimate-metabolism. The required files "z_high_quality_MAG_list.txt and z_external-genomes.txt" are included in this directory.

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

#### With some minor edits to the input, you can use R to create the box-whisker plots show in figure 4c. The key file to reconstruct the plot "abund_modules_dat" is included in this directory
    library(ggplot2)
    library(phyloseq)
    library(vegan)
    joes_custom <- c("#762a83","#af8dc3","#e7d4e8","#d9f0d3","#7fbf7b","#1b7837","#ffffbf","#fc8d59","#fee08b","#2166ac",
    "#66c2a5","#3288bd","#21666a","#d73027","#053061","#d6604d","#f4a582","#000542","#fcc000","#ffff01","#bbb000","#000998",
    "#a99999","#b98765","#ddd000","#aaaaff","#000011","#0000ff","#0000aa","#aacc00","#b99999","#cccfff")

    dat = read.table("~/Documents/DEEP-CORE/ABUNDANCE/z_ALL-read-recruitment-per-MAG.txt", header = TRUE, row.names = 1, sep = '\t')
    tdat = read.table("~/Documents/DEEP-CORE/COMMUNITY-ANALYSIS/deep-core-metadata-for-community-analysis.txt", header = TRUE, row.names = 1, sep = '\t')
    mdat = read.table("~/Documents/DEEP-CORE/sample-metadata-all.txt", header = TRUE, row.names = 1, sep = '\t')

    ## convert the occurrence table to a matrix
    pfmat <- as.matrix(dat)
    ## convert the Mag metadata to a matrix
    pftax <- as.matrix(tdat)

    ## convert the matrices to phyloseq input formats
    OTU <- otu_table(pfmat, taxa_are_rows = TRUE)
    TAX <- tax_table(pftax)
    meta <- sample_data(mdat)

    ## Create the phyloseq object
    physeq <- phyloseq(OTU, TAX, meta)
    physeq1 = transform_sample_counts(physeq, function(x) x/sum(x)*100)

    abund_modules <- subset_taxa(physeq1, module == "a_0" | module == "a_1" | module == "a_2" | module == "a_3" | module == "a_4" | module == "a_5" | module == "a_6" | module == "a_7")
    abund_modules <- prune_taxa(taxa_sums(abund_modules)>8, abund_modules)
    abund_modules_dat <- data.frame(tax_table(abund_modules))
    abund_modules_dat$module <- factor(abund_modules_dat$module, levels=c("a_0", "a_3", "a_6", "a_5", "a_1", "a_2","a_4", "a_7"))
    abund_modules_dat$total_complete_pathways <- as.numeric(abund_modules_dat$total_complete_pathways)

    ggplot(abund_modules_dat, aes(x = total_complete_pathways, y = module))+
      geom_boxplot()+
      geom_jitter(aes(fill = phylum),shape = 21, size = 2.5)+
      scale_fill_manual(values= joes_custom1)+
      coord_flip()

### To identify the presence of 





