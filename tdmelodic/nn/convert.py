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
# import argparse
import jaconv

import chainer
from chainer.training import extensions
from chainer.dataset import convert

from tdmelodic.nn.net import Net
from tdmelodic.nn.lang.mecab.unidic import UniDic
from tdmelodic.nn.lang.japanese.kana.mora_sep import sep_katakana2mora
from tdmelodic.nn.lang.japanese.kana.kanamap.kanamap_normal import roman_map
from tdmelodic.nn.lang.japanese.accent.accent_alignment import accent_map
from tdmelodic.nn.lang.category.symbol_map import char_symbol_to_numeric
from tdmelodic.nn.loader.data_loader import NeologdDictionaryLoader
from tdmelodic.nn.loader.data_loader import _convert_parsed_surface_to_codes
from tdmelodic.nn.loader.data_loader import _convert_yomi_to_codes
from tdmelodic.nn.inference import InferAccent
from tdmelodic.util.dic_index_map import get_dictionary_index_map

class Converter(object):
    # gpu_id = -1
    # bs = 1
    accent_symbol={0: "]", 1 : "", 2: "["}
    def __init__(self):
        self.model = InferAccent()
        self.unidic = UniDic()

    def encode_sy(self, surface, yomi):
        # analyze surface, and get the result of MeCab+UniDic
        lst_mecab_parsed, rank, ld = self.unidic.get_n_best(surface, yomi)
        mecab_parsed = lst_mecab_parsed[rank[0]]

        # convert to codes
        # codes : v_code, c_code, accent_code, pos_code, conc_code, gosh_code
        S_vow, S_con, S_acc, S_pos, S_acccon, S_gosh = _convert_parsed_surface_to_codes( mecab_parsed )
        Y_vow, Y_con = _convert_yomi_to_codes( yomi )

        # join
        S_vow    = ''.join([s + ' ' for s in S_vow])
        S_con    = ''.join([s + ' ' for s in S_con])
        S_acc    = ''.join([s       for s in S_acc])
        S_pos    = ''.join([s + ' ' for s in S_pos])
        S_acccon = ''.join([s + ' ' for s in S_acccon])
        S_gosh   = ''.join([s + ' ' for s in S_gosh])
        Y_vow    = ''.join([s + ' ' for s in Y_vow])
        Y_con    = ''.join([s + ' ' for s in Y_con])

        # adjust the length
        S_len = len(S_vow)
        Y_len = len(Y_vow)
        S_con    = (S_con    + " " * (S_len - len(S_con   ))) [:S_len]
        S_acc    = (S_acc    + " " * (S_len - len(S_acc   ))) [:S_len]
        S_pos    = (S_pos    + " " * (S_len - len(S_pos   ))) [:S_len]
        S_acccon = (S_acccon + " " * (S_len - len(S_acccon))) [:S_len]
        S_gosh   = (S_gosh   + " " * (S_len - len(S_gosh  ))) [:S_len]
        Y_vow    = (Y_vow    + " " * (Y_len - len(Y_vow   ))) [:Y_len]
        Y_con    = (Y_con    + " " * (Y_len - len(Y_con   ))) [:Y_len]

        # zeropad y
        pad = 8
        Y_vow    = (Y_vow    + "0" * pad) [:Y_len + pad]
        Y_con    = (Y_con    + "0" * pad) [:Y_len + pad]

        # convert to numpy array
        S_vow_np     = np.array( [roman_map[c]              for c in S_vow]    , np.int32)
        S_con_np     = np.array( [roman_map[c]              for c in S_con]    , np.int32)
        S_acc_np     = np.array( [accent_map[c]             for c in S_acc]    , np.int32)
        S_pos_np     = np.array( [char_symbol_to_numeric[c] for c in S_pos]    , np.int32)
        S_acccon_np  = np.array( [char_symbol_to_numeric[c] for c in S_acccon] , np.int32)
        S_gosh_np    = np.array( [char_symbol_to_numeric[c] for c in S_gosh]   , np.int32)
        Y_vow_np     = np.array( [roman_map[c]              for c in Y_vow]    , np.int32)
        Y_con_np     = np.array( [roman_map[c]              for c in Y_con]    , np.int32)

        # return encoded information
        S = S_vow_np, S_con_np, S_pos_np, S_acc_np, S_acccon_np, S_gosh_np
        Y = Y_vow_np, Y_con_np
        return S, Y

    def add_batch_dim(self, X_s, X_y):
        X_s = [np.expand_dims(xs, 0) for xs in X_s]
        X_y = [np.expand_dims(xy, 0) for xy in X_y]
        return X_s, X_y

    def infer(self, X_s, X_y):
        dummy = X_y[0] * 0  # dummy data
        accent = self.model.infer(X_s, X_y, dummy)
        accent = accent.tolist()
        accent = np.asarray(accent).astype(np.int32)
        return accent

    def zip_ya(self, yomi, accent):
        # the length of the list zip return is equalt to the shorter argument
        return "".join([y + self.accent_symbol[a]
            for y, a in zip(sep_katakana2mora(yomi), accent)])

    def sy2a(self, s, y):
        # preprocess strings
        s = s.strip()
        y = jaconv.normalize(y, "NFKC")
        y = jaconv.hira2kata(y)

        # encode
        s_np, y_np = self.encode_sy(s, y)
        s_np, y_np = self.add_batch_dim(s_np, y_np)

        # inference
        accent = self.infer(s_np, y_np)[0]
        yomi_and_accent = self.zip_ya(y, accent)
        return yomi_and_accent

    def s2ya(self, s):
        s = jaconv.normalize(s, "NFKC").strip()
        y = self.unidic.get_yomi(s).strip()
        return self.sy2a(s, y)

# =============================================================================================
def main_s2ya():
    tdmelodic = Converter()
    for surface in sys.stdin:
        accent = tdmelodic.s2ya(surface)
        print(accent)

def main_sy2a():
    tdmelodic = Converter()
    for line in sys.stdin:
        surface, yomi = line.strip().split(",")
        accent = tdmelodic.sy2a(surface, yomi)
        print(accent)
