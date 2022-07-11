from typing import Union
import numpy as np

from shapely.geometry import Polygon, MultiPoint, LineString


def concave_hull(pts: np.ndarray, k: int = 3) -> Union[Polygon, None]:
    pts = np.array(list({(x, y) for x, y in pts}))
    if len(pts) < 3:
        return None

    if len(pts) == 3:
        return Polygon(pts)

    xs = pts[:, 0]
    ys = pts[:, 1]
    return _concave_hull(xs, ys, np.argmin(ys), k)


def _concave_hull(
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

    while (current != top or step == 2) and np.count_nonzero(alive) > 0:
        if step == 5:
            alive[top] = 1
        step += 1

        # consider only alive points
        alive_indices = np.arange(n)[alive == 1]

        # populate the delta columns
        deltax = xs[alive_indices] - xs[current]
        deltay = ys[alive_indices] - ys[current]

        # nearest neighbors
        #
        # TODO: in case of failure we could reuse the distances of the previous
        # run instead of calculating everything from scratch again
        dists = np.hypot(deltax, deltay)
        ixs = np.argpartition(dists, min(kk - 1, len(alive_indices) - 1))[:kk]

        alive_indices = alive_indices[ixs]
        # dists = dists[ixs]
        deltax = deltax[ixs]
        deltay = deltay[ixs]

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
            return _concave_hull(xs, ys, top, kk + 1)

    hh = Polygon(hull)
    if hh.covers(MultiPoint(list(zip(xs, ys)))):
        return hh

    return _concave_hull(xs, ys, top, kk + 1)
