from os import system, makedirs, listdir
from os.path import join, expanduser


# English
eng_urls = [
    "https://download.zerospeech.com/2017/train/english.zip",
    "https://download.zerospeech.com/2017/test/english_test.zip",
]

# French
fre_urls = [
    "https://download.zerospeech.com/2017/train/french.zip",
    "https://download.zerospeech.com/2017/test/french_test.zip",
]

# Mandarin
man_urls = [
    "https://download.zerospeech.com/2017/train/mandarin.zip",
    "https://download.zerospeech.com/2017/test/mandarin_test.zip",
]

# Development dataset
lang1_urls = [
    "https://download.zerospeech.com/2017/train/LANG1.zip",
    "https://download.zerospeech.com/2017/test/LANG1_test.zip",
]

lang2_urls = [
    "https://download.zerospeech.com/2017/train/LANG2.zip",
    "https://download.zerospeech.com/2017/test/LANG2_test.zip",
]


def download_single(datapath, lang=None):
    if lang.lower() == "eng":
        urls = eng_urls
    elif lang.lower() == "fre":
        urls = fre_urls
    elif lang.lower() == "man":
        urls = man_urls
    elif lang.lower() == "lang1":
        urls = lang1_urls
    elif lang.lower() == "lang2":
        urls = lang2_urls
    else:
        print("#" * 50)
        print(f"Language {lang} unknown")
        print(f"Please use eng, fre or man")
        print("#" * 50)
        raise NotImplementedError

    makedirs(datapath, exist_ok=True)
    for i, url in enumerate(urls):
        print(f"Downloading {i+1}/{len(urls)}")
        wget_cmd = ["wget", "-P", datapath, url, "-q", "--show-progress"]
        system(" ".join(wget_cmd))

    zips = [f for f in listdir(datapath) if f.endswith(".zip")]
    for zip in zips:
        print(f"Extracting {zip}")
        system(f"tar xjf {join(datapath, zip)} -C {datapath}")


def download_all(datapath):
    print("Downloading English")
    download_single(datapath, lang="eng")
    print("Downloading French")
    download_single(datapath, lang="fre")
    print("Downloading Mandaring")
    download_single(datapath, lang="man")
    print("Downloading Lang1")
    download_single(datapath, lang="lang1")
    print("Downloading Lang2")
    download_single(datapath, lang="lang2")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Download Zerospeech 2017")
    parser.add_argument("--datapath", default="data")
    parser.add_argument("--lang", default="eng")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()

    if args.all:
        download_all(args.datapath)
    else:
        download_single(args.datapath, args.lang)
