import unittest
from unittest import TestCase
from tdmelodic.util.word_type import WordType as W

class TestWordType(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestWordType, self).__init__(*args, **kwargs)
        self.w = W()

    def test_is_symbol(self):
        f = self.w.is_symbol
        self.assertEqual(True, f(",,,,記号,一般,,,,".split(",")))
        self.assertEqual(False, f(",,,,記号,,,,,".split(",")))

    def test_is_hashtag(self):
        f = self.w.is_hashtag
        self.assertEqual(True, f("#hello,,,".split(",")))
        self.assertEqual(True, f("#hello world,,,".split(",")))
        self.assertEqual(True, f("#こんにちは12345,,,".split(",")))
        self.assertEqual(False, f("＃hello world,,,".split(",")))

    def test_is_emoji(self):
        f = self.w.is_emoji
        self.assertEqual(True, f("😄,,,".split(",")))
        self.assertEqual(False, f("あ,,,".split(",")))

    def test_is_noisy_katakana(self):
        f = self.w.is_noisy_katakana
        self.assertEqual(True, f("カタカナ,,,,,,,,,,,片仮名,".split(",")))
        self.assertEqual(True, f("カタカナ,,,,,,,,,,,かたかな,".split(",")))
        self.assertEqual(False, f("カタカナ,,,,,,,,,,,カタカナ,".split(",")))
        self.assertEqual(True, f("トウキョウトチジセンキョ,,,,,,,,,,,東京都知事選挙,".split(",")))

    def test_is_katakana(self):
        f = self.w.is_katakana
        self.assertEqual(True, f("カタカナ,,,,,,,,,,,カタカナ,".split(",")))
        self.assertEqual(False, f("カタカナ,,,,,,,,,,,片仮名,".split(",")))
        self.assertEqual(False, f("ひらがな,,,,,,,,,,,平仮名,,,".split(",")))
        self.assertEqual(False, f("漢字,,,,,,,,,,,漢字,,".split(",")))
        self.assertEqual(False, f("漢字カタカナ,,,,,,,,,,,漢字片仮名,,,".split(",")))

    def test_is_hira_kata_kanji(self):
        f = self.w.is_hira_kata_kanji
        self.assertEqual(True, f("カタカナ,,,,,,,,,,,,".split(",")))
        self.assertEqual(True, f("カタカナ,,,,,,,,,,,,".split(",")))
        self.assertEqual(True, f("ひらがな,,,,,,,,,,,,,,".split(",")))
        self.assertEqual(True, f("漢字,,,,,,,,,,,,,".split(",")))
        self.assertEqual(True, f("漢字ひらがなカタカナ,,,,,,,,,,,,,,".split(",")))
        self.assertEqual(True, f("漢字＝カタカナ＆ひらがな,,,,,,,,,,,,,,".split(",")))
        self.assertEqual(False, f("カタカナabc,,,,,,,,,,,,".split(",")))

    def test_is_hira_kata_kanji_romaji(self):
        f = self.w.is_hira_kata_kanji_romaji
        self.assertEqual(True, f("カタカナ,,,,,,,,,,,,".split(",")))
        self.assertEqual(True, f("カタカナ,,,,,,,,,,,,".split(",")))
        self.assertEqual(True, f("ひらがな,,,,,,,,,,,,,,".split(",")))
        self.assertEqual(True, f("漢字,,,,,,,,,,,,,".split(",")))
        self.assertEqual(True, f("漢字ひらがなカタカナ,,,,,,,,,,,,,,".split(",")))
        self.assertEqual(True, f("漢字＝カタカナ＆ひらがな,,,,,,,,,,,,,,".split(",")))
        self.assertEqual(True, f("カタカナabc,,,,,,,,,,,,".split(",")))

    def test_is_romaji(self):
        f = self.w.is_romaji
        self.assertEqual(True, f("this is an apple,,,,,,,,,,,,".split(",")))
        self.assertEqual(True, f("A&B&C,,,,,,,,,,,,".split(",")))
        self.assertEqual(True, f("A-B-C,,,,,,,,,,,,,,".split(",")))
        self.assertEqual(False, f("カタカナabc,,,,,,,,,,,,".split(",")))

    def test_is_KK(self):
        f = self.w.is_KK
        self.assertEqual(True, f("株式会社あああああ,,,,,,,,,,,,,カブシキガイシャアアアアア,".split(",")))
        self.assertEqual(True, f("株式会社あああああ,,,,,,,,,,,,,カブシキカイシャアアアアア,".split(",")))
        self.assertEqual(True, f("あああああ株式会社,,,,,,,,,,,,,アアアアアカブシキガイシャ,".split(",")))
        self.assertEqual(True, f("あああああ株式会社,,,,,,,,,,,,,アアアアアカブシキカイシャ,".split(",")))
        self.assertEqual(False, f("株式会社あああああ,,,,,,,,,,,,,アアアアア,".split(",")))

    def test_is_YK(self):
        f = self.w.is_YK
        self.assertEqual(True, f("有限会社あああああ,,,,,,,,,,,,,ユーゲンガイシャアアアアア,".split(",")))
        self.assertEqual(True, f("有限会社あああああ,,,,,,,,,,,,,ユーゲンカイシャアアアアア,".split(",")))
        self.assertEqual(True, f("有限会社あああああ,,,,,,,,,,,,,ユウゲンガイシャアアアアア,".split(",")))
        self.assertEqual(False, f("有限会社あああああ,,,,,,,,,,,,,アアアアア,".split(",")))

    def test_is_station(self):
        f = self.w.is_station
        self.assertEqual(True, f("東京駅,,".split(",")))
        self.assertEqual(False, f("東京駅前,,".split(",")))

    def test_is_road(self):
        f = self.w.is_road
        self.assertEqual(True, f("東京都道1号あああああ線,,".split(",")))
        self.assertEqual(False, f("東京都道1号あああああ,,".split(",")))

    def test_is_school(self):
        f = self.w.is_school
        self.assertEqual(True, f("あああ小学校,,".split(",")))
        self.assertEqual(True, f("いいい中学校,,".split(",")))
        self.assertEqual(True, f("ううう高等学校,,".split(",")))
        self.assertEqual(True, f("えええ高校,,".split(",")))
        self.assertEqual(True, f("おおお大学,,".split(",")))
        self.assertEqual(True, f("かかか専門学校,,".split(",")))

    def test_is_address(self):
        f = self.w.is_address
        self.assertEqual(True, f("東京都文京区本郷,,".split(",")))
        self.assertEqual(True, f("埼玉県さいたま市浦和区,,".split(",")))
        self.assertEqual(True, f("神奈川県横浜市西区,,".split(",")))
        self.assertEqual(True, f("東京都八王子市,,".split(",")))


    def test_is_date(self):
        f = self.w.is_date
        self.assertEqual(True, f("10月10日,,,,,,,,,,,,,ジュウガツトオカ,".split(",")))
        self.assertEqual(False, f("十月十日,,,,,,,,,,,,,ジュウガツトオカ,".split(",")))
        self.assertEqual(False, f("10月10日,,,,,,,,,,,,,トツキトオカ,".split(",")))
        self.assertEqual(True, f("2020-10-10,,,,,,,,,,,,,,".split(",")))

    def test_is_numeral(self):
        f = self.w.is_numeral
        self.assertEqual(True, f("1億5000万円,,,".split(",")))
        self.assertEqual(True, f("$4,,,".split(",")))
        self.assertEqual(True, f("50ドル,,,".split(",")))
        self.assertEqual(True, f("80kg,,,".split(",")))
        self.assertEqual(True, f("80W,,,".split(",")))
        self.assertEqual(True, f("1階建て,,,".split(",")))
        self.assertEqual(True, f("10両編成,,,".split(",")))
        self.assertEqual(True, f("123456あああ,,,".split(",")))

if __name__ == '__main__':
    unittest.main()