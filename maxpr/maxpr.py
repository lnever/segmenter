class Dag:
    size = 0
    bigram = {}

    def __init__(self, n):
        self.bigram = {}
        self.size = n

    def add_bigram(self, i, j, k, pr):

        if k not in self.bigram.keys():
            self.bigram[k] = {}

        if i == j == 0:
            self.bigram[k][0] = pr
            return

        if j not in self.bigram[k].keys():
            self.bigram[k][j] = {}

        self.bigram[k][j][i] = pr

    def bigram_max_pr(self, inf):

        pr = [-100000000 for i in range(self.size)]
        bpr = [([-100000000 for i in range(self.size)]) for i in range(self.size)]
        bpre = [([-1 for i in range(self.size)]) for i in range(self.size)]
        bpr[0][0] = 1

        for k in range(1, self.size, 1):

            for i in range(k - 1):
                if bpr[k - 1][i] + inf > bpr[k][k - 1]:
                    bpr[k][k - 1] = bpr[k - 1][i] + inf
                    bpre[k][k - 1] = i

            for j in range(k):
                if j == 0:
                    try:
                        tmp = self.bigram[k][0]
                    except:
                        continue
                    if tmp:
                        bpr[k][0] = tmp

                for i in range(j):
                    try:
                        tmp = self.bigram[k][j][i]
                    except:
                        continue
                    if bpr[j][i] + tmp >= bpr[k][j]:
                        bpr[k][j] = bpr[j][i] + tmp
                        bpre[k][j] = i

        now = self.size - 1
        path = []
        while now != -1:
            maxpr = -100000000
            to = -1
            for i in range(now):
                if bpr[now][i] > maxpr:
                    maxpr = bpr[now][i]
                    to = i
            if to == -1:
                break
            path.append((to, now))
            if bpre[now][to] == -1:
                break
            path.append((bpre[now][to], to))

            now = bpre[now][to]

        path.reverse()

        return path


def test():
    g = Dag(10)
    g.add_bigram(0, 0, 1, 1)
    g.add_bigram(1, 2, 3, 1)
    g.add_bigram(2, 3, 4, 5)
    print(g.bigram_max_pr(-10))


if __name__ == '__main__':
    test()
