import sys
import pandas as pd


sample_sheet_path = sys.stdin
toselect = list(pd.read_csv("/home/deserteagle/project/tcga_data_analysis/data/to_select.tsv",sep='\t',names=['tumor_type'])['tumor_type'])



header = False
for line in sys.stdin:
    if not header:
        header=line
        print(line,end='')
        continue
    for q in toselect:
        if  q in line:
            print(line,end='')

        
