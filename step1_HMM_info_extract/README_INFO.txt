#For batch consolidation of the results conducted with hmmsearch (large numbers of .tab files), users can execute the following command:
find  .  -name  "*.tab" | xargs -i cat {} > test_hmm_TMA_cnt.tab

#The final value of 200 indicates the results with a score ≥ 200, which can be adjusted freely. The execution code is as follows:
python3  HMM_info_extract.py  examples/test_hmm_TMA_cnt  examples/lable  examples/data   examples/result_test_hmm   200