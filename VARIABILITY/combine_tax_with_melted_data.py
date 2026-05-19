#!/usr/bin/env python

import sys

outfile = open(sys.argv[3], 'w')

tax_dict = {}

for i in open(sys.argv[1], 'r'):
    x = i.strip().split('\t')
    tax_dict[x[0]] = x[0:len(x)]


for i in open(sys.argv[2],'r'):
    x = i.strip().split('\t')
    if x[0] == "uid":
        outfile.write('\t'.join(x)+'\t'+"tax"+'\n')
    elif tax_dict[x[2]][16] == "YES":
        outfile.write('\t'.join(x)+'\t'+tax_dict[x[2]][15]+'\n')
