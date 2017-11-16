import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int)

    args = parser.parse_args()
    n = args.n
    # n = 2
    ft = open('{}.out'.format(n), 'r', encoding='utf-8')
    fg = open('pku_test_gold.utf8', 'r', encoding='utf-8')

    # ft = open('10.out', 'r', encoding='utf-8')
    # fg = open('pku_test_gold.utf8', 'r', encoding='utf-8')

    gs = fg.readlines()
    ts = ft.readlines()

    for i in gs:
        i = i.join('')

    for i in ts:
        i = i.join('')

    tot = 0
    yes = 0

    for i in gs:
        g = i.split()
        # print(tot)
        tot += 1
        for j in ts[tot*n-n:tot*n]:
            t = j.split()
            if not t:
                continue
            ok = 0
            for word in t:
                if word in g:
                    ok += 1
            if ok/len(t) >= 0.95:
                yes += 1
                break

    print(yes/tot)
