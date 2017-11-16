
class Graph:
    size = 0
    lattice = []

    def __init__(self, n, ):
        self.size = n
        self.lattice = [([0 for i in range(n)]) for i in range(n)]

    def add_edge(self, s, t):
        self.lattice[s][t] = 1

    def get_paths(self, pre):
        path = []
        now = self.size - 1
        while pre[now] != -1:
            path.append((pre[now], now))
            now = pre[now]
        if not path:
            return path
        path.reverse()
        return path

    def forward_max_match(self):
        dist = 0
        pre = [-1 for i in range(self.size)]
        start = 0
        while start < self.size - 1:
            for end in range(self.size - 1, start, -1):
                if self.lattice[start][end]:
                    pre[end] = start
                    dist += self.lattice[start][end]
                    start = end

        return self.get_paths(pre)

    def backward_max_match(self):
        dist = 0
        pre = [-1 for i in range(self.size)]
        end = self.size - 1
        while end > 0:
            for start in range(end):
                if self.lattice[start][end]:
                    pre[end] = start
                    dist += self.lattice[start][end]
                    end = start

        return self.get_paths(pre)

    def bidirectional_max_match(self):
        res_forward = self.forward_max_match()
        res_backward = self.backward_max_match()

        return [res_forward, res_backward]


def test():
    g = Graph(3)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(0, 2)
    print(g.bidirectional_max_match())


if __name__ == '__main__':
    test()
