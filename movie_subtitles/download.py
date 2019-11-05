from subprocess import call
import os
import shutil


def download():
    """ download and extract cornell movie subtitle dataset """

    # Download
    url = "http://www.cs.cornell.edu/~cristian/data/cornell_movie_dialogs_corpus.zip"
    call(["wget", url])

    # Create data dir and unzip
    os.makedirs("data", exist_ok=True)
    zip_path = "data/cornell_movie_dialogs_corpus.zip"
    shutil.move("cornell_movie_dialogs_corpus.zip", zip_path)
    call(["unzip", zip_path, "-d", "data"])


if __name__ == "__main__":
    download()
