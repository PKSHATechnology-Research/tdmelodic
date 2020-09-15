# -----------------------------------------------------------------------------
# Copyright (c) 2019-, PKSHA Technology Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# -----------------------------------------------------------------------------

accent_map ={
# Note!!
# low/high code:
    '.':0,
    'L':1,
    'H':2,
    '?':3,
# up/down code:
#     0:down
#     1:keep
#     2:up
# These codes below are also hard coded in accent_diff.py
    '-':0, # keep
    'D':1, # down
    'U':2, # up
# See also data_loader.py, convert_dic.py.
}
accent_invmap = {v: i for i, v in accent_map.items()}

def accent_align(roman, a_kernel):
    """
    ローマ字とアクセント核を入力として、L/H方式のアクセント情報を出力する。
    roman: 他のモジュールにおいて既に1モーラ2文字に変換されていることを想定。
    a_kernel: アクセント核位置
    """
    n_morae = len(roman) // 2
    r = 2 # 2文字で1モーラなので、長さを2倍にする。
    try:
        a_kernel = int(a_kernel.split(",")[0]) # 複数書いてある場合は最初のものを優先して採用する。
        if a_kernel == 0:
            accent = 'L' * r + 'H' * n_morae * r
            return accent
        elif a_kernel == 1:
            accent = 'H' * r + 'L' * n_morae * r
            return accent
        elif 2 <= a_kernel and a_kernel <= n_morae:
            accent = 'L' * r + 'H' * (a_kernel - 1) * r + 'L' * (n_morae + 1 - a_kernel) * r
            return accent
        elif a_kernel == n_morae + 1:
            accent = 'L' * r + 'H' * (a_kernel - 1) * r + 'L' * (n_morae + 1 - a_kernel) * r
            return accent
        else:
            accent = "." * (n_morae + 1) * r
            return accent

    except Exception as e:
        if a_kernel is '*':
            accent = "?" * (n_morae + 1) * r
            return accent
        else:
            accent = "." * (n_morae + 1) * r
            return accent

if __name__ == '__main__':
    txt = "rixngo"
    a = accent_align(txt, 0)
    print(txt)
    print(a)

    txt = "mikaxn"
    a = accent_align(txt, 1)
    print(txt)
    print(a)

    txt = "paxinaqqpuru"
    a = accent_align(txt, 3)
    print(txt)
    print(a)
