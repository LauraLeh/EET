import sys
import re
from string import punctuation


# punctuation that marks the end of a sentence.
# closing brackets / quotation marks after dots are included.
sentence_marker = ('.', '!', '?', '.)', '.]', '."')
# accepts numbers of form 1,23 and 1.23
float_regex = r'\d+(\.|\,)\d+'
# considers (optional) http:// or https:// and extensions of the form /.../...
website_regex = r'\(*(http:\/{2}|https:\/{2})*(www\.).+\.\w{2,3}(\/\w*)*\)*'


def read_files(abbreviations_path, text_path):
    with open(text_path, "r") as f:
        text = f.read()

    with open(abbreviations_path) as file:
        abbr = file.readlines()
        abbr = [line.strip() for line in abbr]

    return text, abbr


def main():
    if len(sys.argv) != 3:
        exit()

    text, abbr = read_files(sys.argv[1], sys.argv[2])
    sentence = ""

    # split() splits the text on spaces:
    # "some words; and some more words." -> ["some", "words;", "and", "some", "more", "words."]
    for token in text.split():
        # if the token is an abbreviation, a float number, a website or doesn't contain any punctuation:
        # just add the token to the sentence as it is
        if token in abbr or re.match(float_regex, token) or re.match(website_regex, token) or not any(
                p in token for p in punctuation):
            sentence += token + " "
        # else (i.e. if the token is no special case and has some punctuation):
        # split the token on any character that is not alpha-numeric, e.g. "Donau-Isar" -> "Donau", "-", "Isar"
        else:
            sentence += " ".join(re.split('(\W)', token))
            # if the end of a potential sentence is reached: print the accumulated sentence
            if token.endswith(sentence_marker):
                print(sentence)
                sentence = ""

if __name__ == '__main__':
    main()