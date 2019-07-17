# [Switchboard](https://catalog.ldc.upenn.edu/LDC97S62)


**REQUIRES LICENCE and ACCESS. Go to [website](https://catalog.ldc.upenn.edu/LDC97S62) for
further information.**


| Info |  |
| :-----|:-------|
| Sample Type | 2-channel ulaw |
| Sample Rate | 8000 |
| Language(s) | English |
| License(s) | LDC User Agreement for Non-Members |
| Online Documentation | [LDC97S62 Documents](https://catalog.ldc.upenn.edu/docs/LDC97S62/) |


Annotations are done by [ISIP](https://www.isip.piconepress.com/projects/switchboard/)
- [Penn treebank transcription](https://www.isip.piconepress.com/projects/switchboard/releases/ptree_word_alignments.tar.gz)
- [ICSI Transcriptions](https://www.isip.piconepress.com/projects/switchboard/releases/switchboard_icsi_phone.tar.gz)
- [Manually corrected word alignments](https://www.isip.piconepress.com/projects/switchboard/releases/switchboard_word_alignments.tar.gz)
  - **Used in this repo**
  - Word level transcriptions, words and timings
  - This data is used in this repo


## Using

**Structure**: The data should be in the following structure


```bash
SpeechCorpus

└── switchboard
    ├── download_switchboard.py
    ├── README.md
    └── data
        └── swb1_d1
            └── data
                ├── sw02001.sph
                ├── ...
                └── sw03726.sph
```

------

1. Download the audio and save it into $SpeechCorpus/switchboard/data
2. Download the annotations by running `python download_switchboard.py`
    - [Manually corrected word alignments](https://www.isip.piconepress.com/projects/switchboard/releases/switchboard_word_alignments.tar.gz)
      - Word level transcriptions, words and timings
3. Resample audio by running `python process_switchboard.py`
    - default: `.sph - 8bit - 8kHz -> .wav, 16bit, 16kHz`
    - savepath: `data/audio`
    - NOTE! the upsampled wav files tak up ~56Gb
4. [get_word_counter.py](./get_word_counter.py) counts the words in the corpus (used for
   building vocab)
