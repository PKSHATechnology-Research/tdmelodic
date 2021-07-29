import regex as re


def modify_longvowel_errors(line, idx_yomi=None):
    line[idx_yomi] = line[idx_yomi]\
        .replace("ーィ","ウィ")\
        .replace("ーェ","ウェ")\
        .replace("ーォ","ウォ")
    return line

def modify_yomi_of_numerals(line, idx_surface=None, idx_yomi=None):
    """
    数値の読みを簡易的に修正する（完全なものではない）
    """

    surface = line[idx_surface]
    # 1文字目が数字で2文字以上の長さがあるもの
    num=[str(i) for i in range(10)] + ['１','２','３','４','５','６','７','８','９','０']
    if (surface[0] in num) and len(line[1]) >= 2:
        pass
    else:
        # otherwise do nothing
        return line

    filters=[
        (r"ニ(テン\p{Katakana}+)", r"ニー\1" ),
        (r"ゴ(テン\p{Katakana}+)", r"ゴー\1" ),
        (r"ニ(イチ|ニ|サン|ヨン|ゴ|ロク|ナナ|ハチ|キュウ|キュー|レー|レイ|ゼロ)", r"ニー\1" ),
        (r"ゴ(イチ|ゴ|サン|ヨン|ゴ|ロク|ナナ|ハチ|キュウ|キュー|レー|レイ|ゼロ)", r"ゴー\1" ),
        (r"イチ(サ^ン|シ|ス|セ|ソ|タ|チ|ツ|テ|ト|カ|キ^ュ|ケ|コ|パ|ピ|プ|ペ|ポ)", r"イッ\1" ),
        (r"ハチ(サ^ン|シ|ス|セ|ソ|タ|チ|ツ|テ|ト|カ|キ^ュ|ケ|コ|パ|ピ|プ|ペ|ポ)", r"ハッ\1" ),
        (r"ジュウ(サ^ン|シ^チ|ス|セ|ソ|タ|チ|ツ|テ|ト|カ|キ^ュ|ケ|コ|パ|ピ|プ|ペ|ポ)", r"ジュッ\1" ),
        (r"ンエ", r"ンイェ" ), # 「万円」などを en -> yen
        (r"ヨンニチ", r"ヨッカ" ),
        (r"ニーニチ", r"ニニチ" ), # 12日など
        (r"ゴーニチ", r"ゴニチ" ) # 15日など
    ]
    yomi = line[idx_yomi]

    for regex1, regex2 in filters:
        prev_yomi = ''
        while prev_yomi != yomi: # 変化しなくなるまでループ
            prev_yomi = yomi
            if re.search(regex1, yomi):
                yomi = re.sub(regex1, regex2, yomi)

    line[idx_yomi] = yomi

    return line
