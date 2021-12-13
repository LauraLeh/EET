from collections import defaultdict, Counter
import itertools
import math
import sys
import json

weights = defaultdict(float)

def read_data():
    global tagset
    tagset = {"<s>", "</s>"}
    tags = ["<s>"]             # a sentence's tags (with the start-tag)
    words = ["<s>"]            # a sentence's words (with the start-token)
    sentences = []

    with open(sys.argv[1]) as file:
        for line in file:
            line = line.strip()
            if len(line) == 0:
                # add end-token and end-tag
                words.append("</s>")
                tags.append("</s>")
                sentences.append((words, tags))
                words, tags = ["<s>"], ["<s>"]
            else:
                word, tag = line.split()
                words.append(word)
                tags.append(tag)
                tagset.add(tag)
    return sentences

def get_substrings(string):
  string = " " + string + " "
  min_range, max_range = 3, 6
  substrings = [string[min: min+max] for min in range(len(string) - min_range) for max in range(min_range, max_range+1)]
  return substrings

def get_word_shape(string):
    shape = ""
    for x in string:
        if x.isupper():
            shape = shape + "X"
        elif x.islower():
            shape = shape + "x"
        elif x.isdigit():
            shape = shape + "0"
        else:
            shape = shape + x
    return ''.join(x for x, _ in itertools.groupby(shape))

def get_features(word, tag, prev_tag):
    features = []
    features.append("TT-" + prev_tag + "-" + tag) # context feature: prev_tag + tag
    features.append("TWT-" + prev_tag + "-" + word + "-" + tag) # context feature: prev_tag + word + tag
    features.append("TW-" + tag + "-" + word) # lexical feature: tag + word
    features.append("TSH-" + tag + "-" + get_word_shape(word))  # lexical feature: tag + shape
    for substring in get_substrings(word):
        features.append('TSUB-' + tag + "-" + substring)  # lexical feature: tag + substring (all substrings of the word)
    return features

def log_sum_exp(x1, x2):
    a = max(x1, x2)
    b = min(x1, x2)
    return a + math.log(1 + math.exp(b-a))

def local_score(features):
    return sum([weights[f] for f in features])

def forward(words: list):
    n = len(words) - 1
    forw = defaultdict(lambda: defaultdict(float))
    forw[0]["<s>"] = 0
    for i in range(1, n):
        for tag in tagset:
            for prev_tag, prev_score in forw[i-1].items():
                features = get_features(words[i], tag, prev_tag)
                fwd_score = prev_score + local_score(features)
                forw[i][tag] = log_sum_exp(forw[i][tag], fwd_score)
    return forw

def backward(words: list):
    n = len(words) - 1
    backw = defaultdict(lambda: defaultdict(float))
    backw[n]["</s>"] = 0
    for j in range(n-1, 0, -1):
        for tag in tagset:
            for prev_tag, prev_score in backw[j+1].items():
                features = get_features(words[j], tag, prev_tag)
                bwd_score = prev_score + local_score(features)
                backw[j][tag] = log_sum_exp(backw[j][tag], bwd_score)
    return backw

def estimated_feat_values(forward: dict, backward: dict, words: list):
    n = len(words) - 1
    estimated = defaultdict(float)
    for i in range(1, n):
        for tag, beta_score in backward[i].items():
            for prev_tag, alpha_score in forward[i-1].items():
                f = get_features(words[i], tag, prev_tag)
                gamma = alpha_score + local_score(f) + beta_score - forward[-1]["</s>"]
                # first calculate and weight "local" counts, then sum them up into a "global" feature vector
                local_estimated = Counter(feat for feat in f)
                for feat in local_estimated:
                    estimated[feat] += local_estimated[feat] * gamma
    return estimated

def calculate_observed(words, tags):
    observed = defaultdict(float)
    n = len(words) - 1
    for i in range(1, n):
        features = get_features(words[i], tags[i], tags[i-1])
        for feat in features:
            observed[feat] += 1
    return observed


if __name__ == "__main__":
    epochs = 2
    learning_rate = 0.001
    sentences = read_data()
    for _ in range(epochs):
        for sentence in sentences:
            words, tags = sentence
            alpha = forward(words)
            beta = backward(words)
            efv = estimated_feat_values(alpha, beta, words)
            ofv = calculate_observed(words, tags)
            for feature in efv:
                gradient = ofv[feature] - efv[feature]
                weights[feature] += learning_rate * gradient

    with open(sys.argv[2], 'w', encoding="utf-8") as param_file:
        json.dump([weights, tagset], param_file)