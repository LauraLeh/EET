
# Verarbeitet den Baum und gibt u.a. die Wortliste und die Konstituentenliste zurück
def process_tree(tree: str, s: int, index: int):
    if tree[s] != "(":
        print("Error 2 in Syntax")
        exit()
    words, constituents = [], []
    current_const, current_word = "", ""
    end_index = index
    pos = s + 1
    word = False
    while pos != len(tree):
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
        # pos == Teil eines Wortes, evtl Ende eines Wortes
        if word is True and tree[pos] != ")":
            current_word = current_word + tree[pos]
            if tree[pos +1] == ")":
                words.append(current_word)
                current_word = ""
                end_index = index +1
            pos = pos + 1
            continue
        # pos == ) -> Ende einer Regel, eventuell Ende des ganzen Satzes
        if tree[pos] == ")":
            constituents.append((current_const, index, end_index))
            if pos == len(tree)-1:
                new_const = []
                for x in range(0, len(constituents) - 1):
                    c_1, c_2 = constituents[x], constituents[x + 1]
                    if c_1[1] == c_2[1] and c_1[2] == c_2[2]:
                        new_const.append((c_2[0]+"="+c_1[0], c_1[1], c_1[2]))
                    else:
                        new_const.append(c_1)
                return words, new_const, pos + 1, end_index
            return words, constituents, pos + 1, end_index

def build_tree(wors: list, constituentes: list):

with open("data/laura.txt", "r") as file:
    for line in file:
        try:
            w, c, _, _ = process_tree(line.replace("\n", ""), 0, 0)
            c.reverse()
            print(w, c)
        except:
            print("Error 1 in Syntax")
            exit()