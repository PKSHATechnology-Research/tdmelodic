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

mora_with_subs = kanamap_normal.exceptions.keys()
small_vowel = list("ァィゥェォャュョヮぁぃぅぇぉゃゅょゎ")
large_vowel = {
    "ァ":"ア",
    "ィ":"イ",
    "ゥ":"ウ",
    "ェ":"エ",
    "ォ":"オ",
    "ャ":"ヤ",
    "ュ":"ユ",
    "ョ":"ヨ",
    "ヮ":"ワ",
    "ぁ":"ア",
    "ぃ":"イ",
    "ぅ":"ウ",
    "ぇ":"エ",
    "ぉ":"オ",
    "ゃ":"ヤ",
    "ゅ":"ユ",
    "ょ":"ヨ",
    "ゎ":"ワ",
}

def sep_katakana2mora(katakana_text=""):
    eos_char = "@"
    lst = list(katakana_text + eos_char)
    lst1, lst2 = lst[:-1], lst[1:]

    concat_ = [      [i + j, ""]            if i + j in mora_with_subs # i + j が「キャ」「シュ」などのパターンに合致する場合
                else [i, large_vowel[j]]    if ((not i in small_vowel) and (    j in small_vowel)) # それ以外のパターンの場合。
                else ["", ""]               if ((    i in small_vowel) and (not j in small_vowel))
                else [large_vowel[i], ""]   if ((    i in small_vowel) and (    j in small_vowel))
                else [i, ""] # それ以外は普通に返す。
                for i, j in zip(lst1, lst2) ]

    concat_ = sum(concat_, [])
    concat = [i for i in [c for c in concat_ if c != ""] if i != ""]

    return concat

if __name__ == "__main__":
    # test
    test_str = [
        "キューリョービ",
        "シュークリーム",
        "クィニーアマン",
        "クロワッサン",
        "シークヮーサー",
        "ベートーヴェン",
        "ドストエフスキィ",
        "ウワァ",
        "ウワァァ",
        "ウワァァァァァァァ",
        "ァアィアアゥアウアアウィアァアァアァアアウォオゥオァアァ"
    ]
    for s in test_str:
        print("{}\n{}\n{}".format(s, str(sep_katakana2mora(s)),'-'*80))
