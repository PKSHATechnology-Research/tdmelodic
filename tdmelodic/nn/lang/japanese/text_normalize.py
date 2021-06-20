# -----------------------------------------------------------------------------
# Copyright (c) 2019-, PKSHA Technology Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# -----------------------------------------------------------------------------

import os, sys
import re

from .kansuji import numeric2kanji
import jaconv


#このファイルでは以下を実施する。
#    ・数字列をすべて漢数字に変換する。
#    ・英字アルファベットを全て小文字から大文字に変換する。
#    ・英字アルファベットを全て全角に変換する。

def suuji(text):
    # 数字の間の小数点を「点」にする
    text = re.sub(r"(?<!\d)0\.(\d+)", r"零点<NON_CONVERT>\1</NON_CONVERT>", text, count=0, flags=0)
    text = re.sub(r"\.(\d+)", r"点<NON_CONVERT>\1</NON_CONVERT>", text, count=0, flags=0)
    text = re.sub(r"(\d+)", r"<CONVERT>\1</CONVERT>", text, count=0, flags=0)

    # 数字表現
    text = numeric2kanji(text)

    # タグ消し
    text = text.replace("<CONVERT>","").replace("</CONVERT>","")
    text = text.replace("<NON_CONVERT>","").replace("</NON_CONVERT>","")

    return text

def normalize_jpn(text):
    text = suuji(text)
    text = jaconv.h2z(text.upper(), ignore='', kana=True, ascii=True, digit=True)
    text = text.replace("ー","ー")
    return text

if __name__ == "__main__":
    text = "12345.67890あああ林檎蜜柑リンゴミカンABCDEFGabcdefg1234あ5あ0.3あ3あああ。"
    text = normalize_jpn(text)
    print(text)
