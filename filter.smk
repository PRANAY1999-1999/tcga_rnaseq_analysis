import sys
import pandas as pd

run_df = pd.read_csv("/home/deserteagle/project/tcga_data_analysis/data/run_matadata.tsv", sep="\t",header="infer")
sample_df= pd.read_csv("/home/deserteagle/project/tcga_data_analysis/data/sample.tsv", sep="\t", header="infer")

run_df.index = run_df["run"]
sample_df.index = sample_df["sample"]

print(run_df)
print(sample_df)

def get_all_runs_for_a_sample (wildcards):
    all_runs = sample_df.loc[wildcards.sample, "runs"].split(",")
    run_path_list = []
    for r in all_runs:
        p = run_df.loc[r, "file_path"]
        run_path_list.append(p)
    return run_path_list

print(get_all_runs_for_a_sample)

rule filter_file_based_on_directory:
    input:
        all_runs = lambda wildcards: get_all_runs_for_a_sample(wildcards)
    output:
        filter_file = "filter_file/for_{sample}.tsv"
    shell:
        "cat {input.all_runs} | awk 'NR==1;BEGIN {{IGNORECASE=1}} /primary tumor|solid tissue normal/ {{print $0}}' > {output.filter_file}"

rule find_gene_in_filtered_file:
    input:
         filter_file = "filter_file/for_{sample}.tsv"
    output:
         find_gene = "find_gene/gene_{sample}.tsv"
    shell:
         "cat {input.filter_file} | python3 scripts1/find_file.py {output.find_gene}"

rule box_plot:
    input:
        find_gene = "find_gene/gene_{sample}.tsv"
    output:
        plot_box = "plot/plot_{sample}.png"
    shell:
        "cat {input.find_gene} | Rscript scripts2/plot.R {output.plot_box}" 
