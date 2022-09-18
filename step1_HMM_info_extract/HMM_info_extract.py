#!/bin/python3

import re
import os
import sys
import glob
import pandas as pd
from collections import defaultdict

def getLable(lable):
    '''
    get gene name in lable
    '''
    lable_file = open(lable)
    lables = []
    for line in lable_file:
        lables.append(line.strip())
    lable_file.close()
    return set(lables)

def getHmmIndex(stext, target=' '):
    target_idnex = []
    i = 0
    start_r = 0
    for s in stext:
        if s == '-' and start_r == 0:
            start_r = 1
        if s == target and start_r != 0:
            target_idnex.append(i)
        i+= 1
    return target_idnex

def getData(file, lable, score, out):
    infile = open(file)
    headers = {}
    score_left = 0
    score_right = 0
    for line in infile:
        header_line = line.strip()
        if line.startswith('# target name'):
            total = 0
            file_index = 0
            score_max = 0
            already = []
            sep_line = next(infile)
            sep_index = getHmmIndex(sep_line)
            if len(headers) == 0:
                start = 0
                for idx in sep_index:
                    key = line[start:idx].strip()
                    for i in range(1,10):
                        if key in headers:
                            key += str(i)
                    headers[key] = []
                    start = idx 
                headers[line[start:].strip()] = []
                headers['file'] = []
            idx_key = {}
            headers_tmp = {}
            start = 0
            for idx in sep_index:
                key = line[start:idx].strip()
                for i in range(1,10):
                    if key in headers_tmp:
                        key += str(i)
                headers_tmp[key] = ''
                idx_key[idx] = key
                if key == 'score':
                    score_left = start
                    score_right = idx
                start = idx
            while True:
                line = next(infile).strip()
                if not line.startswith('#'):
                    score_tmp = float(line[score_left:score_right].strip())
                    if  ((score_max==0 and score_tmp>=score) or (score_tmp>=score and score_max!=0 and score_max-score_tmp<=20)) and line[0:sep_index[0]].strip() not in already:
                        if score_max == 0:
                            score_max = float(line[score_left:score_right].strip())
                        #rint (line)
                        total += 1
                        start = 0
                        file_index = 1
                        already.append(line[0:sep_index[0]].strip())
                        for idx in sep_index:
                            key = idx_key[idx]
                            headers[key].append(line[start:idx].strip())
                            start = idx + 1
                        headers[header_line[start:]].append(line[start:].strip())
                elif line.startswith('# Program') and total == 0:
                    break
                elif line.startswith('# Target file') and file_index == 1:
                    file_name = os.path.basename(line.split(' ')[-1]).strip()
                    for i in range(total):
                        headers['file'].append(file_name)
                    file_index = 0
                    total = 0
                elif line.startswith('# [ok]'):
                    break
    infile.close()
    '''
    for key in headers:
        print (key, len(headers[key]))
    '''
    out_data = pd.DataFrame(headers)
    cols = ['GenomesID']
    cols.extend(list(out_data.columns))
    out_data['GenomesID'] = out_data['file'].apply(lambda x:'.'.join(x.split('.')[:-1]))
    out_data = out_data.loc[:, cols]
    genomes_ids = set(out_data['GenomesID'].to_list())
    for genome in genomes_ids:
        genes = set(out_data[out_data['GenomesID']==genome]['query name'].to_list())
        if len(genes.intersection(lable)) == len(lable):
            continue
        else:
            out_data = out_data.drop(out_data[out_data['GenomesID']==genome].index)
    out_data.to_csv(out, sep='\t', index=False)

if __name__ == '__main__':
    if len(sys.argv) != 6:
        print ('Usage: python3 hmmsearch-parse.py lable_name lable_path data_path out_path score')
        sys.exit()
    lable_name = sys.argv[1]
    lable_path = sys.argv[2]
    data_path = sys.argv[3]
    out_path = sys.argv[4]
    score_set = int(sys.argv[5])
    lables = getLable(f'{lable_path}/{lable_name}.txt')
    if os.path.exists(out_path):
        pass
    else:
        os.makedirs(out_path)
    for file in glob.glob(f'{data_path}/*tab'):
        out_name = os.path.basename(file)
        if re.search(lable_name, file):
            getData(file, lables, score_set, f'{out_path}/{out_name}.xls')