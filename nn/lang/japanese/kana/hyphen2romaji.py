# -----------------------------------------------------------------------------
# Copyright (c) 2019-, PKSHA Technology Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# -----------------------------------------------------------------------------

import sys
import os
import re

def replace_hyphen_by_romaji(text):
    """
    長音「ー」などを仮名に置換する。
    """

    # error check
    if len(text) < 2:
        return ""

    while "-" in list(text) or "~" in list(text):
        text_ = text

        if (text[0] == "-" or text[0] == "~") and len(text) >= 2:
            text = text[2:]
            continue

        text = re.sub(r"(?P<vowel>[aeiou])[-~][-~]", r"\g<vowel>x\g<vowel>", text) # "-" を 2文字
        text = re.sub(r"A[-~][-~]", r"Axa", text)
        text = re.sub(r"E[-~][-~]", r"Exe", text)
        text = re.sub(r"O[-~][-~]", r"Oxo", text)
        text = re.sub(r"U[-~][-~]", r"Uxu", text)
        if text_ == text:
            break # 変化しなかったら終わり

    return text

if __name__ == "__main__":
    print(replace_hyphen_by_romaji("xa--xi--xu--xe--xo--"))
    print(replace_hyphen_by_romaji("ka--ki--ku--ke--ko--"))
    print(replace_hyphen_by_romaji("haxnba--ga-~"))
    print(replace_hyphen_by_romaji("xA--xi--"))
    print(replace_hyphen_by_romaji("wa--------------xi"))
    print(replace_hyphen_by_romaji("~~~~hoge--"))
