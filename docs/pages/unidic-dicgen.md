# Dictionary generation for UniDic users
WARNING: _This section takes several hours or days._

## Prepare the base dictionary
### git clone NEologd
First, download the NEologd dictionary as follows.

```sh
WORKDIR=/path/to/your/work/dir
cd $WORKDIR # move to the working directory
git clone --depth 1 https://github.com/neologd/mecab-unidic-neologd/
```

### Extract the NEologd vocabulary file and apply a patch

Then, extract the csv file of NEologd dictionary using `unxz` command.

```sh
# if your system has the unxz command
unxz -k `ls mecab-unidic-neologd/seed/*.xz | tail -n 1`
# otherwise
docker run -v $(pwd):/root/workspace tdmelodic:latest \
    unxz -k `ls mecab-unidic-neologd/seed/*.xz | tail -n 1`
```

This will generate a CSV file named `mecab-unidic-user-dict-seed.yyyymmdd.csv`.
Then, apply the patch to the NEologd dictionary which we have just extracted, as follows.
This creates a dictionary file `neologd_modified.csv` in the `/tmp` directory of the docker instance.

```sh
docker run -v $(pwd):/root/workspace tdmelodic:latest \
    tdmelodic-neologd-patch \
    --input `ls mecab-unidic-neologd/seed/mecab-unidic-user-dict-seed*.csv | tail -n 1` \
    --output /tmp/neologd_modified.csv
```

## Inference

_WARNING! THIS TAKES MUCH TIME!_
(FYI: It took about 2.5 hours in a MacBookPro, 5 hours in our Linux server.)

Now let generate the accent dictionary.
It estimates the accent of the words listed in NEologd dictionary
by a machine learning -based technique.

```sh
docker run -v $(pwd):/root/workspace tdmelodic:latest \
    tdmelodic-convert \
    -m unidic \
    --input /tmp/neologd_modified.csv \
    --output ${WORKDIR}/tdmelodic_original.csv
cp ${WORKDIR}/tdmelodic_original.csv ${WORKDIR}/tdmelodic.csv # backup
```

## Postprocess

Unigram costs can be fixed using the following script.
```sh
cp ${WORKDIR}/tdmelodic.csv ${WORKDIR}/tdmelodic.csv.bak
docker run -v $(pwd):/root/workspace tdmelodic:latest \
    tdmelodic-modify-unigram-cost \
    -i tdmelodic.csv.bak \
    -o tdmelodic.csv
```
