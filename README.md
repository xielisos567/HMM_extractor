# HMM_extractor

This includes the step1_HMM_info_extract and the step2_HMM_gene_extract files, the usage of HMM-extractor is as follows:

### step1:
python3 HMM_info_extract.py lable_name path/lable path/data path/result score

### step2:
python3 HMM_gene_extract.py -i path/protein or path/cds -f path/HMM_seqs_test.txt -s path/species -o path/result_test
