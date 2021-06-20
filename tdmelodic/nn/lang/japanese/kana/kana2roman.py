# -----------------------------------------------------------------------------
# Copyright (c) 2019-, PKSHA Technology Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# -----------------------------------------------------------------------------

import sys
import os

from .kanamap import kanamap_normal
from .mora_sep import sep_katakana2mora
from .hyphen2romaji import replace_hyphen_by_romaji


# get dict
k2r_dic = kanamap_normal.kana2roman_dictionary
_unknown_ = k2r_dic["0"]

# subsidiary functions
def _mora2roman(mora, UNKNOWN=_unknown_):
    """ unknown char -> UNKNOWN Token (#) """
    return k2r_dic[mora] if mora in k2r_dic.keys() else UNKNOWN

def _moralist2roman(moralist, UNKNOWN=_unknown_):
    return "".join([_mora2roman(m, UNKNOWN) for m in  moralist])

# main function
def kana2roman(kana):
    mora_list = sep_katakana2mora(katakana_text=kana)
    roman = _moralist2roman(mora_list)
    roman = replace_hyphen_by_romaji(roman)
    return roman

if __name__ == "__main__":
    katakana_texts=[
        "リンゴ",
        "アップル",
        "ミカン",
        "オレンジ",
        "パイナップル",
        "チョコレート",
        "マシュマロ",
    ]
    for t in katakana_texts:
        mora_list = sep_katakana2mora(katakana_text=t)
        roman = _moralist2roman(mora_list)
        roman_ = replace_hyphen_by_romaji(roman)
        print(mora_list)
        print(roman)
        print(roman_)
        print("{} -> {}".format(t, kana2roman(t)))
