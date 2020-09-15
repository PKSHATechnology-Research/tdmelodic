# -----------------------------------------------------------------------------
# Copyright (c) 2019-, PKSHA Technology Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# -----------------------------------------------------------------------------

# 仮名をローマ字（1モーラが2文字になるようにした独自表現）に変換するための辞書
# これらのマッピングは、モーラ分割後に各モーラに適用する。

kana2roman_alias = {
    "ァ":"xa",
    "ィ":"xi",
    "ゥ":"xu",
    "ェ":"xe",
    "ォ":"xo",
    "ぁ":"xa",
    "ぃ":"xi",
    "ぅ":"xu",
    "ぇ":"xe",
    "ぉ":"xo",

    "ゐ":"wi",
    "ゑ":"we",

# 合拗音
    "クヮ":"ka",
    "グヮ":"ga",

# 濁音
    "ヂャ":"ja",
    "ヂュ":"ju",
    "ヂェ":"je",
    "ヂョ":"jo",

# 促音
    "っ":"QQ",
}

kana2roman_standard = {
# 直音・清音
    "ア":"xa",
    "イ":"xi",
    "ウ":"xu",
    "エ":"xe",
    "オ":"xo",

    "カ":"ka",
    "キ":"ki",
    "ク":"ku",
    "ケ":"ke",
    "コ":"ko",

    "サ":"sa",
    "シ":"Si",
    "ス":"su",
    "セ":"se",
    "ソ":"so",
    "スィ":"si",

    "タ":"ta",
    "チ":"Ci",
    "ツ":"Zu",
    "テ":"te",
    "ト":"to",
    "ティ":"ti",
    "トゥ":"tu",

    "ナ":"na",
    "ニ":"ni",
    "ヌ":"nu",
    "ネ":"ne",
    "ノ":"no",

    "ハ":"ha",
    "ヒ":"hi",
    "フ":"fu",
    "ヘ":"he",
    "ホ":"ho",

    "マ":"ma",
    "ミ":"mi",
    "ム":"mu",
    "メ":"me",
    "モ":"mo",

    "ヤ":"xA",
    "ユ":"xU",
    "ヨ":"xO",
    "イェ":"xE",

    "ラ":"ra",
    "リ":"ri",
    "ル":"ru",
    "レ":"re",
    "ロ":"ro",

    "ワ":"wa",
    "ヰ":"wi",
    "ヱ":"we",
    "ヲ":"wo",
    "ウィ":"wi",
    "ウェ":"we",
    "ウォ":"wo",

# 濁音・半濁音
    "ガ":"ga",
    "ギ":"gi",
    "グ":"gu",
    "ゲ":"ge",
    "ゴ":"go",

    "ザ":"za",
    "ジ":"ji",
    "ズ":"zu",
    "ゼ":"ze",
    "ゾ":"zo",
    "ズィ":"zi",

    "ダ":"da",
    "ヂ":"ji",
    "ヅ":"zu",
    "デ":"de",
    "ド":"do",
    "ディ":"di",
    "ドゥ":"du",

    "バ":"ba",
    "ビ":"bi",
    "ブ":"bu",
    "ベ":"be",
    "ボ":"bo",

    "パ":"pa",
    "ピ":"pi",
    "プ":"pu",
    "ペ":"pe",
    "ポ":"po",

    "ヴァ":"va",
    "ヴィ":"vi",
    "ヴ": "vu",
    "ヴェ":"ve",
    "ヴォ":"vo",

# 開拗音
    "キャ":"kA",
    "キュ":"kU",
    "キェ":"kE",
    "キョ":"kO",

    "テャ":"tA",
    "テュ":"tU",
    "テェ":"tE",
    "テョ":"tO",

    "ニャ":"nA",
    "ニュ":"nU",
    "ニェ":"nE",
    "ニョ":"nO",

    "ヒャ":"hA",
    "ヒュ":"hU",
    "ヒェ":"hE",
    "ヒョ":"hO",

    "ミャ":"mA",
    "ミュ":"mU",
    "ミェ":"mE",
    "ミョ":"mO",

    "リャ":"rA",
    "リュ":"rU",
    "リェ":"rE",
    "リョ":"rO",

    "ギャ":"gA",
    "ギュ":"gU",
    "ギェ":"gE",
    "ギョ":"gO",

    "ズャ":"zA",
    "ズュ":"zU",
    "ズェ":"zE",
    "ズョ":"zO",

    "デャ":"dA",
    "デュ":"dU",
    "デェ":"dE",
    "デョ":"dO",

    "ビャ":"bA",
    "ビュ":"bU",
    "ビェ":"bE",
    "ビョ":"bO",

    "ピャ":"pA",
    "ピュ":"pU",
    "ピェ":"pE",
    "ピョ":"pO",

    "ツャ":"ZA",
    "ツュ":"ZU",
    "ツョ":"ZO",

    "フャ":"fA",
    "フュ":"fU",
    "フョ":"fO",

    "ヴャ":"vA",
    "ヴュ":"vU",
    "ヴョ":"vO",

# その他拗音
    "シャ":"Sa",
    "シュ":"Su",
    "シェ":"Se",
    "ショ":"So",

    "チャ":"Ca",
    "チュ":"Cu",
    "チェ":"Ce",
    "チョ":"Co",

    "ツァ":"Za",
    "ツィ":"Zi",
    "ツェ":"Ze",
    "ツォ":"Zo",

    "ファ":"fa",
    "フィ":"fi",
    "フェ":"fe",
    "フォ":"fo",

    "ジャ":"ja",
    "ジュ":"ju",
    "ジェ":"je",
    "ジョ":"jo",

# 撥音と促音
    "ン":"xn",
    "ッ":"QQ",

# 句読点など
    "。":".",
    "。":".",
    "。":".",
    ".":".",

    "．":".",
    "、":",",
    "，":",",
    ",":",",

    "?":"?",
    "？":"?",

    "!":"!",
    "！":"!",
    "♪":"!",

# 括弧
    "「":"(",
    "」":")",

    "【":"(",
    "】":")",

    "『":"(",
    "』":")",

    "（":"(",
    "）":")",

    "(":"(",
    ")":")",

    "<":"<",
    ">":">",

# 空白
    " ":" ",
    "　":" ",

# 伸ばし棒、点
    "—":"-",
    "ー":"-",

    "~":"~",
    "〜":"~",
    "～":"~",

    "…":":",
    ":":":",
    "・":",",

# 例外記号
    "0" : "##",
}

