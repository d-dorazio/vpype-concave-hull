from typing import Iterable, Union

import numpy as np
from scipy.spatial import KDTree
from shapely.geometry import LineString, MultiPoint, Polygon


def concave_hull_knn(pts: Iterable[tuple[float, float]], k: int = 3) -> Union[Polygon, None]:
    pts = np.array(list({(x, y) for x, y in pts}))
    if len(pts) < 3:
        return None

    if len(pts) == 3:
        return Polygon(pts)

    xs = pts[:, 0]
    ys = pts[:, 1]
    return _concave_hull_knn(xs, ys, np.argmin(ys), k)


def _concave_hull_knn(
    xs: np.ndarray, ys: np.ndarray, top: int, kk: int = 3
) -> Union[Polygon, None]:
    n = len(xs)

    kk = max(3, kk)
    if kk > n:
        return None

    alive = np.ones(n, dtype=int)

    hull = [(xs[top], ys[top])]
    current = top
    alive[current] = 0

    angle = np.pi
    step = 2

    index = KDTree(list(zip(xs, ys)))
    index_to_world = np.arange(n, dtype=int)

    while (current != top or step == 2) and np.count_nonzero(alive) > 0:
        if step == 5:
            alive[top] = 1
        step += 1

        # nearest neighbors
        for j in range(2):
            nn = kk * (1 + (1 - j) * 5)
            _, ixs = index.query((xs[current], ys[current]), nn)
            ixs = np.array([i for i in ixs if i < index.n and alive[index_to_world[i]]])[:kk]
            if len(ixs) >= kk:
                break

            index_to_world = np.array([i for i in index_to_world if alive[i]])
            index = KDTree([(xs[i], ys[i]) for i in index_to_world])

        alive_indices = index_to_world[ixs]

        # populate the delta columns
        deltax = xs[alive_indices] - xs[current]
        deltay = ys[alive_indices] - ys[current]

        # sort by right hand turn
        angles = np.unwrap(np.arctan2(deltay, deltax) - angle)
        ixs = np.argsort(angles)

        hh = LineString(hull) if len(hull) > 1 else None
        for ix in ixs:
            i = alive_indices[ix]

            pt = (xs[i], ys[i])
            if hh and hh.crosses(LineString([hull[-1], pt])):
                continue

            hull.append(pt)
            current = i
            alive[current] = 0
            angle = angles[ix]
            break
        else:
            return _concave_hull_knn(xs, ys, top, kk + 1)

    hh = Polygon(hull)
    if hh.covers(MultiPoint(list(zip(xs, ys)))):
        return hh

    return _concave_hull_knn(xs, ys, top, kk + 1)
