# -----------------------------------------------------------------------------
# Copyright (c) 2019-, PKSHA Technology Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# -----------------------------------------------------------------------------

import sys
import os
import csv

import numpy as np
import argparse
from tqdm import tqdm

import chainer
from chainer.training import extensions
from chainer.dataset import convert

from .net import Net
from .loader.data_loader import NeologdDictionaryLoader
from .lang.japanese.kana.mora_sep import sep_katakana2mora
from .inference import InferAccent

from ..util.dic_index_map import get_dictionary_index_map

# hyper params
gpu_id = -1
bs = 64

def apply_all(
    test_csv, output_csv, up_symbol="[", down_symbol="]", mode="unidic"
):
    index_map = get_dictionary_index_map(mode)

    test_dat = NeologdDictionaryLoader(
        test_csv, infer_mode=True, index_map=index_map, store_entire_line=False
    )

    test_iter = chainer.iterators.SerialIterator(
        test_dat, bs, repeat=False, shuffle=False
    )

    model = InferAccent()
    with open(output_csv, "w") as ofs:
        csv_out = csv.writer(ofs)
        for batch_ in tqdm(test_iter, total=len(test_dat) // bs):
            batch = [a for a, b in batch_]
            orig_info = [b for a, b in batch_]

            batch = chainer.dataset.convert.concat_examples(
                batch, device=gpu_id, padding=0
            )
            X = batch[:-1]
            y_truth = batch[-1]  # Ground Truth

            # X   : (S_vow_np, S_con_np, S_pos_np, S_acc_np, S_acccon_np, S_gosh_np, Y_vow_np, Y_con_np)
            # X_s : (S_vow_np, S_con_np, S_pos_np, S_acc_np, S_acccon_np, S_gosh_np)
            # X_y :                                                                 (Y_vow_np, Y_con_np)
            X_s = X[:-2]
            X_y = X[-2:]
            y_dummy_GT = X_y[0] * 0  # dummy data

            # infer
            a_est = model.infer(X_s, X_y, y_dummy_GT)
            a_est = a_est.tolist()
            a_est = np.asarray(a_est).astype(np.int32)

            # postprocessing
            def proc(b, orig_info, a_est):
                idx, kanji, yomi, orig_entry = orig_info[b]
                A = a_est[b].tolist()
                A = A[: len(yomi)]
                y_ = [
                    y + (up_symbol if a_ == 2 else down_symbol if a_ == 0 else "")
                    for y, a_ in zip(sep_katakana2mora(yomi), A)
                ]
                y_ = "".join(y_)
                orig_entry[index_map["YOMI"]] = y_
                if mode == "unidic":
                    orig_entry[index_map["ACCENT"]] = "@"
                return orig_entry

            for i in range(len(batch_)):
                line = proc(i, orig_info, a_est)
                csv_out.writerow(line)

# =============================================================================================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input", type=str, help="input csv (neologd dicitionary file)"
    )
    parser.add_argument("-o", "--output", type=str, help="output csv")
    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        help="dictionary format type",
        choices=["unidic", "ipadic"],
        default="unidic",
    )
    args = parser.parse_args()

    if args.input == args.output:
        print("[ Error ] intput and output files should be different.")
    else:
        try:
            apply_all(
                test_csv=args.input,
                output_csv=args.output,
                mode=args.mode,
            )
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()