# ===========================================================================================
# 辞書結合
kana2roman_dictionary = {**kana2roman_standard, **kana2roman_alias}

# 1文字のコードを2文字にする。
kana2roman_dictionary = {k: (v * 2)[:2] for k, v in kana2roman_dictionary.items()}

# invmap 本当はこれでは正しくないが、学習中の参考情報としてしか使わないのでとりあえずこれで良い。
kana2roman_dictionary_inv = {v: k for k, v in kana2roman_standard.items()}
kana2roman_dictionary_inv["  "] = "＿"

# 2文字で1モーラになるもののリスト
exceptions = {k: v for k, v in kana2roman_dictionary.items() if len(k) == 2}

# 子音と母音のリスト
consonants = list(sorted(set([code[0] for code in kana2roman_dictionary.values()])))
vowels     = list(sorted(set([code[1] for code in kana2roman_dictionary.values()])))

# 子音と母音のエンコード
roman_map = {v: i+1 for i, v in enumerate(list(sorted(set(consonants + vowels))))}
roman_map[None] = 0
roman_map["0"] = 0
roman_map[""] = 0
roman_invmap = {v: k for k, v in roman_map.items()}

if __name__ == '__main__':
    print(sorted([(k, v) for k, v in kana2roman_dictionary.items()], key=lambda _: _[0]))

    print("-"*80)
    print(sorted([(k, v) for k, v in exceptions.items()], key=lambda _: _[0]))

    print("-"*80)
    print("consonants",consonants)

    print("-"*80)
    print("vowels",vowels)

    print("-"*80)
    print(roman_map)

    print("-"*80)
    print(roman_invmap)
