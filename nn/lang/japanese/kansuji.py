# -----------------------------------------------------------------------------
# Copyright (c) 2019-, PKSHA Technology Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# -----------------------------------------------------------------------------

import re

"""
数字列を漢数字に変換する。
"""

digit2kanji = {
    '0':'零',
    '1':'一',
    '2':'二',
    '3':'三',
    '4':'四',
    '5':'五',
    '6':'六',
    '7':'七',
    '8':'八',
    '9':'九'
}
unit_1 = ['', '十', '百', '千']
unit_2 = ['', '万', '億', '兆',
        '京', '垓', '𥝱', '穣',
        '溝', '澗', '正', '載',
        '極', '恒河沙', '阿僧祇',
        '那由他', '不可思議', '無量大数']
unit = sum([[u1 + u2 if u1 == '' else u1 for u1 in unit_1] for u2 in unit_2], [])

def split_4(lst):
    return ["".join(lst[0+n:4+n]) for n in range(0, int(len(lst)), 4)]

def _case_straightforward(num_str):
    """ simply replace """
    kanji = "".join([digit2kanji[n] for n in num_str])
    return kanji

def _case_int(num_str):
    if num_str in ['0', '']:
        return digit2kanji['0']
    else:
        lst = split_4(list(reversed(num_str)))
        fourdigits = ["".join(reversed([
                                ''        if r == '0' else
                                unit_1[i] if r == '1' and (i == 1 or i == 2) else
                                digit2kanji[r] + unit_1[i]
                            for i, r in enumerate(l)]
                        )) for l in lst]
        tmp = "".join(reversed([
                                ''            if l == '' else
                                l + unit_2[i]
                        for i, l in enumerate(fourdigits)]
                        ))

        # "一千"などを修正
        ret = re.sub('一千(?![{}])'.format("".join(unit_2)), '千', tmp)
        return ret

def _case_float(num_str):
    # 小数
    sep = num_str.split(".")

    # 整数部分
    i_str = sep[0]
    i_kanji = _case_int(i_str)

    # 小数部分
    if len(sep) >= 2 and sep[1] != '':
        d_str = sep[1:]
        d_kanji = "点".join([_case_straightforward(d) for d in d_str])
        num_kanji = i_kanji + "点" + d_kanji
    else:
        num_kanji = i_kanji

    return num_kanji

def num2kansuji(num_str, mode='digit'):
    '''
    数字列を漢数字に変換する。

    mode=digitのときはそのまま漢数字にする。
    mode=replaceのときは単に置換する。
    '''

    if len(num_str) > 72:
        print(" ********** error 73文字以上の数字が入力されました。無視してそのまま出力します。 **************", len(num_str))
        return num_str

    num_str = num_str.replace(",", '') # 桁区切りのカンマは削除

    if mode == 'digit':
        return _case_float(num_str)
    elif mode == 'replace':
        return _case_straightforward(num_str)
    else:
        # default
        return _case_float(num_str)

def numeric2kanji(text_orig):
    r = re.compile(r"[0-9０-９.]+", flags=0) # 小数点（仮）
    digits = r.findall(text_orig)
    split = r.split(text_orig)

    # convert
    digits_ = []
    for d in digits:
        d_orig = d
        d = d.replace("１","1").\
            replace("２","2").\
            replace("３","3").\
            replace("４","4").\
            replace("５","5").\
            replace("６","6").\
            replace("７","7").\
            replace("８","8").\
            replace("９","9").\
            replace("０","0")
        d = num2kansuji(d)
        digits_.append(d)
    digits = digits_

    # join
    l = max(len(digits), len(split))
    digits = (digits + [""] * 3)[:l]
    split  = (split  + [""] * 3)[:l]

    converted = "".join([t + str(d) for t, d in zip(split, digits)])
    return converted


if __name__ =='__main__':
    # tests
    print(num2kansuji("123"))
    print(num2kansuji("100"))
    print(num2kansuji("103"))
    print(num2kansuji("111"))
    print(num2kansuji("123456"))
    print(num2kansuji("123412341234"))
    print(num2kansuji("100010001000"))
    print(num2kansuji("100011001000"))
    print(num2kansuji("1020304050607080"))
    print(num2kansuji("123412341234123400001234"))
    print(num2kansuji("12345678901234567890123456789012345678901234567890123456789012345678901"))
    print(num2kansuji("123456789012345678901234567890123456789012345678901234567890123456789012"))
    print(num2kansuji("1234567890123456789012345678901234567890123456789012345678901234567890123"))
    print(num2kansuji("12"))
    print(num2kansuji("12."))
    print(num2kansuji("12.345"))
    print(num2kansuji(".345"))
    print(num2kansuji("3.141592"))

    print( "----------" )
    print(num2kansuji("100010001000", mode='replace'))
    print(num2kansuji("100011001000", mode='replace'))
    print(num2kansuji("1020304050607080", mode='replace'))
    print(num2kansuji("12345678901234567890123456789012345678901234567890123456789012345678901", mode='replace'))

    print( "----------" )
    print(numeric2kanji("<BOS>金額は1234567円です<EOS>"))
    print(numeric2kanji("１２３４５６は３４.５で、さらに0.１２３４５になります。0.1.2.3.4."))
    print(numeric2kanji("1000000円、10000000円、100000000円、1000円、100000000000円"))
