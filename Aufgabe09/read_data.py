import sys

def process_tree(tree: str, s: int, index: int): #s ist startpos
    if tree[s] != "(":
        print("Error")
    words, constituents = [], []
    end_index = index
    pos = s + 1
    current_const, current_word = "", ""
    word = False
    while pos != len(tree) or pos != ")": #pos != 17 and pos != len(tree) or pos != 17 and pos != ")":
        # pos == " " -> beginn eines Wortes
        if tree[pos] == " ":
            word = True
            pos = pos + 1
            continue
        # pos == Teil einer Konstituente
        if tree[pos] != " " and tree[pos] != ")" and tree[pos] != "(" and word is False:
            current_const = current_const + tree[pos]
            if tree[pos +1] == "(" or tree[pos +1] == " ":
                constituents.append((current_const, index, "x"))
                current_const = ""
            pos = pos + 1
            continue
        # pos == ( -> beginn einer neuen Regel
        if tree[pos] == "(":
            w, c, e, i = process_tree(tree, pos, end_index) #return words, constituents, pos + 1
            end_index, words, constituents, pos, word = i, words+w, constituents+c, e, False
            continue
        if word is True and tree[pos] != ")":
            current_word = current_word + tree[pos]
            if tree[pos +1] == ")":
                words.append(current_word)
                current_word = ""
                end_index = index +1
            pos = pos + 1
            continue
        if tree[pos] == ")":
            return words, constituents, pos + 1, end_index
    if tree[pos] == ")":
        constituents.append((current_const, index, end_index))
        return words, constituents, pos + 1, end_index


with open("data/test.txt", "r") as file:
    for line in file:
        line = line.replace("\n", "")
        line = ' '.join(line.split()) + "\n"
        w, c, _, _ = process_tree(line, 0, 0)
        print(w, c)

