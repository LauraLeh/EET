from collections import defaultdict
import math

weights = defaultdict(float)  # weight vector


def read_data():
    global tagset
    tagset = set("<s>")        # all available tags
    tags = ["<s>"]             # a sentence's tags (with the start-tag)
    words = ["<s>"]            # a sentence's words (with the start-token)
    sentences = []             # list of sentences

    with open("Tiger/develop.txt") as file:
        for line in file:
            line = line.strip()
            if len(line) == 0:
                # add end-token and end-tag
                words.append("<s>")
                tags.append("<s>")
                sentences.append((words, tags))
                words = ["<s>"]
                tags = ["<s>"]
            else:
                word, tag = line.split()
                words.append(word)
                tags.append(tag)
                tagset.add(tag)
    return sentences


def get_substrings(string):
  substring_len = 3
  string_len = len(string)
  substrings = []
  i = 0
  while not i > string_len - substring_len:
    substrings.append(string[i: i+ substring_len])
    i += 1
  return substrings


def get_features(word, tag, prev_tag):
    features = list()
    features.append("TT-"+prev_tag+"-"+tag) # context feature: prev_tag + tag
    features.append("TWT-"+prev_tag+"-"+word+"-"+tag) # context feature: prev_tag + word + tag
    features.append("TW-"+tag+"-"+word) # lexical feature: tag + word
    if len(word) > 3: # otherwise the feature would be the same as the TW feature anyways (we're taking substrings of len 3)
        substrings = get_substrings(word)
        for substring in substrings:
            features.append('TS-'+tag+"-"+substring)  # lexical feature: tag + substring (all substrings of the word)
    return features


def local_score(features):
    return math.exp(sum([weights[f] for f in features]))


def calculate_expected(words):
    n = len(words) - 1
    forward = defaultdict(lambda: defaultdict(float))
    backward = defaultdict(lambda: defaultdict(float))
    forward[0]["<s>"] = 1
    backward[n]["<s>"] = 1

    for i in range (1, n):
        for tag in tagset:
            fwd_score = 0
            for prev_tag in forward[i-1]:
                features = get_features(words[i], tag, prev_tag)
                fwd_score += forward[i-1][prev_tag] * local_score(features)
            forward[i][tag] = fwd_score
    print(forward)


def train():
    epochs = 1
    sentences = read_data()
    for _ in range(epochs):
        for sentence in sentences[0:1]:
            words, tags = sentence
            expected = calculate_expected(words)

train()