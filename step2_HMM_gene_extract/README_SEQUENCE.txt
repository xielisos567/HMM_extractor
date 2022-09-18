#Note that the first column cannot contain characters like "_protein", and the third column must be the category (such CntA and CntB) to be extracted
#Match and output according to the range given in the species file and the unmatched genome will be placed in nohup.out file, which can be further used to filter genomes such as the non-reference types. The execution code is as follows (proteins and nucleotides):
python3  HMM_gene_extract.py  -i  examples/protein  -f  examples/HMM_info_test.txt  -s  examples/species  -o  examples/results/result_protein_test
python3  HMM_gene_extract.py  -i examples/cds  -f  examples/HMM_info_test.txt  -s  examples/species  -o  examples/results/result_cds_test

#Users can then extract the gene length information, and filter out those genes that do not match the length of reference sequences, so as to generate the final results (gene dataset). Follows is the execution code:
seqkit  fx2tab --length --name --header-line  input.fa
#Make sure seqkit is installed:
conda install -c bioconda seqkit
