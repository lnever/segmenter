import sys
sys.path.append('..')

from npath.npath import Graph as npath_graph
from mmatch.mmatch import Graph as mmatch_graph
from maxpr.maxpr import Dag as maxpr_graph
from data import data
from model import bigram as Bigram
import argparse
import math
import time


def max_pr_seg(text, bigram, b, dict):

    g = maxpr_graph(len(text) + 1)

    for i in range(len(text) + 1):
        g.add_bigram(0, 0, i, Bigram.get('start', text[0:i], bigram, dict, b))

    for i in range(len(text) - 1):
        for j in range(i + 1, len(text), 1):
            for k in range(j + 1, len(text) + 1, 1):
                res = Bigram.get(text[i:j], text[j:k], bigram, dict, b)
                if res:
                   g.add_bigram(i, j, k, res)

    path = g.bigram_max_pr(b)
    result = []
    for edge in path:
        result.append(text[edge[0]:edge[1]])

    return result


def n_path_seg(text, dict, n, p):

    g = npath_graph(len(text) + 1)

    for i in range(len(text) - 1):
        for j in range(len(text)):
            if text[i:j + 1] in dict.keys():
                g.add_edge(i, j + 1, - math.log(dict[text[i:j + 1]]))

    for i in range(len(text)):
        if not g.lattice[i][i+1]:
            g.add_edge(i, i + 1, p)

    paths = g.n_shortest_path_dag(n)
    # print(paths)
    results = []
    for path in paths:
        words = []
        for edge in path:
            words.append(text[edge[0]:edge[1]])
        results.append(words)

    return results


def max_match_seg(text, dict):
    g = mmatch_graph(len(text) + 1)

    for i in range(len(text)):
        g.add_edge(i, i + 1)

    for i in range(len(text) - 1):
        for j in range(len(text)):
            if text[i:j + 1] in dict.keys():
                g.add_edge(i, j + 1)

    paths = g.bidirectional_max_match()

    results = []
    for path in paths:
        words = []
        for edge in path:
            words.append(text[edge[0]:edge[1]])
        results.append(words)

    return results


def disambiguate(segs, bigram, inf):
    now = -100000000000
    res = None
    for i in segs:
        p = Bigram.calc(i, bigram, inf)
        # print('{0}: {1}'.format(p, i))
        if p > now:
            res = i
            now = p

    return res


def output(seg, fout):
    if not seg:
        print('', file=fout)
        return
    for i in seg:
        print(i, end="  ", file=fout)
    print('', file=fout)
    pass


def main(n, m, pr, p, b, fi, fo):
    dict = data.load_dict()
    bigram = data.load_bigram()

    if not p:
        p = 15

    if not b:
        b = -30

    if not fi:
        print('No input file')
        return
    fin = open(fi, 'r', encoding='UTF-8')
    if not fo:
        fout = open('{0}_n{1}_m{2}_pr{3}_p{4}_b{5}.out'.format(fi, n, m, pr, p, b), 'w', encoding='UTF-8')
    else:
        fout = open(fo, 'w', encoding='UTF-8')

    texts = fin.readlines()
    now = 0
    for i in texts:
        if i.endswith('\n'):
            i = i[:-1]

        results = []
        if n:
            results += (n_path_seg(i, dict, n, p))
        if m:
            results += (max_match_seg(i, dict))
        if pr:
            results.append(max_pr_seg(i, bigram, b, dict))

        result = disambiguate(results, bigram, b)
        # while len(results) < n:
        #     results.append(None)
        # for result in results:
        #     output(result, fout=fout)
        output(result, fout=fout)
        now += 1
        print('{0}/{1}'.format(now, len(texts)))


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-n', type=int, help='使用N-最短路径分词算法，参数为N的大小')
    # parser.add_argument('-m', action='store_true', help='使用最大匹配分词算法')
    # parser.add_argument('-pr', action='store_true', help='使用最大概率分词算法')
    # parser.add_argument('-p', type=int, help='使用N-最短路径分词算法时，不成词单字的边权指数值（推荐8以上）')
    # parser.add_argument('-b', type=int, help='bigram中不存在词对的概率的对数值，推荐-15以下')
    # parser.add_argument('-fi', type=str, help='测试输入文件')
    # parser.add_argument('-fo', type=str, help='测试输出文件')
    # args = parser.parse_args()
    #
    # pre = time.time()
    # main(args.n, args.m, args.pr, args.p, args.b, args.fi, args.fo)
    # print(time.time() - pre)
    main(3, None, True, None, -15, 'in.txt', None)
