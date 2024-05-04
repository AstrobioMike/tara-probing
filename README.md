# tara-probing

- TARA-info downloading and parsing are in the "tara-parsing-and-plotting" directory, there is a "log" file in there with commands and environments
- Workflows for downloading the SRA data and processing through to the gene-level KO coverage table were used from my [bit package](https://github.com/AstrobioMike/bit), retrieved and run as shown below:

```bash
conda create -n bit -c astrobiomike -c conda-forge -c bioconda -c defaults bit=1.9.1

conda activate bit

bit-get-workflow sra-download

#   The sra-download workflow was downloaded to
#   'bit-sra-download-wf-v1.0.0/'

#     It was pulled from this release page:
#         https://api.github.com/repos/astrobiomike/bit/releases

bit-get-workflow metagenomics

#   The metagenomics workflow was downloaded to
#   'bit-metagenomics-wf-v1.0.0/'

#     It was pulled from this release page:
#         https://api.github.com/repos/astrobiomike/bit/releases

## after modifying config.yaml files as appropriate, each were run in the bit conda environment in their respective directories with
snakemake --use-conda --conda-prefix ${CONDA_PREFIX}/envs -j 10 -p
```

Due to size, only the "Combined-gene-level-KO-function-coverages.tsv" table is included here.
