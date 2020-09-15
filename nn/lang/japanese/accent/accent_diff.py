# -----------------------------------------------------------------------------
# Copyright (c) 2019-, PKSHA Technology Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# -----------------------------------------------------------------------------

def simple_accent_diff(a):
    '''
    L/H方式のアクセント情報を入力として、up/down方式のアクセント情報を出力する。
    '''
    if len(a) == 1:
        return "."
    a_ = a.replace(".", "0").replace("?", "0").replace("H", "1").replace("L", "0")
    diff = [int(n) - int(p) for n, p in zip(a_[1:], a_[:-1])]

    # 1モーラ目のup (+1) は情報量がないので（ほぼ無意味な情報なので）消す。down(-1)は重要なので残す。
    # Ignore the 'up' (+1) after the first mora, because it has almost no information.
    # Every word except 'type-1 accent' words ('down' after the first mora) raise the pitch first.
    diff[0] = 0 if diff[0] == 1 else diff[0]

    diff = ["-" if d == 0 else
            "U" if d == 1 else
            "D" if d == -1 else
            "?" for d in diff]
    diff="".join(diff) + "."
    return diff

if __name__ == '__main__':
    def test(a):
        print(a)
        d = simple_accent_diff(a)
        print(d)
        print("")

    test("LHHHHLLLL")
    test("LHHLLLHHLLL")
    test("HLLLLLHHHHLLLLLLHHHLLHLHLHLHL")
    test("LHLHLHLHL")
