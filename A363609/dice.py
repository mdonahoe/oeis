"""
min sum for the visible pips on n dice
"""

from collections import namedtuple
import unittest


SIDES = [(1,6), (2, 5), (3, 4)]

OPPOSITE = dict()
for a, b in SIDES:
    OPPOSITE[a] = b
    OPPOSITE[b] = a


Rot = namedtuple("Rot", ("top", "front", "right"))

A = Rot(1, 2, 3)
B = Rot(1, 3, 5)
C = Rot(1, 4, 2)
D = Rot(1, 5, 4)

E = Rot(2, 1, 4)
F = Rot(2, 3, 1)
G = Rot(2, 4, 6)
H = Rot(2, 6, 3)

I = Rot(3, 1, 2)
J = Rot(3, 2, 6)
K = Rot(3, 5, 1)
L = Rot(3, 6, 5)

M = Rot(4, 1, 5)
N = Rot(4, 2, 1)
O = Rot(4, 5, 6)
P = Rot(4, 6, 2)

Q = Rot(5, 1, 3)
R = Rot(5, 3, 6)
S = Rot(5, 4, 1)
T = Rot(5, 6, 4)

U = Rot(6, 2, 4)
V = Rot(6, 3, 2)
X = Rot(6, 4, 5)
Y = Rot(6, 5, 3)

Rotations = [A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,X,Y]

assert len(Rotations) == 24


class Dice:
    def __init__(self, top=1, front=2, right=3):
        self.f = front
        self.u = top
        self.r = right

    @property
    def front(self):
        return self.f

    @property
    def back(self):
        return OPPOSITE[self.front]

    @property
    def top(self):
        return self.u

    @property
    def bottom(self):
        return OPPOSITE[self.top]

    @property
    def right(self):
        return self.r

    @property
    def left(self):
        return OPPOSITE[self.right]

    def sides(self):
        return [self.front, self.back, self.top, self.bottom, self.left, self.right]

    def __repr__(self):
        return f"Dice(top={self.top}, front={self.front})"


DICE = [Dice(top=rot.top, front=rot.front, right=rot.right) for rot in Rotations]


Mask = namedtuple('Mask', ['front', 'back', 'top', 'bottom', 'left', 'right'])


def lowest(mask):
    die = None
    score = None
    tests = []
    for d in DICE:
        sides = d.sides()
        s = sum(c * s for c, s in zip(mask, sides))
        if score is None or s < score:
            score = s
            die = d 
    return die, score


class Layout:
    def __init__(self, i,j,k,b,h,x):
        assert i > 0
        assert j > 0
        assert k > 0
        assert i >= b
        assert i >= x
        assert b >= x
        if b > 0:
            assert h > 0
        if h > 0:
            assert b > 0
        if x == 0:
            assert j >= h
        else:
            assert j >= h+1

        self.i = i
        self.j = j
        self.k = k
        self.cube = (i,j,k)
        self.b = b
        self.h = h
        self.rect = (b, h)
        self.x = x

    def __str__(self):
        i,j,k,b,h,x = self.i, self.j, self.k, self.b, self.h, self.x
        pieces = []
        if i*j*k > 0:
            pieces.append(f"{i}x{j}x{k}")
        if b * h > 0:
            pieces.append(f"{b}x{h}")
        if x > 0:
            pieces.append(str(x))
        return " + ".join(pieces)

    def __repr__(self):
        return f"Layout({self.i}, {self.j}, {self.k}, {self.b}, {self.h}, {self.x})"

    def count(self):
        return self.i * self.j * self.k + self.b * self.h + self.x

    def top(self):
        grid = []
        for j in range(self.j):
            row = []
            for i in range(self.i):
                row.append('c')
            grid.append(row)

        for i in range(self.b):
            for j in range(self.h):
                grid[self.j - j - 1][i] = 'r'

        if self.x > 0:
            for i in range(self.x):
                grid[self.j - 1 - self.h][i] = 'x'

        return '\n'.join(''.join(line) for line in grid)

    def front(self):
        return 'r' * self.b + '\n' + '\n'.join(['c' * self.i] * self.k)

    def iterdice(self):
        for k in range(self.k):
            for j in range(self.j):
                for i in range(self.i):
                    front = j == 0
                    back = j == self.j - 1
                    top = k == self.k - 1
                    if top:
                        if i < self.b and j < self.h:
                            top = False
                        elif j == self.h and i < self.x:
                            top = False
                        else:
                            pass
                    bottom = k == 0
                    left = i == 0
                    right = i == self.i - 1
                    yield Mask(front, back, top, bottom, left, right)
        for h in range(self.h):
            for b in range(self.b):
                front = h == 0
                back = (h == self.h - 1) and (b >= self.x)
                top = True
                bottom = False
                left = b == 0
                right = b == self.b - 1
                yield Mask(front, back, top, bottom, left, right)

        for x in range(self.x):
            front = False
            back = True
            top = True
            bottom = False
            left = x == 0
            right = x == self.x - 1
            yield Mask(front, back, top, bottom, left, right)

