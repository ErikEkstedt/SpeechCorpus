from os import system, makedirs


ORIGINAL = {
    "audio": "http://www.openslr.org/resources/12/original-mp3.tar.gz",
    "books": "http://www.openslr.org/resources/12/original-books.tar.gz",
}

ENGLISH = {
    "train_clean_100": "http://www.openslr.org/resources/12/train-clean-100.tar.gz",
    "train_clean_360": "http://www.openslr.org/resources/12/train-clean-360.tar.gz",
    "train_other_500": "http://www.openslr.org/resources/12/train-other-500.tar.gz",
}


def download_audio(audio_path, url):
    makedirs(audio_path, exist_ok=True)
    wget_cmd = ["wget", "-P", audio_path, url, "-q", "--show-progress"]
    system(" ".join(wget_cmd))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Librispeech")
    parser.add_argument("--audio_path", default="data/audio")
    parser.add_argument("--data", type=str, default="train_clean_100")
    args = parser.parse_args()

    download_audio(args.audio_path, ENGLISH[args.data])
