from collections import defaultdict
import math

weights = defaultdict(float)  # weight vector


def read_data():
    global tagset
    tagset = set()
    tagset.add("<s>")# all available tags
    words, tags = ["<s>"],  ["<s>"]             # a sentence's tags (with the start-tag) # a sentence's words (with the start-token)
    sentences = []             # list of sentences [([w,w,w,...], [t,t,t,...]), (),...]
    with open("Tiger/develop.txt") as file:
        for line in file:
            line = line.strip()
            if len(line) == 0:
                # add end-token and end-tag
                words.append("<s>")
                tags.append("<s>")
                sentences.append((words, tags))
                words, tags = ["<s>"], ["<s>"]
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
    # feature: tag + shape
    shape = ""
    for x in word:
        if x.isupper():
            shape = shape + "X"
        elif x.islower():
            shape = shape + "x"
        elif x.isdigit():
            shape = shape + "0"
        else:
            shape = shape + x
    shape_old, shape_new = shape, ""
    while shape_old != shape_new:
        s = "".join([shape_old[x] for x in range(0, len(shape_old) - 1) if shape_old[x] != shape_old[x + 1]])
        shape_new = shape_old
        shape_old = s + shape_old[len(shape_old) - 1]
    features.append("TSH-" + tag + "-" + shape_new)
    return features


def local_score(features):
    return math.exp(sum([weights[f] for f in features]))


def calculate_expected(words: list):
    print(words)
    n = len(words)
    print(n)
    forward = defaultdict(lambda: defaultdict(float))
    backward = defaultdict(lambda: defaultdict(float))
    forward[0]["<s>"] = 1
    backward[n]["<s>"] = 1
    # collect forward probs
    for i in range(1, n):
        for tag in tagset:
            fwd_score = 0
            for prev_tag in forward[i-1]:
                features = get_features(words[i], tag, prev_tag) # TT (prev_tag + tag), TSH (tag + shape), TS (tag + substring), TW (tag + word), TWT (prev_tag + word + tag)
                fwd_score += forward[i-1][prev_tag] * local_score(features)
            forward[i][tag] = fwd_score
    # collect backward probs
    for j in range(n-1, 0):
        for tag in tagset:
            bwd_score = 0
            for prev_tag in backward[j+1]:
                features = get_features(words[j], tag, prev_tag)
                bwd_score += backward[j+1][prev_tag] * local_score(features)
            backward[j][tag] = bwd_score

    # Gamma berechnen
    for i in range(1, n):
        for tag in tagset:
            gamma = 0
            for prev_tag in forward[i-1]:
                f = get_features(words[i], tag, prev_tag)
                gamma += forward[i-1][prev_tag] * local_score(f) * backward[i][tag] / forward[n-1]['<s>']






def train():
    epochs = 1
    sentences = read_data() # [ ([w,w,w,...],[t,t,t,...]) , ([w],[t]) ,...]
    for _ in range(epochs):
        for sentence in sentences[0:1]:
            words, tags = sentence[0], sentence[1]
            expected = calculate_expected(words)

train()