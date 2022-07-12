import vsketch

import datetime
import alphashape


from vpype_concave_hull import concave_hull_knn

import numpy as np


class ExampleSketch(vsketch.SketchClass):
    # Sketch parameters:
    # radius = vsketch.Param(2.0)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        # vsk.randomSeed(188032766)
        # vsk.randomSeed(896598421)
        # pts = [(vsk.random(18), vsk.random(21)) for _ in range(5)]

        # vsk.randomSeed(66436237)
        # pts = [(vsk.random(18), vsk.random(21)) for _ in range(6)]

        # pts = [
        #     (0, 0),
        #     (10, 0),
        #     (0, 10),
        #     (10, 10),
        # ]

        pts = [(vsk.random(18), vsk.random(21)) for _ in range(1000)]

        for x, y in pts:
            vsk.circle(x, y, 0.5)

        start = datetime.datetime.now()
        a = alphashape.alphashape(pts, 0.9)
        print(datetime.datetime.now() - start)

        start = datetime.datetime.now()
        a = concave_hull_knn(np.asarray(pts))
        print(datetime.datetime.now() - start)

        if a is not None:
            coords = list(a.exterior.coords)
            vsk.circle(coords[0][0], coords[0][1], 0.25)
            for i in range(len(coords)):
                # vsk.geometry(a)
                vsk.stroke(i + 2)
                vsk.line(*coords[i], *coords[(i + 1) % len(coords)])

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    ExampleSketch.display()
