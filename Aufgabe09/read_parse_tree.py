words = []
span_end = 0

def process_tree(tree, pos):
    global span_end
    start = len(words)
    constituents = []
    label, new_pos = read_symbol(tree, pos)

    while tree[new_pos] == "(":
        new_consts, new_pos = process_tree(tree, new_pos)
        for constituent in new_consts:
            constituents.append(constituent)
        if tree[new_pos] == ")":
            parent = (label, start, span_end)
            child_label, child_start, child_end = constituents[0]
            # eliminate chain-rule
            if (child_start, child_end) == (start, span_end):
                constituents.pop(0)  # remove the child
                parent = (f"{label}={child_label}", start, span_end)

            constituents.insert(0, parent) # insert parent before the children

    if tree[new_pos] == " ":
        word, new_pos = read_symbol(tree, new_pos)
        words.append(word)
        span_end += 1
        constituents.append((label, start, span_end))
    return (constituents), new_pos+1

# reads label or word
def read_symbol(tree, pos):
    pos += 1
    symbol = ""
    while tree[pos] not in [" ", "(", ")"]:
        symbol  += tree[pos]
        pos += 1
    return symbol, pos


with open("data/dev.txt", "r") as file:
    for line in file:
        cons, _ = process_tree(line,0)
        print(cons)
        print(words)
        words = []
        span_end = 0
