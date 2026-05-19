#!/usr/bin/env python
import sys

## THis is key: Make sure that the order of the columns (samples) is the same in
## both the mean and variability matrices. I do this manually, because i'm not that good at it :).


outfile = open(sys.argv[4], 'w')
outfile.write("uid"+'\t'+"mean_or_var"+'\t'+"core"+'\t'+"depth")
# Dictionary of the variability
var_dict = {}
# Dictionary of the mean
mean_dict = {}

# Create the variability dictionary
for i in open(sys.argv[1], 'r'):
    x = i.strip().split('\t')
    if "Sal" in x[0]:
        mean_dict[x[0]] = x[0:len(x)]
    else:
        outfile.write('\t'.join(x)+'\n')

# Create the mean dictionary
for i in open(sys.argv[2], 'r'):
    x = i.strip().split('\t')
    if "Sal" in x[0]:
        var_dict[x[0]] = x[0:len(x)]

mag_list = []
for element in open(sys.argv[3], 'r'):
    x = element.strip().split('\t')
    for mag in x:
        mag_list.append(mag)
        print(mag)

def get_mean(mag):
    meanr = []
    for key in mean_dict.keys():
        if key == mag:
            meanr.append("mean")
            for item in mean_dict[key]:
                meanr.append(item)
    return(meanr)

def get_var(mag):
    varr = []
    for key in var_dict.keys():
        if key == mag:
            varr.append("varibility")
            for item in var_dict[key]:
                varr.append(item)
    return(varr)

count = 0
for mags in mag_list:
    m = get_mean(mags)
    v = get_var(mags)
    outfile.write("a"+str(count)+'\t'+'\t'.join(m)+'\n')
    outfile.write("a"+str(count+1)+'\t'+'\t'.join(v)+'\n')
    count += 2
