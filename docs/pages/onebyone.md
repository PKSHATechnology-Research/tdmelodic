# One-by-one Manual Inference Mode

In some cases, you may want to estimate the accent for one word,
rather than the entire dictionary at once.
This page introduces the tools for this purpose.

## s2ya: Surface -> Yomi & Accent

`s2ya` estimates the reading (`yomi`) and accent of a word from its orthographic form (`surface`).
For yomi, it uses the best estimates from MeCab and UniDic.

- Input: Orthographic (surface) form, such as kanji
- Output: Reading (yomi) and Accent

```sh
$ echo 機械学習 | docker run tdmelodic:latest tdmelodic-s2ya
```
Then you will have the following result.
```
キ[カイガ]クシュー
```

It is convenient to define an alias command as follows.
```sh
alias tdmelodic-s2ya=docker run tdmelodic:latest tdmelodic-s2ya
```
Using this, try other examples.
```sh
$ echo 深層学習 | tdmelodic-s2ya
シ[ンソーガ]クシュー

$ echo 確率微分方程式 | tdmelodic-s2ya
カ[クリツビブンホーテ]ーシキ

$ echo 電験一種 | tdmelodic-s2ya
デ[ンケンイ]ッシュ

$ echo マルクス・アウレリウス・アントニヌス | tdmelodic-s2ya
マ[ルクスアウレリウスアントニ]ヌス

$ echo IoT | tdmelodic-s2ya
ア[イオーティ]ー
```

It also predicts the accents of sentences.
```sh
$ echo 今日の東京の天気は晴れ | tdmelodic-s2ya
キョ]ーノト[ーキョーノテ]ンキワハレ

$ echo 漢字の音読みには主に呉音と漢音があり、漢音の方が新しい。 | tdmelodic-s2ya
カ[ンジノオンヨミニ]ワオ]モニゴ[オントカ]ンオンガアリ[カ]ンオンノホ]ーガアタラシ]ー

$ echo 現在、西新宿ジャンクションから談合坂サービスエリアまで、およそ四十五分 | tdmelodic-s2ya
ゲ]ンザイニ[シシンジュクジャ]ンクションカラダ[ンゴーサカサ[ービスエ]リアマ]デ]オ[ヨソヨ]ンジュー[ゴ]フン

$ echo 完備なノルム空間をバナッハ空間といい、完備な内積空間をヒルベルト空間という。 | tdmelodic-s2ya
カ]ンビナノ[ルムク]ーカンオバ[ナッハク]ーカントイーカ]ンビナナ[イセキク]ーカンオヒ[ルベルトク]ーカントイウ

$ echo 権利の行使及び義務の履行は、信義に従い誠実に行わなければならない。 | tdmelodic-s2ya
ケ]ンリノコ]ーシオヨビギ]ムノリコーワ[シ]ンギニシ[タガイセージツニオコナワナ]ケレ]バナラナイ
```

## sy2a: Surface & Yomi -> Accent

`sy2a` estimates the accent of a word from its orthographic form (`surface`) and the reading (`yomi`).

- Input: Orthographic (surface) form, such as kanji, and reading (yomi).
- Output: Accent

For example,
```sh
$ alias tdmelodic-sy2a=docker run -v tdmelodic:latest tdmelodic-sy2a
$ echo 機械学習,きかいがくしゅー | tdmelodic-sy2a
キ[カイガ]クシュー
```

Try other examples.
```sh
$ echo 日本語アクセント,にほんごあくせんと | tdmelodic-sy2a
ニ[ホンゴア]クセント

$ echo 御御御付け,おみおつけ | tdmelodic-sy2a
オ[ミオ]ツケ

$ echo 談合坂SA,だんごーざかさーびすえりあ | tdmelodic-sy2a
ダ[ンゴーザカサービスエ]リア
```

It can also predict the accents of sentences.
```sh
$ echo Wifiに接続できません,わいふぁいにせつぞくできません | tdmelodic-sy2a
ワ[イファイニセ[ツゾクデキマセ]ン

$ echo 国立市の国立大学,くにたちしのこくりつだいがく | tdmelodic-sy2a
ク[ニタチ]シノコ[クリツダ]イガク

$ echo 漢音は、当時の唐の都、長安の音を持ち帰ったものである。,かんおんわとーじのとーのみやこちょーあんのおとおもちかえったものである | tdmelodic-sy2a
カ]ンオンワ[ト]ージノト]ーノミ[ヤコ[チョ]ーアンノオ[ト]オモ[チカエッタモノ]デア]ル
```
