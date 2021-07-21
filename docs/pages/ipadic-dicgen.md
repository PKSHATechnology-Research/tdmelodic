# Dictionary Generation for IPADIC users
_UNDER CONSTRUCTION_

WARNING: _This section takes several hours or days._

## Prepare the base dictionary
### Download IPADIC

First, download IPADIC manually from [https://taku910.github.io/mecab](https://taku910.github.io/mecab)
```sh
WORKDIR=/path/to/your/work/dir
cd $WORKDIR # move to the working directory
cp /path/to/your/download/dir/mecab-ipadic-2.7.0-XXXX.tar.gz $WORKDIR
tar zxfv mecab-ipadic-2.7.0-XXXX.tar.gz
```
By trying `ls mecab-ipadic-2.7.0-XXXX`, you will find many CSV files and configuration files
in the directory.

### Download NEologd
Also, download the NEologd dictionary as follows.

```sh
cd $WORKDIR # move to the working directory
git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd/
```

Then, extract the csv file of NEologd dictionary using `unxz` command.
If your system has the unxz command,
```sh
find ./mecab-ipadic-neologd/seed/ -type f -name "*.xz" | xargs -I{} unxz -k {}
```
Or, otherwise,
```sh
docker run -v $(pwd):/root/workspace tdmelodic:latest \
    find ./mecab-ipadic-neologd/seed/ -type f -name "*.xz" | xargs -I{} unxz -k {}
# Or,
# find ./mecab-ipadic-neologd/seed/ -type f -name "*.xz" | xargs -I{} \
#    docker run -v $(pwd):/root/workspace tdmelodic:latest unxz -k {}
```
Thus many CSV files will be created at `./mecab-ipadic-neologd/seed/`.

## Inference

_WARNING! THIS TAKES MUCH TIME!_

Now let generate the accent dictionary.
It estimates the accent of the words listed in NEologd dictionary
by a machine learning -based technique.

### IPADIC
```sh
docker run -v $(pwd):/root/workspace tdmelodic:latest \
    find ./mecab-ipadic-2.7.0-*/ -type f -name "*.csv" | xargs -I{} \
        tdmelodic-convert -m ipadic --input {} --output {}.accent
```

### NEologd
```sh
docker run -v $(pwd):/root/workspace tdmelodic:latest \
    find ./mecab-ipadic-neologd/seed/ -type f -name "*.csv" | xargs -I{} \
        tdmelodic-convert -m ipadic --input {} --output {}.accent
```

Thus we obtain dictionary files `*.csv.accent` with the accent information added.
