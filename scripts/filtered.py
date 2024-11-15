import sys
import os
import pandas as pd


sample_sheet_path = sys.stdin
base_data_dir = '/home/deserteagle/project/tcga_data_analysis/directory'

sample_sheet = pd.read_csv(sample_sheet_path, sep='\t', header='infer')


matching_samples = pd.DataFrame(columns=sample_sheet.columns)


for index, row in sample_sheet.iterrows():
    sample_id = row['File ID']  

    
    sample_dir = os.path.join(base_data_dir, sample_id)
    if os.path.isdir(sample_dir):
        
        matching_samples = pd.concat([matching_samples, pd.DataFrame([row])], ignore_index=True)

output_file=sys.stdout
matching_samples.to_csv(output_file, sep='\t',header=True, index=False)