class CoveredDice:
    def __init__(self, mask):
        self.mask = mask
        self.die, self.score = lowest(mask)

    def visible_sides(self):
        return [s for c, s in zip(self.mask, self.die.sides()) if c]


def score(layout):
    score = 0
    for i, cover in enumerate(layout.iterdice()):
        d = CoveredDice(cover)
        vs = d.visible_sides()
        score += d.score
    return score


class TestDice(unittest.TestCase):

    def test_single_coverage(self):
        # Top
        d, s = lowest(Mask(False, False, True, False, False, False))
        self.assertEqual(d.top,1)
        self.assertEqual(d.front,2)
        self.assertEqual(s,1)

        # Bottom
        d, s = lowest(Mask(False, False, False, True, False, False))
        self.assertEqual(d.top,6)
        self.assertEqual(d.front,2)
        self.assertEqual(s,1)
        self.assertEqual(d.bottom,1)

        # Front
        d, s = lowest(Mask(True, False, False, False, False, False))
        self.assertEqual(d.top,2)
        self.assertEqual(s,1)
        self.assertEqual(d.front,1)

        # Back
        d, s = lowest(Mask(False, True, False, False, False, False))
        self.assertEqual(d.top,2)
        self.assertEqual(s, 1)
        self.assertEqual(d.front,6)
        self.assertEqual(d.back,1)

        # left
        d, s = lowest(Mask(False, False, False, False, True, False))
        self.assertEqual(d.top,2)
        self.assertEqual(s,1)
        self.assertEqual(d.front,4)
        self.assertEqual(d.left,1)

        # right
        d, s = lowest(Mask(False, False, False, False, False, True))
        self.assertEqual(d.top,2)
        self.assertEqual(s,1)
        self.assertEqual(d.front,3)
        self.assertEqual(d.right,1)

    def test_double_coverage(self):
        # front and top
        d, s = lowest(Mask(True, False, True, False, False, False))
        self.assertEqual(1, d.top)
        self.assertEqual(2, d.front)
        self.assertEqual(3, s)

        # left and right
        d, s = lowest(Mask(False, False, False, False, True, True))
        self.assertEqual(1, d.top)
        self.assertEqual(2, d.front)
        self.assertEqual(7, s)

        # bottom and right
        d, s = lowest(Mask(False, False, False, True, False, True))
        self.assertEqual(5, d.top)
        self.assertEqual(4, d.front)
        self.assertEqual(1, d.right)
        self.assertEqual(2, d.bottom)
        self.assertEqual(3, s)

        # back and right
        d, s = lowest(Mask(False, True, False, False, False, True))
        self.assertEqual(3, d.top)
        self.assertEqual(5, d.front)
        self.assertEqual(1, d.right)
        self.assertEqual(2, d.back)
        self.assertEqual(3, s)

    def test_triple_coverage(self):
        # front, bottom, left corner
        d, s = lowest(Mask(True, False, False, True, True, False))
        self.assertEqual(4, d.top)
        self.assertEqual(1, d.front)
        self.assertEqual(2, d.left)
        self.assertEqual(3, d.bottom)
        self.assertEqual(6, s)

        # front, bottom, right corner
        d, s = lowest(Mask(True, False, False, True, False, True))
        self.assertEqual(2, d.front)
        self.assertEqual(1, d.right)
        self.assertEqual(3, d.bottom)
        self.assertEqual(6, s)
        self.assertEqual(4, d.top)

    def test_layout(self):
        a1 = Layout(1,1,1,0,0,0)
        self.assertEqual(1, a1.count())
        self.assertEqual(21, score(a1))

        a2 = Layout(2,1,1,0,0,0)
        self.assertEqual(2, a2.count())
        self.assertEqual(30, score(a2))

        a3 = Layout(2,1,1,1,1,0)
        self.assertEqual(3, a3.count())
        self.assertEqual(40, score(a3))

        a4 = Layout(2,2,1,0,0,0)
        self.assertEqual(4, a4.count())
        self.assertEqual(40, score(a4))

        a5 = Layout(2,2,1,1,1,0)
        self.assertEqual(5, a5.count())
        self.assertEqual(51, score(a5))

        a6 = Layout(2,2,1,2,1,0)
        self.assertEqual(6, a6.count())
        self.assertEqual(52, score(a6))

        a18 = Layout(3,3,2,0,0,0)
        self.assertEqual(18, a18.count())
        self.assertEqual(74, score(a18))


        a23 = Layout(3,3,2,2,2,1)
        self.assertEqual(23, a23.count())
        self.assertEqual(94, score(a23))

        a24 = Layout(4,3,2,0,0,0)
        self.assertEqual(24, a24.count())
        self.assertEqual(88, score(a24))

        # This was my first attempt at a lowest score
        a24b = Layout(3,3,2,3,2,0)
        self.assertEqual(24, a24b.count())
        self.assertEqual(91, score(a24b))

        a25 = Layout(3,3,2,3,2,1)
        self.assertEqual(25, a25.count())
        self.assertEqual(95, score(a25))

        a26 = Layout(3,3,2,3,2,2)
        self.assertEqual(26, a26.count())
        self.assertEqual(93, score(a26))

        a27 = Layout(3,3,3,0,0,0)
        self.assertEqual(27, a27.count())
        self.assertEqual(90, score(a27))

    def test_sequence(self):
        lows = dict()
        lows[0] = 0
        lays = dict()
        lays[0] = None
        # naive brute force search
        m = 8
        serts = 0
        for i in range(1, m):
            for j in range(1, i + 1):
                print("i=", i, "j=", j)
                for b in range(i + 1):
                    for x in range(b + 1):
                        for h in range(j + 1):
                            for k in range(1, m):
                                n = i * j * k + b * h + x
                                if n > 125: continue
                                try:
                                    l = Layout(i,j,k,b,h,x)
                                except AssertionError:
                                    serts += 1
                                    continue
                                s = score(l)
                                c = l.count()
                                if c not in lows or lows[c] > s:
                                    lows[c] = s
                                    lays[c] = l

        # Compare against the terms we manually determined.
        A363609 = [0, 21, 30, 40, 40, 51, 52, 54, 48, 60, 62, 65, 60, 72, 74, 77, 72, 78, 74, 86, 84, 91, 88, 92, 88, 95, 93, 90]
        ans = []
        for n, an in enumerate(A363609):
            self.assertEqual(an, lows[n], f"failed for {n}, {lays[n]}")

        # Print the layouts for each solution
        for n in sorted(lows.keys()):
            print(f"a({n}) = {lows[n]} via {lays.get(n, None)}")
            ans.append(lows[n])

        # Print the solutions in OEIS list format
        print("a(n) = ", ans)


if __name__ == "__main__":
    unittest.main()
