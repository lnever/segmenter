import heapq


class Graph:
    size = 0
    lattice = []

    def __init__(self, n, ):
        self.size = n
        self.lattice = [([0 for i in range(n)]) for i in range(n)]

    def add_edge(self, s, t, w):
        self.lattice[s][t] = w

    def shortest_path(self):
        inf = 1e12
        n = self.size
        g = self.lattice
        dist = [inf for i in range(n)]
        pre = [-1 for i in range(n)]
        in_queue = [0 for i in range(n)]
        dist[0] = 0
        in_queue[0] = 1

        q = list()
        q.append(0)

        while len(q):
            now = q.pop(0)
            in_queue[now] = 0
            for to in range(n):
                if not g[now][to]:
                    continue
                if dist[now] + g[now][to] < dist[to]:
                    pre[to] = now
                    dist[to] = dist[now] + g[now][to]
                    if not in_queue[to]:
                        q.append(to)
                        in_queue[to] = 1

        return dist, pre

    def get_paths(self, pre):
        path = []
        now = self.size - 1
        while pre[now] != -1:
            path.append((pre[now], now, self.lattice[pre[now]][now]))
            now = pre[now]
        if not path:
            return path
        path.reverse()
        return path

    def n_shortest_path(self, n):
        paths = []

        dist, pre = self.shortest_path()
        path = self.get_paths(pre)
        heapq.heappush(paths, (dist[self.size - 1], path, []))
        select_paths = []
        cut_paths = []
        select_paths.append(set(path))

        for i in range(n):

            if len(paths) > n:
                paths = heapq.nsmallest(n + 1, paths)

            items = heapq.nsmallest(i + 1, paths)
            try:
                pre = items[i][:]
            except IndexError:
                break
            pre_path = pre[1][:]
            pre_cut_path = pre[2][:]

            for edge in pre_cut_path:
                self.lattice[edge[0]][edge[1]] = 0

            for edge in pre_path:
                if edge in pre_cut_path:
                    continue

                now_cut_path = pre_cut_path[:]
                now_cut_path.append(edge)

                if set(now_cut_path) in cut_paths:
                    continue
                self.lattice[edge[0]][edge[1]] = 0
                dist, pre = self.shortest_path()
                self.lattice[edge[0]][edge[1]] = edge[2]
                path = self.get_paths(pre)
                if not path:
                    continue
                if set(path) in select_paths:
                    continue
                heapq.heappush(paths, (dist[self.size - 1], path, now_cut_path))
                # if len(paths) > n:
                #     paths = heapq.nsmallest(n, paths)

                select_paths.append(set(path))
                cut_paths.append(set(now_cut_path))

            for edge in pre_cut_path:
                self.lattice[edge[0]][edge[1]] = edge[2]

        heapq_res = heapq.nsmallest(n, paths)

        segs = []

        for i in heapq_res:
            seg = []
            for j in i[1]:
                seg.append(j[0:2])
            segs.append(seg)

        return segs

    def n_shortest_path_dag(self, n):
        dist = [[] for i in range(self.size)]

        dist[0].append((0, 0, None))

        for now in range(1, self.size, 1):
            for pre in range(now):
                if not self.lattice[pre][now]:
                    continue
                for i in dist[pre]:
                    heapq.heappush(dist[now], (i[0] + self.lattice[pre][now], now, i))
            if len(dist[now]) > n:
                dist[now] = heapq.nsmallest(n, dist[now])

        # print(dist)
        heapq_res = heapq.nsmallest(n, dist[self.size - 1])
        paths = []
        for i in heapq_res:
            pre = [-1 for i in range(self.size)]
            while i[2]:
                pre[i[1]] = i[2][1]
                i = i[2]
            paths.append(self.get_paths(pre))

        segs = []

        for i in paths:
            seg = []
            for j in i:
                seg.append(j[0:2])
            segs.append(seg)

        return segs


def test():
    g = Graph(3)
    g.add_edge(0, 1, 1)
    g.add_edge(1, 2, 1)
    g.add_edge(0, 2, 5)
    # print(g.n_shortest_path(2))
    print(g.n_shortest_path_dag(3))


if __name__ == '__main__':
    test()
