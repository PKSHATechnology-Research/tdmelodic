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

import re
import numpy as np
import csv
from pprint import pprint

import chainer
from chainer import dataset
from chainer import datasets
from chainer import iterators

# base
from .data_loader_base import DataLoaderBase

# unidic
from ..lang.mecab.unidic import UniDic

# textproc
from ..lang.japanese.text_normalize import normalize_jpn
from ..lang.japanese.kana.kana2roman import kana2roman
from ..lang.japanese.accent.accent_alignment import accent_align
from ..lang.japanese.accent.accent_diff import simple_accent_diff

# map code to int
from ..lang.category.symbol_map import acccon_map_robust
from ..lang.category.symbol_map import goshu_map_robust
from ..lang.category.symbol_map import pos_map_robust
from ..lang.category.symbol_map import numeric_to_char_symbol
from ..lang.category.symbol_map import char_symbol_to_numeric
from ..lang.japanese.kana.kanamap.kanamap_normal import roman_map
from ..lang.japanese.accent.accent_alignment import accent_map


# ------------------------------------------------------------------------------------
def split_codes_to_vowel_and_consonant(romancode):
    L = len(romancode)
    c = romancode[0::2]
    v = romancode[1::2]
    return c, v

# ------------------------------------------------------------------------------------
def _convert_yomi_to_codes(kana, **kwargs):
    pron = [kana]
    pron_code = ["".join([c for c in kana2roman(p)]) for p in pron]

    # split into vowel and consonant
    c_code = [split_codes_to_vowel_and_consonant(pron_code_)[0] for pron_code_ in pron_code]
    v_code = [split_codes_to_vowel_and_consonant(pron_code_)[1] for pron_code_ in pron_code]

    return c_code, v_code

# ------------------------------------------------------------------------------------
def _convert_parsed_surface_to_codes(mecab_p, **kwargs):
    """
    mecabのエントリは以下の通り。
    ["surface", "pron", "kana", "pos", "acc", "concat"]
    """
    pron = [e["pron"]   for e in mecab_p]
    pos  = [e["pos"]    for e in mecab_p]
    gosh = [e["goshu"]  for e in mecab_p]
    acc  = [e["acc"]    for e in mecab_p]
    conc = [e["concat"] for e in mecab_p]

    # code
    pron_code = ["".join([c for c in kana2roman(p)]) for p in pron]
    accent_code = [accent_align(y, a) for y, a in zip(pron_code, acc)]
    pos_code  = [numeric_to_char_symbol[pos_map_robust(s)   ] * len(w) for s, w in zip(pos,  pron_code)]
    conc_code = [numeric_to_char_symbol[acccon_map_robust(s)] * len(w) for s, w in zip(conc, pron_code)]
    gosh_code = [numeric_to_char_symbol[goshu_map_robust(s) ] * len(w) for s, w in zip(gosh, pron_code)]

    # Split prin_code into vowel and consonant
    c_code = [split_codes_to_vowel_and_consonant(pron_code_)[0] for pron_code_ in pron_code]
    v_code = [split_codes_to_vowel_and_consonant(pron_code_)[1] for pron_code_ in pron_code]

    # LH binary -> up down
    accent_code = [split_codes_to_vowel_and_consonant(a)[0] for a in accent_code]
    accent_code = [simple_accent_diff(a) for a in accent_code]

    # halve the length
    pos_code    = [split_codes_to_vowel_and_consonant(a)[0] for a in pos_code]
    conc_code   = [split_codes_to_vowel_and_consonant(a)[0] for a in conc_code]
    gosh_code   = [split_codes_to_vowel_and_consonant(a)[0] for a in gosh_code]

    # return
    codes = (c_code, v_code, accent_code, pos_code, conc_code, gosh_code)
    return codes


# ------------------------------------------------------------------------------------
class NeologdDictionaryLoader(DataLoaderBase):
    def __init__(self,
                csv_file='default_path.csv',
                verbose=False,
                valid_mode=False,
                infer_mode=False,
                index_map={
                    # see also mecabrc
                    'SURFACE': 1 + 0,
                    'COST'   : 1 + 3,
                    'POS1'   : 1 + 4 +  0, # f[0]:   pos1
                    'POS2'   : 1 + 4 +  1, # f[1]:   pos2
                    'POS3'   : 1 + 4 +  2, # f[2]:   pos3
                    'POS4'   : 1 + 4 +  3, # f[3]:   pos4
                    'YOMI'   : 1 + 4 +  9, # f[9]:   pron
                    'GOSHU'  : 1 + 4 + 12, # f[12]:  goshu
                    #ACCENT = 1 + 4 + 23 # f[23]:  aType
                    'ACCENT' : 23, # f[23]:  aType
                },
                load_all_lines_first=False,
                store_entire_line=False # store whole of the neologd dictionary data in memory if this flag is True.
                ):

        # flags
        self.infer_mode = infer_mode
        self.valid_mode = valid_mode

        self.store_entire_line = store_entire_line
        self.load_all_lines_first = load_all_lines_first

        self.index = index_map

        # on the data
        self.csv_file = csv_file
        self.lines = self._count_lines(csv_file)

        # load first
        if self.load_all_lines_first:
            self.neologd_quadraple, self.neologd_lines = self._load_word_list(csv_file)
        else:
            self.line_generator = self._read_line(self.csv_file)

        # load unidic
        self.unidic = UniDic()
        super().__init__()

    def _count_lines(self,text_file):
        c = 0
        cf = csv.reader(open(text_file, 'r'))
        for entry in cf:
            c += 1
        return c

    def _load_word_list(self, text_file, **kwargs):
        data_lst = []
        line_lst = []
        cf = csv.reader(open(text_file, 'r'))
        for entry in cf:
            surface = entry[self.index['SURFACE']]
            pos     = "-".join([e for e in entry[self.index['POS1']:self.index['POS4']+1] if len(e) > 0 and e != '*']) # we do not use them
            kana    = None #entry[11] # we do not use them
            yomi    = entry[self.index['YOMI']]
            goshu   = entry[self.index['GOSHU']] # we do not use them
            accent  = entry[self.index['ACCENT']] # annotated accent (during training only)
            data_lst.append([surface, kana, yomi, accent])
            if self.store_entire_line:
                line_lst.append(entry)
        return data_lst, line_lst

    def _read_line(self, text_file, **kwargs):
        cf = csv.reader(open(text_file, 'r'))
        for entry in cf:
            surface = entry[self.index['SURFACE']]
            pos     = "-".join([e for e in entry[self.index['POS1']:self.index['POS4']+1] if len(e) > 0 and e != '*']) # we do not use them
            kana    = None #entry[11] # we do not use them
            yomi    = entry[self.index['YOMI']]
            goshu   = entry[self.index['GOSHU']] # we do not use them
            accent  = entry[self.index['ACCENT']] # annotated accent (during training only)
            yield (surface, kana, yomi, accent, entry)

    def __len__(self):
        return self.lines
