
import sys
import csv
import shutil
import regex as re
from .dic_index_map import get_dictionary_index_map

class WordType(object):
    def __init__(self):
        self.map = get_dictionary_index_map("unidic")

    def is_symbol(self, line):
        flag1 = re.search(r"^記号$", line[self.map["POS1"]], flags=0)
        flag2 = re.search(r"^一般$", line[self.map["POS2"]], flags=0)
        return all([flag1, flag2])

    def is_hashtag(self, line):
        """ extract hash tags"""
        flag1 = re.search(r"^\#.+$", line[self.map["SURFACE"]], flags=0)
        return all([flag1])

    def is_emoji(self, line):
        """ extract emojis """
        flag1 = re.search(u"[\U0001F1E6-\U0001F645]+", line[self.map["SURFACE"]], flags=0)
        return all([flag1])

    def is_noisy_katakana(self, line):
        """ extract word such that the surface form is katakana but the lemma form contains kanji or hiragana """
        flag1 = re.search(r"^[\p{Han}\p{Hiragana}a-zA-Z0-9]+$", line[self.map["LEMMA"]], flags=0)
        flag2 = re.search(r"^[\p{Katakana}・&＆!！ー＝\s　]+$", line[self.map["SURFACE"]], flags=0)
        return all([flag1, flag2])

    def is_katakana(self, line):
        flag1 = re.search(r"^[\p{Katakana}・&＆!！ー＝\s　]+$", line[self.map["LEMMA"]], flags=0)
        flag2 = re.search(r"^[\p{Katakana}・&＆!！ー＝\s　]+$", line[self.map["SURFACE"]], flags=0)
        return all([flag1, flag2])

    def is_hira_kata_kanji(self, line):
        flag1 = re.search(r"^[\p{Han}\p{Hiragana}\p{Katakana}・&＆!！ー＝\s　]+$", line[self.map["SURFACE"]], flags=0)
        return all([flag1])

    def is_romaji(self, line):
        flag1 = re.search(r"^[a-zA-Zａ-ｚＡ-Ｚ',，.!！\-&＆\s　]+$", line[self.map["SURFACE"]], flags=0)
        return all([flag1])

    def is_hira_kata_kanji_romaji(self, line):
        flag1 = re.search(r"^[a-zA-Zａ-ｚＡ-Ｚ',.!！\-&＆\s　\p{Han}\p{Hiragana}\p{Katakana}ー＝]+$", line[self.map["SURFACE"]], flags=0)
        return all([flag1])

    def is_KK(self, line):
        """ extract KK (kabushiki gaisha) """
        flag1 = re.search("カブシキ[ガ|カ]イシャ", line[self.map["YOMI"]], flags=0)
        return all([flag1])

    def is_YK(self, line):
        """ extract YK (yugen gaisha) """
        flag1 = re.search("ユ[ウ|ー]ゲン[ガ|カ]イシャ", line[self.map["YOMI"]], flags=0)
        return all([flag1])

    def is_station(self, line):
        """ extract station """
        flag1 = re.search(r".+駅$", line[self.map["SURFACE"]], flags=0)
        return all([flag1])

    def is_road(self, line):
        """ extract station """
        flag1 = re.search(r"^\p{Han}+道.*\d号.+線$", line[self.map["SURFACE"]], flags=0)
        return all([flag1])

    def is_school(self, line):
        """ extract schools """
        flag1 = re.search(r"^[\p{Han}\p{Katakana}\p{Hiragana}ー・]+[小|中|高等]+学校$", line[self.map["SURFACE"]], flags=0)
        flag2 = re.search(r"^[\p{Han}\p{Katakana}\p{Hiragana}ー・]+[大学|高校]$", line[self.map["SURFACE"]], flags=0)
        flag3 = re.search(r"^[\p{Han}\p{Katakana}\p{Hiragana}ー・]+専門学校$", line[self.map["SURFACE"]], flags=0)
        return any([flag1, flag2, flag3])

    def is_address(self, line):
        """ extract schools """
        flag1 = re.search(r"^.+[都道府県][^,]+[郡市区町村].*$", line[self.map["SURFACE"]], flags=0)
        return all([flag1])

    def is_placename(self, line):
        flag1 = re.search(r"^名詞$", line[self.map["POS1"]], flags=0)
        flag2 = re.search(r"^固有名詞$", line[self.map["POS2"]], flags=0)
        flag3 = re.search(r"^地名$", line[self.map["POS3"]], flags=0)
        return all([flag1, flag2, flag3])

    def is_person(self, line):
        flag1 = re.search(r"^名詞$", line[self.map["POS1"]], flags=0)
        flag2 = re.search(r"^固有名詞$", line[self.map["POS2"]], flags=0)
        flag3 = re.search(r"^人名$", line[self.map["POS3"]], flags=0)
        return all([flag1, flag2, flag3])

    def is_date(self, line):
        flag1 = re.search(r"^\d+月\d+日$", line[self.map["SURFACE"]], flags=0)
        flag2 = re.search(r"^.*ガツ.*$", line[self.map["YOMI"]], flags=0)
        flag3 = re.search(r"\d{4}-\d{2}-\d{2}$", line[self.map["SURFACE"]], flags=0)
        return any([all([flag1, flag2]), flag3])

    def is_JPY(self, line):
        flag1 = re.search(r"^\d+[万億兆京]*円$", line[self.map["SURFACE"]], flags=0)
        return all([flag1])

    def is_USD(self, line):
        flag1 = re.search(r"^\$\d+$", line[self.map["SURFACE"]], flags=0)
        flag2 = re.search(r"^\d+ドル$", line[self.map["SURFACE"]], flags=0)
        return any([flag1, flag2])

    def is_length(self, line):
        flag1 = re.search(r"^[.\d]+[kcm]*m$", line[self.map["SURFACE"]], flags=0)
        return all([flag1])

    def is_weight(self, line):
        flag1 = re.search(r"^[.\d]+[km]*g$", line[self.map["SURFACE"]], flags=0)
        flag2 = re.search(r"^[.\d]+t$", line[self.map["SURFACE"]], flags=0)
        return any([flag1, flag2])

    def is_electric_unit(self, line):
        flag1 = re.search(r"^[.\d]+m[aA]$", line[self.map["SURFACE"]], flags=0)
        flag2 = re.search(r"^[.\d]+[vV]$", line[self.map["SURFACE"]], flags=0)
        flag3 = re.search(r"^[.\d]+[wW]$", line[self.map["SURFACE"]], flags=0)
        return any([flag1, flag2, flag3])

    def is_mass(self, line):
        flag1 = re.search(r"^[.\d]+ml$", line[self.map["SURFACE"]], flags=0)
        return all([flag1])

    def is_temperature(self, line):
        flag1 = re.search(r"^[.\d]+度$", line[self.map["SURFACE"]], flags=0)
        return all([flag1])

    def is_pressure(self, line):
        flag1 = re.search(r"^[.\d]+hPa$", line[self.map["SURFACE"]], flags=0)
        return all([flag1])

    def is_ratio(self, line):
        flag1 = re.search(r"^[.\d]+\%$", line[self.map["SURFACE"]], flags=0)
        flag2 = re.search(r"^[.\d]+パーセント$", line[self.map["SURFACE"]], flags=0)
        flag3 = re.search(r"^[.\d]+倍$", line[self.map["SURFACE"]], flags=0)
        return any([flag1, flag2, flag3])

    def is_byte(self, line):
        flag1 = re.search(r"^[.\d]+[kKmMgGtT]B$", line[self.map["SURFACE"]], flags=0)
        return all([flag1])

    def is_number(self, line):
        flag1 = re.search(r"^-*[\d.]+$", line[self.map["SURFACE"]], flags=0)
        return all([flag1])

    def is_1char_unit_numeral(self,line):
        flag1 = re.search(r"^-*[\d.]+[階話色系種秒発番点歳枚杯本期曲日敗打才戦形巻基均回周勝分億傑件代人万部節時児月年条限位]+$", line[self.map["SURFACE"]], flags=0)
        flag2 = re.search(r"\d+[\p{Han}\p{Katakana}\p{Hiragana}]{1}$", line[self.map["SURFACE"]], flags=0)
        return any([flag1, flag2])

    def is_2char_unit_numeral(self,line):
        flag1 = re.search(r"^-*[\d.]+(部隊|連敗|連勝|試合|行目|秒間|杯目|期目|期生|時間|日間|打点|度目|年間|日目|週目|週間|年目|年後|年前|年代|学期|回目|周年|周目|列目|分間|円玉|円札|作品|代目|人月|人年|万人|キロ|か年|か月|世紀|丁目|連休|年度)+$", line[self.map["SURFACE"]], flags=0)
        flag2 = re.search(r"\d+[\p{Han}\p{Katakana}\p{Hiragana}]{2}$", line[self.map["SURFACE"]], flags=0)
        return any([flag1, flag2])

    def is_3char_unit_numeral(self,line):
        flag1 = re.search(r"^-*[\d.]+(か月目|か月間|インチ|カ月目|カ月間|セント|チャン|ユーロ|世紀間|両編成|年ぶり|年戦争|年連続|時間前|時間半|時間五|番人気|階建て|系電車)+$", line[self.map["SURFACE"]], flags=0)
        flag2 = re.search(r"\d+[\p{Han}\p{Katakana}\p{Hiragana}]{3}$", line[self.map["SURFACE"]], flags=0)
        return any([flag1, flag2])

    def is_numeral(self,line):
        return self.is_JPY(line) or \
            self.is_USD(line) or \
            self.is_length(line) or\
            self.is_weight(line) or \
            self.is_electric_unit(line) or \
            self.is_mass(line) or \
            self.is_temperature(line) or\
            self.is_pressure(line) or \
            self.is_ratio(line) or \
            self.is_byte(line) or \
            self.is_number(line) or \
            self.is_1char_unit_numeral(line) or \
            self.is_2char_unit_numeral(line) or \
            self.is_3char_unit_numeral(line)
