
from dataclasses import dataclass
#from .lang.japanese.kana.mora_sep import sep_katakana2mora
from tdmelodic.nn.lang.mecab.unidic import UniDic

@dataclass
class Word(object):
    surf: str
    yomi: str
    pos: str

class Alignment(object):
    # TODO
    def __init__(self):
        pass

    def __call__(self, x_yomi, lst_y_yomi, y_mask):
        y_idx = sum([[idx] * len(y_) for idx, y_ in enumerate(lst_y_yomi)], [])
        y_yomi = "".join(lst_y_yomi)
        print(y_idx, y_yomi)

class DetectWrongParticle(object):
    def __init__(self):
        self.unidic = UniDic()
        self.special_particles = [
            Word("は", "ワ", "助詞"),
            Word("へ", "エ", "助詞"),
            # Word("を", "オ", "助詞")
        ]

    def parse(self, surf):
        """ parse text and return the words and the flags (whether it is a special particle or not) """
        parsed = self.unidic._UniDic__parse(surf)[0]
        words = [Word(word["surface"], word["pron"], word["pos"].split("-")[0]) for word in parsed]
        masks = [w in self.special_particles for w in words]
        return words, masks

    def has_special_particles(self, surf):
        """ check if the text has special particles は, へ or not"""
        words, masks = self.parse(surf)
        return any(masks)


class ParticleYomi(object):
    """
    neologdの読みは　ワガハイ【ハ】ネコデアル　のように助詞「は」「へ」の読みが適切に処理されていないケースがあるので削除する。
    TODO : 削除ではなく修正するようにする
    """
    def __init__(self):
        self.detector = DetectWrongParticle()

    def __call__(self, line, IDX_MAP):
        if self.detector.has_special_particles(line[IDX_MAP["SURFACE"]]):
            return None
        else:
            return line

if __name__ == '__main__':
    a = Alignment()
    a("あああああ", ["あああ", "いい", "うううううううう"], None)

    txt = "今日はいい天気ですね。犬を連れてどこへ行きましょうか。"
    d = DetectWrongParticle()
    a = d.parse(txt)
    print(a)
    a = d.has_special_particles(txt)
    print (a)
