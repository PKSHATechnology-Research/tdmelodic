# -----------------------------------------------------------------------------
# Copyright (c) 2019-, PKSHA Technology Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# -----------------------------------------------------------------------------

# -*- coding: utf-8 -*-
import sys
import os
import argparse
import csv
import copy
from tqdm import tqdm

# unigram costなどを後処理で微調整するためのスクリプト

# ------------------------------------------------------------------------------------
# see also mecabrc
IDX_SURFACE= 0
IDX_COST   = 3
IDX_POS1   = 4 +  0 # f[0]:   pos1
IDX_POS2   = 4 +  1 # f[1]:   pos2
IDX_POS3   = 4 +  2 # f[2]:   pos3
IDX_YOMI   = 4 +  9 # f[9]:   pron
IDX_GOSHU  = 4 + 12 # f[12]:  goshu
IDX_ACCENT = 4 + 23 # f[23]:  aType

# ------------------------------------------------------------------------------------
def count_lines(fname):
    with open(fname, 'r') as f:
        for i, l in enumerate(f):
            pass
    return i + 1

# ------------------------------------------------------------------------------------
def modify_unigram_cost(line, verbose=True):
    cost = int(line[IDX_COST])

    #------------------------------------------------------------------------------
    # 数詞のコストを必要に応じて調整する
    if (line[IDX_SURFACE][0] in [str(i) for i in range(10)]) and len(line[1]) >= 2:
        cost = cost - 5000

    # 人名のコストを必要に応じて調整する
    elif line[IDX_POS1] == "名詞" and line[IDX_POS2] == "固有名詞" and line[IDX_POS3] == "人名":
        cost = cost + 5000

    else:
    # 必要であればその他の単語のコストも全体的に高めるなど
    # （例えばUniDicに同じ単語がある場合はUniDicを優先させるなど）
        pass
        #cost = cost + 10000

    #------------------------------------------------------------------------------

    # avoid overflow (signed short int)
    INT16_MIN = -32768
    INT16_MAX = 32767
    cost = INT16_MAX if cost > INT16_MAX else INT16_MIN if cost < INT16_MIN else cost
    # convert to string
    line[IDX_COST] = str(cost)

    return line

# ------------------------------------------------------------------------------------
def main_(neologd_csv, output_csv):
    L = count_lines(neologd_csv)
    fp_in = csv.reader(open(neologd_csv, 'r'))

    with open(output_csv, mode='w') as fp_out:
        for i, line in enumerate(tqdm(fp_in, total=L)):
            # unigram cost を調整する
            line_modified = modify_unigram_cost(copy.deepcopy(line))

            if i % 100000 == 0:
                print(i)
                print("before", line)
                print("after", line_modified)

            # output
            line = ','.join(line_modified) + '\n'
            fp_out.write(line)

    print("Complete! Saved the converted file as ... ", output_csv)
    return

def main():
    '''
usage :
    cp tdmelodic.csv tdmelodic.csv.bak
    python tdmelodic/script/postprocess_modify_unigram_cost.py -i tdmelodic.csv.bak -o tdmelodic.csv
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str,
                        help='input csv (neologd dicitionary file)')
    parser.add_argument('-o', '--output', type=str,
                        help='output csv')
    args = parser.parse_args()
    if args.input == args.output:
        print("[ Error ] intput and output files should be different.")
    else:
        try:
            main_(args.input, args.output)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()