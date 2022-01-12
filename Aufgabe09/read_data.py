
def process_tree(tree: str, s: int, index: int): #s ist startpos
    if tree[s] != "(":
        print("Error 2 in Syntax")
        exit()
    words, constituents = [], []
    current_const, current_word = "", ""
    end_index = index
    pos = s + 1
    word = False
    while pos != len(tree): #pos != len(tree) or pos != ")"
        # pos == " " -> beginn eines Wortes
        if tree[pos] == " ":
            word = True
            pos = pos + 1
            continue
        # pos == Teil einer Konstituente
        if tree[pos] != " " and tree[pos] != ")" and tree[pos] != "(" and word is False:
            current_const = current_const + tree[pos]
            pos = pos + 1
            continue
        # pos == ( -> beginn einer neuen Regel
        if tree[pos] == "(":
            w, c, e, i = process_tree(tree, pos, end_index) #return words, constituents, pos + 1
            end_index, words, constituents, pos, word = i, words+w, c+constituents, e, False
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
            constituents.append((current_const, index, end_index))
            if pos == len(tree)-1:
                new_const = []
                x = 0
                while x != len(constituents):
                    c_1, c_2 = constituents[x], constituents[x + 1]
                    if c_1[1] == c_2[1] and c_1[2] == c_2[2]:
                        new_const.append((c_2[0]+"="+c_1[0], c_1[1], c_1[2]))
                        x = x+2
                    else:
                        new_const.append(c_1)
                        x = x+1
                return words, new_const, pos + 1, end_index
            return words, constituents, pos + 1, end_index

def build_tree(wors: list, constituentes: list):
    # words: ['Ms.', 'Haag', 'plays', 'Elianti', '.']
    # constituentes[('TOP=S', 0, 5), ('NP', 0, 2), ('NNP', 0, 1), ('NNP', 1, 2), ('VP', 2, 4), ('VBZ', 2, 3), ('NP', 3, 4), ('NP=NNP', 3, 4), ('.', 4, 5)]
    sentence, max_const = [], [] # tree, max_const
    max_distance = 0
    marker = "$$nw$$"
    for c in constituentes:
        if c[2]-c[1] > max_distance: max_distance = c[2]-c[1]
        if "=" in c[0]:
            c_1, c_2 = c[0].split("=")
            max_const.append((c_1 + marker, c[1], c[2]))
            max_const.append((c_2, c[1], c[2]))
        else:
            max_const.append(c)
    rem_const = []
    for x in range(0, len(max_const)):
        c = max_const[x]
        if c[2]-c[1] == 1 and marker not in c[0]:
            w = "("+c[0]+" "+wors[c[1]]+")"
            if ["",w] not in sentence:
                sentence.append(["",w])
        else:
            rem_const.append(c)
    rem_const.reverse()
    for c in rem_const:
        sentence[c[1]][0] = "(" + c[0] + sentence[c[1]][0]
        sentence[c[2]-1][1] = sentence[c[2]-1][1] + ")"
    return "".join([x[0]+x[1] for x in sentence]).replace(marker, "")


with open("data/laura.txt", "r") as file:
    for line in file:
        w, c, _, _ = process_tree(line.replace("\n", ""), 0, 0)
        c.reverse()
        print("wordlist: ", w, "\nConstituents: ", c)
        s = build_tree(w, c)
        print(s)
        if s != line.replace("\n", ""):
            print("Fehler")
        else:
            print("WORKS")


'''with open("data/laura.txt", "r") as file:
    for line in file:
        try:
            w, c, _, _ = process_tree(line.replace("\n", ""), 0, 0)
            c.reverse()
            print(w, c)
            s = build_tree(w, c)
            print(s)
            if s != line.replace("\n", ""):
                print("Fehler")
            else:
                print("WORKS")
        except:
            print("Error 1 in Syntax")
            exit()'''