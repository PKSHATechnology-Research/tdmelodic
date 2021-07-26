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
from ..util.dic_index_map import get_dictionary_index_map
from ..util.util import count_lines

# unigram costなどを後処理で微調整するためのスクリプト

IDX_MAP = get_dictionary_index_map("unidic")

def avoid_overflow(line, cost, INT16_MIN = -32768, INT16_MAX = 32767):
    """avoid overflow (signed short int)"""
    cost = INT16_MAX if cost > INT16_MAX else INT16_MIN if cost < INT16_MIN else cost
    line[IDX_MAP["COST"]] = str(cost)
    return line, cost

def modify_unigram_cost(line, verbose=True):
    cost = int(line[IDX_MAP["COST"]])

    # 数詞のコストを必要に応じて調整する
    if (line[IDX_MAP["SURFACE"]][0] in [str(i) for i in range(10)]) and len(line[1]) >= 2:
        cost = cost - 5000

    # 人名のコストを必要に応じて調整する
    elif line[IDX_MAP["POS1"]] == "名詞" and line[IDX_MAP["POS2"]] == "固有名詞" and line[IDX_MAP["POS3"]] == "人名":
        cost = cost + 5000

    else:
    # 必要であればその他の単語のコストも全体的に高めるなど
    # （例えばUniDicに同じ単語がある場合はUniDicを優先させるなど）
        pass
        #cost = cost + 10000

    line, cost = avoid_overflow(line, cost)

    return line

# ------------------------------------------------------------------------------------
def main_(fp_in, fp_out):
    L = count_lines(fp_in)
    for i, line in enumerate(tqdm(csv.reader(fp_in), total=L)):
        # unigram cost を調整する
        line_modified = modify_unigram_cost(copy.deepcopy(line))

        if i % 100000 == 0:
            print(i)
            print("before", line, file=sys.stderr)
            print("after", line_modified, file=sys.stderr)

        # output
        line = ','.join(line_modified) + '\n'
        fp_out.write(line)

    print("Complete!", file=sys.stderr)
    return

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i',
        '--input',
        nargs='?',
        type=argparse.FileType("r"),
        default=sys.stdin,
        help='input CSV file (NEologd dicitionary file) <default=STDIN>')
    parser.add_argument(
        '-o',
        '--output',
        nargs='?',
        type=argparse.FileType("w"),
        default=sys.stdout,
        help='output CSV file <default=STDOUT>')
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