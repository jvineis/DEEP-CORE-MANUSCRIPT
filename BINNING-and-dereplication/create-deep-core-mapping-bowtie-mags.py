#!/usr/bin/env python

import sys

infile = sys.argv[1]
for i in open(infile, 'r'):
    print(i)
    x = i.strip()
    outfile = open(x+"_mapping.shx", 'w')
    outfile.write("#!/bin/bash"+'\n'+
                  "#SBATCH --nodes=1"+'\n'+
                  "#SBATCH --tasks-per-node=10"+'\n'+
                  "#SBATCH --mem=2Gb"+'\n'+
                  "#SBATCH --time=00:45:00"+'\n'+
                  "#SBATCH --partition=express"+'\n'+
                  "#SBATCH --array=1-55"+'\n'+
                  '\n'+
                  "SAMPLE=$(sed -n "+'"'+'$'+"SLURM_ARRAY_TASK_ID"+'"'+"p x_sample-names.txt)"+'\n'+
                  "var=*"+'\n'+
                  "echo "+'"'+'$'+"var"+'"'+'\n'+
                  "var="+'"'+'$'+"(echo *)"+'"'+'\n'+
                  '\n'+
                  "ref_file="+x+'\n'+
                  "fastq_file=$( echo "+'"'+"/work/jennifer.bowen/JOE/DEEP-CORE/Filtered_JGI-metaG_reads/${SAMPLE}-METAGENOME.fastq.gz"+'"'+")"+'\n'+
                  "output_file=x_DEREPLICATED-MAPPING/"+x+"-vs-${SAMPLE}.sam"+'\n'+
                  "#covstats_file=x_DEREPLICATED-MAPPING/"+x+"-vs-${SAMPLE}-covstats.txt"+'\n'+
                  "bowtie2 -q -x ${ref_file} --interleaved ${fastq_file} -S ${output_file}"+'\n'+
                  "samtools view -F 4 -bS ${output_file} > x_DEREPLICATED-MAPPING/"+x+"-vs-${SAMPLE}-RAW.bam"+'\n'+
                  "anvi-init-bam x_DEREPLICATED-MAPPING/"+x+"-vs-${SAMPLE}-RAW.bam -o x_DEREPLICATED-MAPPING/"+x+"-vs-${SAMPLE}.bam"+'\n'+
                  "anvi-profile -i x_DEREPLICATED-MAPPING/"+x+"-vs-${SAMPLE}.bam -c "+x+".db -o x_DEREPLICATED-MAPPING/"+x+"-vs-${SAMPLE}-PROFILE"+'\n')
