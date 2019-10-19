""" Source: https://pytorch.org/tutorials/beginner/chatbot_tutorial.html """
import csv
import re
import os
import codecs
from io import open

# import math
# import itertools
# import unicodedata


def printLines(file, n=10):
    with open(file, "rb") as datafile:
        lines = datafile.readlines()
    for line in lines[:n]:
        print(line)


# Splits each line of the file into a dictionary of fields
def loadLines(fileName, fields):
    lines = {}
    with open(fileName, "r", encoding="iso-8859-1") as f:
        for line in f:
            values = line.split(" +++$+++ ")
            # Extract fields
            lineObj = {}
            for i, field in enumerate(fields):
                lineObj[field] = values[i]
            lines[lineObj["lineID"]] = lineObj
    return lines


# Groups fields of lines from `loadLines` into conversations based on *movie_conversations.txt*
def loadConversations(fileName, lines, fields):
    conversations = []
    with open(fileName, "r", encoding="iso-8859-1") as f:
        for line in f:
            values = line.split(" +++$+++ ")
            # Extract fields
            convObj = {}
            for i, field in enumerate(fields):
                convObj[field] = values[i]
            # Convert string to list (convObj["utteranceIDs"] == "['L598485', 'L598486', ...]")
            utterance_id_pattern = re.compile("L[0-9]+")
            lineIds = utterance_id_pattern.findall(convObj["utteranceIDs"])
            # Reassemble lines
            convObj["lines"] = []
            for lineId in lineIds:
                convObj["lines"].append(lines[lineId])
            conversations.append(convObj)
    return conversations


# Extracts pairs of sentences from conversations
def extractSentencePairs(conversations):
    qa_pairs = []
    for conversation in conversations:
        # Iterate over all the lines of the conversation
        for i in range(
            len(conversation["lines"]) - 1
        ):  # We ignore the last line (no answer for it)
            inputLine = conversation["lines"][i]["text"].strip()
            targetLine = conversation["lines"][i + 1]["text"].strip()
            # Filter wrong samples (if one of the lists is empty)
            if inputLine and targetLine:
                qa_pairs.append([inputLine, targetLine])
    return qa_pairs


def create_formatted_movie_lines(path=None, datafile=None, verbose=False):
    if path is None:
        corpus_name = "cornell movie-dialogs corpus"
        corpus = os.path.join("data", corpus_name)
        if verbose:
            printLines(os.path.join(corpus, "movie_lines.txt"))

    if datafile is None:
        # Define path to new file
        datafile = os.path.join(corpus, "formatted_movie_lines.txt")

    delimiter = "\t"
    delimiter = str(
        codecs.decode(delimiter, "unicode_escape")
    )  # Unescape the delimiter

    # Initialize lines dict, conversations list, and field ids
    lines = {}
    conversations = []
    MOVIE_LINES_FIELDS = ["lineID", "characterID", "movieID", "character", "text"]
    MOVIE_CONVERSATIONS_FIELDS = [
        "character1ID",
        "character2ID",
        "movieID",
        "utteranceIDs",
    ]

    # Load lines and process conversations
    lines = loadLines(os.path.join(corpus, "movie_lines.txt"), MOVIE_LINES_FIELDS)
    conversations = loadConversations(
        os.path.join(corpus, "movie_conversations.txt"),
        lines,
        MOVIE_CONVERSATIONS_FIELDS,
    )

    if verbose:
        print("\nProcessing corpus...")
        print("\nLoading conversations...")
        print("\nWriting newly formatted file...")

    # Write new csv file
    with open(datafile, "w", encoding="utf-8") as outputfile:
        writer = csv.writer(outputfile, delimiter=delimiter, lineterminator="\n")
        for pair in extractSentencePairs(conversations):
            writer.writerow(pair)

    # Print a sample of lines
    if verbose:
        print("\nSample lines from file:")
        printLines(datafile)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Cornell Movie Subtitle PyTorch")
    parser.add_argument("--input", type=str, default=None)
    parser.add_argument("--output", type=str, default=None)
    parser.add_argument("--verbose", type=bool, default=False)

    args = parser.parse_args()

    create_formatted_movie_lines(args.input, args.output, args.verbose)
