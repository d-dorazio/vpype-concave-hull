from typing import Union
import numpy as np
from shapely.geometry import Polygon, MultiPoint, LineString


def concave_hull(pts: np.ndarray, k: int = 3) -> Union[Polygon, None]:
    pts = np.array(list({(x, y) for x, y in pts}))
    if len(pts) < 3:
        return None

    if len(pts) == 3:
        return Polygon(pts)

    top = np.argmin(pts[:, 1])

    print()
    print(top)
    print(pts)
    print()

    return _concave_hull(pts, top, k)


def _concave_hull(pts: np.ndarray, top: int, kk: int = 3) -> Union[Polygon, None]:
    kk = max(3, kk)
    if kk > len(pts):
        return None

    alive = np.ones(len(pts), dtype=int)

    hull = [tuple(pts[top])]
    current = top
    alive[current] = 0

    angle = 0
    step = 2

    while (current != top or step == 2) and np.count_nonzero(alive) > 0:
        if step == 5:
            alive[top] = 1
        step += 1

        # index, temp, deltax, deltay
        data = np.zeros((len(pts), 4))
        data[:, 0] = np.indices((len(pts),))

        # consider only alive points
        data = data[alive == 1]

        # populate the delta columns
        alive_pts = pts[data[:, 0].astype(int)]
        data[:, 2] = alive_pts[:, 0] - pts[current][0]
        data[:, 3] = alive_pts[:, 1] - pts[current][1]

        # nearest neighbors
        data[:, 1] = np.hypot(data[:, 2], data[:, 3])
        data = data[np.argpartition(data[:, 1], min(kk - 1, len(data) - 1))[:kk]]
        data = data[data[:, 1].argsort()]

        # sort by right hand turn
        data[:, 1] = np.unwrap(np.arctan2(data[:, 3], data[:, 2]) - angle)
        data = data[data[:, 1].argsort()]

        # print()
        # print(pts[current], current)
        # print(data)

        hh = LineString(hull) if len(hull) > 1 else None
        for i, a, _, _ in data:
            i = int(i)
            pt = tuple(pts[i])
            if hh and hh.crosses(LineString([hull[-1], pt])):
                continue

            hull.append(pt)
            current = i
            alive[current] = 0
            angle = a
            break
        else:
            return _concave_hull(pts, top, kk + 1)

    hh = Polygon(hull)
    if hh.covers(MultiPoint(pts)):
        return hh

    return _concave_hull(pts, top, kk + 1)
