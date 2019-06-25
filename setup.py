import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="SpeechCorpus",
    version="0.1",
    author="Erik Ekstedt",
    author_email="erikekst@kth.se",
    description="SpeechCorpus",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ErikEkstedt/SpeechCorpus",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ],
)
