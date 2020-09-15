pos_short_interm = {
        None:'0',
        '名詞-普通名詞-一般':'n',
        '名詞-普通名詞-サ変可能':'n',
        '名詞-普通名詞-形状詞可能':'n',
        '名詞-普通名詞-サ変形状詞可能':'n',
        '名詞-普通名詞-副詞可能':'n',
        '名詞-固有名詞-一般':'K',
        '名詞-固有名詞-人名-一般':'K',
        '名詞-固有名詞-人名-姓':'S',
        '名詞-固有名詞-人名-名':'M',
        '名詞-固有名詞-地名-一般':'K',
        '名詞-固有名詞-地名-国':'K',
        '名詞-固有名詞-組織名':'K',
        '名詞-数詞':'#',
        '名詞-助動詞語幹':'n',
        '代名詞':'n',
        '形状詞-一般':'n',
        '形状詞-タリ':'n',
        '形状詞-助動詞語幹':'n',
        '連体詞':'n',
        '副詞':'d',
        '接続詞':'d',
        '感動詞-一般':'d',
        '感動詞-フィラー':'d',
        '動詞-一般':'d',
        '動詞-非自立可能':'d',
        '形容詞-一般':'d',
        '形容詞-非自立可能':'d',
        '助動詞':'+',
        '助詞-格助詞':'+',
        '助詞-副助詞':'+',
        '助詞-係助詞':'+',
        '助詞-接続助詞':'+',
        '助詞-終助詞':'+',
        '助詞-準体助詞':'+',
        '接頭辞':'n',
        '接尾辞-名詞的-一般':'n',
        '接尾辞-名詞的-サ変可能':'n',
        '接尾辞-名詞的-形状詞可能':'n',
        '接尾辞-名詞的-副詞可能':'n',
        '接尾辞-名詞的-助数詞':'n',
        '接尾辞-形状詞的':'n',
        '接尾辞-動詞的':'n',
        '接尾辞-形容詞的':'n',
        '記号-一般':'@',
        '記号-文字':'@',
        '補助記号-一般':'@',
        '補助記号-句点':'@',
        '補助記号-読点':'@',
        '補助記号-括弧開':'@',
        '補助記号-括弧閉':'@',
        '空白':'0'
}


def revdic(x):
    revdict = {}
    for k, v in x.items():
        revdict.setdefault(v, []).append(k)
    return revdict

pos_short_interm_inv = revdic(pos_short_interm)

pos_short_ids = list(sorted(set(pos_short_interm.values())))
pos_short_ids = ['0'] + [p for p in pos_short_ids if p is not '0']
pos_short_ids = {v : i for i, v in enumerate(pos_short_ids)}
pos_map = {k: pos_short_ids[v] for k, v in pos_short_interm.items()}
pos_invmap = {v:pos_short_interm[k] for k, v in pos_map.items()}

if __name__ == '__main__':
    from pprint import pprint
    pprint(pos_short_interm_inv)
    pprint(pos_short_ids)
    pprint(pos_map)
    pprint(pos_invmap)
