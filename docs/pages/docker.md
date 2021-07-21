# Build the Docker image

## Download codes and data

### Requirements
Please set up `git`, `docker` and `mecab` (such as `libmecab-dev`) on your UNIX-like system such as Ubuntu or MacOS.

### git clone
Create working directory and download the repositories.

```sh
WORKDIR=/path/to/your/work/dir
cd $WORKDIR
git clone --depth 1 https://github.com/PKSHATechnology-Research/tdmelodic
```

### Download the UniDic dictionary file

Download the UniDic file from [NINJAL](https://unidic.ninjal.ac.jp/).
Several versions have been published, but the version we need is `uniDic-mecab_kana-accent-2.1.2_src.zip`.

```sh
wget https://unidic.ninjal.ac.jp/unidic_archive/cwj/2.1.2/unidic-mecab_kana-accent-2.1.2_src.zip
cp unidic-mecab_kana-accent-2.1.2_src.zip ${WORKDIR}/tdmelodic
```

Note: **This file will be reused later.**
Please do not download the file more than once to avoid overloading the site you are downloading from.
It is recommended that you keep this file somewhere in your local file system.


## Docker build

Build the docker image using following commands.
It will take a few minutes.

```sh
cd ${WORKDIR}/tdmelodic
docker build -t tdmelodic:latest . # --no-cache
```

## Test some commands if needed
If needed, try following commands and check the results.

```console
you@machine:~$ docker run tdmelodic:latest /bin/bash -c "echo 深層学習 | mecab -d \`mecab-config --dicdir\`/unidic"
深層	シンソー	シンソウ	深層	名詞-普通名詞-一般			0
学習	ガクシュー	ガクシュウ	学習	名詞-普通名詞-サ変可能			0
EOS
```

```console
you@machine:~$ docker run -it tdmelodic:latest
root@docker:~/workspace$ echo 深層学習 | mecab -d `mecab-config --dicdir`/unidic
深層	シンソー	シンソウ	深層	名詞-普通名詞-一般			0
学習	ガクシュー	ガクシュウ	学習	名詞-普通名詞-サ変可能			0
EOS

root@docker:~/workspace$ python3

>>> from tdmelodic.nn.lang.mecab.unidic import UniDic

>>> u = UniDic()
[ MeCab setting ] unidic='/usr/lib/x86_64-linux-gnu/mecab/dic/unidic'
[ MeCab setting ] mecabrc='/usr/local/lib/python3.8/dist-packages/tdmelodic/nn/lang/mecab/my_mecabrc'

>>> u.get_n_best("深層学習", "しんそうがくしゅう", 3)
 ([[{'surface': '深層', 'pron': 'シンソー', 'kana': 'シンソウ', 'pos': '名詞-普通名詞-一般', 'goshu': '漢', 'acc': '0', 'concat': 'C2'}, {'surface': '学習', 'pron': 'ガクシュー', 'kana': 'ガクシュウ', 'pos': '名詞-普通名詞-サ変可能', 'goshu': '漢', 'acc': '0', 'concat': 'C2'}], [{'surface': '深', 'pron': 'シン', 'kana': 'シン', 'pos': '接頭辞', 'goshu': '漢', 'acc': '', 'concat': 'P2'}, {'surface': '層', 'pron': 'ソー', 'kana': 'ソウ', 'pos': '名詞-普通名詞-一般', 'goshu': '漢', 'acc': '1', 'concat': 'C3'}, {'surface': '学習', 'pron': 'ガクシュー', 'kana': 'ガクシュウ', 'pos': '名詞-普通名詞-サ変可能', 'goshu': '漢', 'acc': '0', 'concat': 'C2'}], [{'surface': '深', 'pron': 'フカ', 'kana': 'フカイ', 'pos': '形容詞-一般', 'goshu': '和', 'acc': '2', 'concat': 'C1'}, {'surface': '層', 'pron': 'ソー', 'kana': 'ソウ', 'pos': '名詞-普通名詞-一般', 'goshu': '漢', 'acc': '1', 'concat': 'C3'}, {'surface': '学習', 'pron': 'ガクシュー', 'kana': 'ガクシュウ', 'pos': '名詞-普通名詞-サ変可能', 'goshu': '漢', 'acc': '0', 'concat': 'C2'}]], [0, 1, 2], 9)

>>> Ctrl-D

root@docker:~/workspace$ exit
you@machine:~$
```
