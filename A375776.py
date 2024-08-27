import time
"""
Bitwise conflict-free sequence: Each number n is placed into the first set k that contains no element x where n AND x > 0: a(n) = k.
"""

def f1(n):
    """
    This function requires tracking an ordered list of sets and finding the first set
    that can hold the new number n without conflicting with any existing member x of the set.
    For this sequence, the conflict function is defined as a binary overlap (n & x)
    """
    a_and_b = lambda a, b: a & b

    def conflicts(n, s, f):
        for x in s:
            if f(n, x):
                return True
        return False

    sets = []
    output = []
    for x in range(1, n + 1):
        for i, s in enumerate(sets):
            k = i  + 1
            if conflicts(x, s, a_and_b):
                # conflict found. check the next set
                continue
            else:
                # no conflict
                s.add(x)
                output.append(k)
                break
        else:
            # no available set. add a new one
            sets.append(set([x]))
            k = len(sets)
            output.append(k)
    for i, s in enumerate(sets[:]):
        print(i + 1, sorted(s))
    return output[-1]

def a(n):
    L = [0] + [0] * n
    for i in range(1, n + 1):
        k = next(k for k in range(1, len(L)) if i & L[k] == 0)
        L[k] |= i
        yield k

	
data = [0, 1, 1, 2, 1, 3, 4, 5, 1, 4, 3, 6, 2, 7, 8, 9, 1, 8, 7, 10, 6, 11, 12, 13, 5, 14, 15, 16, 17, 18, 19, 20, 1, 12, 11, 17, 10, 15, 14, 21, 13, 22, 23, 24, 25, 26, 27, 28, 2, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 1, 19, 18, 25, 16, 23, 22, 36, 10, 30, 29, 32]

first_10_sets = {
    1: [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536],
    2: [3, 12, 48, 192, 768, 3072, 12288, 49152],
    3: [5, 10, 80, 160, 1280, 2560, 20480, 40960],
    4: [6, 9, 96, 144, 1536, 2304, 24576, 36864],
    5: [7, 24, 224, 1792, 6144, 57344],
    6: [11, 20, 288, 576, 1152, 10240, 53248],
    7: [13, 18, 320, 544, 2176, 5120, 73728],
    8: [14, 17, 352, 640, 7168, 81920],
    9: [15, 112, 384, 3584, 28672, 98304],
    10: [19, 36, 72, 896, 9216, 18432, 69632],
}

def timeit(f):
    t = time.time()
    for i in range(1, 40):
        x = f(i)
        assert x == data[i]
    print(f, time.time() - t)

print(list(a(75)))