#        return len(self.neologd_quadraple)

    def _get_example_core(self, i):
        # i-th entry of neologd quadraples
        if self.load_all_lines_first:
            surface, kana, yomi, accent = self.neologd_quadraple[i]
        else:
            surface, kana, yomi, accent, line = next(self.line_generator)
        yomi_or_kana = yomi

        # analyze surface, and get the result of MeCab+UniDic
        surface_ = normalize_jpn(surface)
        tmp = self.unidic.get_n_best(surface_, yomi_or_kana)
        lst_mecab_parsed, rank, ld = tmp

        # Get pi^*(s)
        if self.valid_mode or self.infer_mode:
            # inference
            rank_ = rank[0]
        else:
            # training
            # randomly draw from N-best candidates
            rank_ = np.random.choice(rank)
        mecab_parsed = lst_mecab_parsed[rank_]

        # convert to codes
        # codes : v_code, c_code, accent_code, pos_code, conc_code, gosh_code
        S_vow, S_con, S_acc, S_pos, S_acccon, S_gosh = \
            _convert_parsed_surface_to_codes( mecab_parsed )
        Y_vow, Y_con = \
            _convert_yomi_to_codes( yomi_or_kana )

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
        Y_len = len(Y_vow) # len(accent)
        S_con    = (S_con    + " " * (S_len - len(S_con   ))) [:S_len]
        S_acc    = (S_acc    + " " * (S_len - len(S_acc   ))) [:S_len]
        S_pos    = (S_pos    + " " * (S_len - len(S_pos   ))) [:S_len]
        S_acccon = (S_acccon + " " * (S_len - len(S_acccon))) [:S_len]
        S_gosh   = (S_gosh   + " " * (S_len - len(S_gosh  ))) [:S_len]
        Y_vow    = (Y_vow    + " " * (Y_len - len(Y_vow   ))) [:Y_len]
        Y_con    = (Y_con    + " " * (Y_len - len(Y_con   ))) [:Y_len]

        # convert to numpy array
        S_vow_np     = np.array( [roman_map[c]              for c in S_vow]    , np.int32)
        S_con_np     = np.array( [roman_map[c]              for c in S_con]    , np.int32)
        S_acc_np     = np.array( [accent_map[c]             for c in S_acc]    , np.int32)
        S_pos_np     = np.array( [char_symbol_to_numeric[c] for c in S_pos]    , np.int32)
        S_acccon_np  = np.array( [char_symbol_to_numeric[c] for c in S_acccon] , np.int32)
        S_gosh_np    = np.array( [char_symbol_to_numeric[c] for c in S_gosh]   , np.int32)
        Y_vow_np     = np.array( [roman_map[c]              for c in Y_vow]    , np.int32)
        Y_con_np     = np.array( [roman_map[c]              for c in Y_con]    , np.int32)
        accent_np    = np.array( [0 if c == "0" else 2 if c== "2" else 1 for c in accent] , np.int32)

        # return X, y pairs
        X = S_vow_np, S_con_np, S_pos_np, S_acc_np, S_acccon_np, S_gosh_np, Y_vow_np, Y_con_np
        y = accent_np
        ret = X + (y,)

        if self.infer_mode:
            # 情報を表示するための情報を返す。
#            if self.store_entire_line:
            if self.load_all_lines_first:
                ret = [ret, (i, surface, yomi_or_kana, self.neologd_lines[i])]
            else:
                ret = [ret, (i, surface, yomi_or_kana, line)]
#                ret = [ret, (i, surface, yomi_or_kana)]
        return ret

if __name__ == "__main__":
    ds = NeologdDictionaryLoader()
    for n in range(2):
        for i in range(len(ds)):
            Xy = ds[i]
            X = Xy[:-1]
            y = Xy[-1]
            print("===", X[0], y)
