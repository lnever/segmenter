import json


def load_dict():
    fin = open('dict_t', 'r+')
    dict = json.load(fin)
    return dict


def load_bigram():
    fin = open('bigram_t', 'r+')
    bigram = json.load(fin)
    return bigram


def training(fin=None):
    if not fin:
        fin = open('training.txt', 'r+', encoding='UTF-8')

    tot = 0
    dict = {}
    bigram = {}
    for i in fin.readlines():
        words = i.split()
        pre = 'start'
        for j in words:
            tot += 1
            if j not in dict.keys():
                dict[j] = 0
            dict[j] += 1

            if pre not in bigram.keys():
                bigram[pre] = {}
            if j not in bigram[pre].keys():
                bigram[pre][j] = 0
            bigram[pre][j] += 1

            pre = j

    for i in dict.keys():
        dict[i] = dict[i]/tot

    for i in bigram.keys():
        for j in bigram[i].keys():
            bigram[i][j] = bigram[i][j]/tot

    json.dump(dict, fp=open('dict_t', 'w+'))
    json.dump(bigram, fp=open('bigram_t', 'w+'))

    fout = open('dict_t.txt', 'w')
    for i in dict.keys():
        print('{0} {1}'.format(i, dict[i]), file=fout)

    fout = open('bigram_t.txt', 'w')
    for i in bigram.keys():
        for j in bigram[i].keys():
            print('{0} {1} {2}'.format(i, j, bigram[i][j]), file=fout)


def test():
    training()


if __name__ == '__main__':
    test()
