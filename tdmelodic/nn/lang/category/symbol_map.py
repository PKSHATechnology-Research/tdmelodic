# -----------------------------------------------------------------------------
# Copyright (c) 2019-, PKSHA Technology Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# -----------------------------------------------------------------------------

import os, sys
import re

from .list_of_symbols.acc_concat import accent_map, accent_invmap
from .list_of_symbols.goshu import goshu_map, goshu_invmap
from .list_of_symbols.pos_short import pos_map, pos_invmap

# キーが定義されていないものは None と同じもの(0番)を返す。
def acccon_map_robust(x):
    return accent_map[x] if x in accent_map.keys() else 0

def goshu_map_robust(x):
    return goshu_map[x] if x in goshu_map.keys() else 0

def pos_map_robust(x):
    return pos_map[x] if x in pos_map.keys() else 0

# 数値 -> 記号
import string
numeric_to_char_symbol = {i + 1: c for
    i, c in enumerate(string.digits +
                string.ascii_letters +
                string.punctuation)}
numeric_to_char_symbol[0] = " " # 空白は0番と同一視。
char_symbol_to_numeric = {v: k for k, v in numeric_to_char_symbol.items()}

if __name__ == '__main__':
    from pprint import pprint
    pprint(numeric_to_char_symbol)
    pprint(char_symbol_to_numeric)
