import sys
import os
import pickle
from collections import Counter, defaultdict

train = sys.argv[1]
paramfile = sys.argv[2]

classe = [f for f in os.listdir(train) if not f.startswith('.')]
#classe=['spam', 'ham']

def read_data(train):
    class_num, class_text = {},{}
    for klass in classe:
        for root,_,files in os.walk(train+'/'+klass):
            klass_address = [os.path.join(root, file) for file in files]
            all_text = ''
            class_num[klass] = len(klass_address)
            for mail in klass_address:
                with open(mail, encoding='ISO-8859-1') as myfile:
                    text = myfile.read()
                    all_text += text
                    class_text[klass] = all_text.split()
    return class_text, class_num #f(c)

def basic_param(class_text, class_num):
    klass_prob, set_word_freq, klass_word_freq, klass_word_freq_dict= {}, Counter(), Counter(), {}
    for klass in classe:
        klass_num = class_num[klass]
        klass_word_freq = Counter(class_text[klass]) #f(w,c)
        klass_word_freq_dict[klass] = dict(klass_word_freq)
        klass_prob[klass] = klass_num/sum(class_num.values()) #p(c)
        set_word_freq += klass_word_freq  #f(w, c')
    word_prob = {k: v/sum(set_word_freq.values()) for k, v in dict(set_word_freq).items()} #p(w)
    return klass_word_freq_dict, klass_prob, word_prob

def rela_freq(klass_word_freq_dict):
    word_count =[]
    for klass in classe:
        word_count += klass_word_freq_dict[klass].values()
    N1 = word_count.count(1)
    N2 = word_count.count(2)
    print(N1,N2)
    delta = N1 / (N1 + 2 * N2) if (N1 + 2 * N2) != 0 else 0
    rela_freq_dic = defaultdict(float)
    for klass in classe:
        #print(klass_word_freq_dict['spam']['spam'])
        rela_freq_dic[klass] = {k: max(0, klass_word_freq_dict[klass].get(k,0) - delta) / sum(klass_word_freq_dict[klass].values()) for k in
                              klass_word_freq_dict[klass].keys()}  # r(w|c)
    return rela_freq_dic

def klass_word_prob(rela_freq_dic, word_prob):
    klass_word_prob = {}
    for klass in classe:
        klass_alpha = 1-sum(rela_freq_dic[klass].values())
        klass_word_prob[klass] = {k: rela_freq_dic[klass][k] + klass_alpha*word_prob[k] for k in rela_freq_dic[klass].keys()}
    return klass_word_prob

def save_parameter(klass_prob, klass_word_prob, filename):
    para = dict()
    para['klass_prio'] = klass_prob
    para['klass_word_prob'] = klass_word_prob
    with open(filename, 'wb') as file:
        pickle.dump(para, file)


if __name__ == '__main__':
    class_text, class_num = read_data(train)
    klass_word_freq, klass_prob, word_prob = basic_param(class_text, class_num)
    rela_freq_dic = rela_freq(klass_word_freq)
    klass_word_prob(rela_freq_dic, word_prob)
    save_parameter(klass_prob, klass_word_prob, paramfile)
