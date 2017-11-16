import math


def get(pre, now, bigram, dict, inf):
    try:
        res = math.log(bigram[pre][now])
    except KeyError:
        if (pre in dict or pre == 'start' or len(pre) == 1) and (now in dict or len(now) == 1):
            return inf
        return None

    return res


def calc(seg, bigram, inf):
    res = 0
    if not inf:
        inf = -15

    pre = 'start'
    for i in seg:
        try:
            res += math.log(bigram[pre][i])
        except KeyError:
            res += inf
        pre = i

    return res
