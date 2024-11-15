import sys
import os
import pandas as pd
from math import log2


filtered_sample_sheet_path = sys.stdin
base_data_dir = '/home/deserteagle/project/tcga_data_analysis/directory'


filtered_samples = pd.read_csv(filtered_sample_sheet_path, sep='\t')


results = []

for index, row in filtered_samples.iterrows():
    sample_id = row['File ID']  
    sample_type = row['Sample Type']  
    sample_dir = os.path.join(base_data_dir, sample_id)


    if os.path.isdir(sample_dir):

        for file_name in os.listdir(sample_dir):
            if file_name.endswith('.rna_seq.augmented_star_gene_counts.tsv'):
                file_path = os.path.join(sample_dir, file_name)


                expr_df = pd.read_csv(file_path, sep='\t',header=1)


                if 'gene_name' in expr_df.columns:
                    expr_df = expr_df.dropna(subset=['gene_name'])
                    nkx2_1_row = expr_df[expr_df['gene_name'] == 'NKX2-1']
                else:
                    print(f"'gene_name' column not found in {file_name}")
                    continue
                if not nkx2_1_row.empty:
                    tpm_value = nkx2_1_row.iloc[0, 6]
                    new_tpm = log2(tpm_value+1)
                    results.append({'Sample ID': sample_id, 'Sample Type': sample_type, 'TPM': tpm_value, 'new_TPM':new_tpm})
                else:
                    print(f"'gene_name'not found in {file_name}")

output_df = pd.DataFrame(results)
output_file = sys.argv[1]
output_df.to_csv(output_file, sep='\t', index=False)

