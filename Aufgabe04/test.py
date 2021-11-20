import sys
import os
import pickle


test = sys.argv[2]
paramfile = sys.argv[1]

classe = [f for f in os.listdir(test) if not f.startswith('.')]

with open(paramfile, 'rb') as file:
    para = pickle.load(file)

priori_klass = para['klass_prio']
klass_word_prob = para['klass_word_prob']


#file = []


def class_predict(words):
    for klass in classe:
        klass_prob = 0
        for word in words:
            klass_prob = math.log(klass_word_prob[klass].get(word,1))
        klass_prob += math.log(priori_klass[klass])
        prob_dict[klass] = klass_prob
    label = max(prob_dict.keys(), key=prob_dict.get)
    return label

def klass_adress(test):
    test_set_path, label_list = [], []
    for klass in classe:
        for root,_,files in os.walk(test+'/'+klass):
            class_address[klass] = [os.path.join(root, file) for file in files]
        test_set_path += class_adress.values()
        label_list.append(klass)
    return test_set_path, label_list

def predict(test_set_path):
    resault = []
    for klass in classe:
        for mail in test_set_path[klass]:
            with open(mail, 'r', encoding='ISO-8859-1') as m:
                text = m.read().split()
                pred_label = class_predict(text)
        resault.append(pred_label)
    return resault

def accuracy(resault):
    num = 0
    for l in resault:
        for m in label_list:
            if l == m:
                num += 1
    acc = num/len(resault)
    print(acc)
    return acc


if __name__ == '__main__':
    for klass in classe:
        for root,_,files in os.walk(train+'/'+klass):
            klass_address = [os.path.join(root, file) for file in files]
            all_text = ''
            klass_words[klass] = all_text.split()
