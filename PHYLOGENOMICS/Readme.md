### The phylogenomic analysis was conducted according to the commands below. The fasta file of concatenated genes from the Bacteria_71 collection and alignment files are contained in this directory

    #!/bin/bash
    #
    #SBATCH --nodes=1
    #SBATCH --tasks-per-node=1
    #SBATCH --time=01:00:00
    #SBATCH --mem=1Gb
    #SBATCH --partition=express

    anvi-get-sequences-for-hmm-hits --external-genomes external-genomes.txt\
                                -o concatenated-proteins-full.fa \
                                --hmm-sources Bacteria_71 \
                                --return-best-hit \
                                --get-aa-sequences \
                                --concatenate-genes
                                
    trimal -in concatenated-proteins-full.fa -out concatenated-proteins-full-trimal.fa
                                
#### This is the treebuild using iqtree v 2.

    #!/bin/bash
    #
    #SBATCH --nodes=1
    #SBATCH --tasks-per-node=2
    #SBATCH --time=05:00:00
    #SBATCH --mem=50Gb
    #SBATCH --partition=short

    iqtree -s concatenated-proteins-full-trimal.fa -nt 40 -m WAG -bb 1000 -o concatenated-proteins-full-trimal.tre
    
