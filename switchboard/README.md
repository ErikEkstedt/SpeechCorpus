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

* (Create python env)
* Install dependencies `pip install -r requirements.txt`
* Source environment


1. Download the audio and save it into $SpeechCorpus/switchboard/data
2. Download the annotations by running `python download_switchboard.py`
    - [Manually corrected word alignments](https://www.isip.piconepress.com/projects/switchboard/releases/switchboard_word_alignments.tar.gz)
      - Word level transcriptions, words and timings
3. Resample audio by running `python process_switchboard.py`
    - default: `.sph - 8bit - 8kHz -> .wav, 16bit, 16kHz`
    - savepath: `data/audio`
    - NOTE! the upsampled wav files tak up ~56Gb


## Annotations

#### Penn Treebank Transcriptions (11/26/02) 

"Download the Penn Treebank Transcriptions: This release contains a few bug
fixes in the 10/19/02 release, reflecting changes described above in the word alignments
and segmentations. This Penn Treebank release contains an alignment of the ISIP
hand-aligned word transcriptions to the Penn Treebank word transcriptions for all **1126** SWB
conversations that are included in the Treebank. For the words which are in agreement
between the two transcriptions, time marks are given. For words that do not agree, we
estimate the times for the Treebank transcriptions using the ISIP transcriptions. The
transcriptions also include all instances of silence, laughter and noise." - website

