import Levenshtein
import romkan
import jaconv
from tdmelodic.nn.lang.mecab.unidic import UniDic

class YomiEvaluator():
    def __init__(self, rank_weight = 0.1, romaji_priority=2, nbest=10):
        self.unidic = UniDic()
        self.romaji_priority=romaji_priority
        self.nbest = nbest
        self.rank_weight = rank_weight

    def eval(self, *args, **kwargs):
        distance1 = self.eval_normal(*args, **kwargs)
        distance2 = self.eval_force_romaji_to_kana(*args, **kwargs)
        distance2 -= self.romaji_priority
        return min(distance1, distance2)

    def eval_normal(self, text, kana_ref, nbest=20):
        '''一番読みが近いものとの距離を評価して返す。順位も考慮に入れる。'''
        text = jaconv.h2z(text, digit=True, ascii=True, kana=True) # zenkaku
        p = self.unidic._UniDic__parse(text, nbest=self.nbest)
        kanas = ["".join([
                        e["pron"] for e in p_
                    ]) for p_ in p]
        dist = [self.rank_weight * rank +
                    Levenshtein.distance(k, kana_ref)
                        for rank, k in enumerate(kanas)]
        rank = [i for i, v in sorted(
                                enumerate(dist),
                                key=lambda v: v[1])]
        ld = dist[rank[0]]
        return ld

    def eval_force_romaji_to_kana(self, text, kana_ref, nbest=20):
        """アルファベットをローマ字読みできそうな箇所を無理やり仮名に変換してからさらにUniDicで分析してより良い読みを探る。"""
        p_ = jaconv.z2h(text, digit=True, ascii=True, kana=False) # hankaku
        p = romkan.to_katakana(p_) # romanize as possible
        if p_ == p: # 変化がないものは以下の処理を行わずに戻る。戻り値は十分大きければなんでも良い。
            return 12345
        return self.eval_normal(p, kana_ref, nbest)
