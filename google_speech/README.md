# Google Speech Commands


[Kaggle competetion](https://www.kaggle.com/c/tensorflow-speech-recognition-challenge/overview)


* Install kaggle API `pip install kaggle`
* Make sure you have your Kaggle credential key
  - in `~/.kaggle/kaggle.json`
  - then run:
    ```bash
    kaggle competitions download -c tensorflow-speech-recognition-challenge
    ```
* Manual download
  - [train](https://www.kaggle.com/c/tensorflow-speech-recognition-challenge/download/train.7z)
  - [test](https://www.kaggle.com/c/tensorflow-speech-recognition-challenge/download/test.7z)
* Extract
  - Check if 7z is installed by `whereis 7z`
  - Extract e.g `7z x train.7z`


## Dataset

A nice dataset from kaggle with (text, wav) pairs.

Everything in dataset.py is based on 
[DadidS Kaggle Kernel](https://www.kaggle.com/davids1992/speech-representation-and-data-exploration)
