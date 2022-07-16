from typing import List, Optional, Union

import click
import vpype as vp
import vpype_cli

from . import concave_hull_knn


@click.command()
@click.option(
    "-l",
    "--layer",
    type=vpype_cli.LayerType(accept_multiple=True),
    default="all",
    help="Source layer(s).",
)
@click.option(
    "-t",
    "--target-layer",
    type=vpype_cli.LayerType(accept_new=True),
    help="Target layer.",
)
@vpype_cli.global_processor
def concave_hull(
    document: vp.Document, layer: Union[int, List[int]], target_layer: Optional[int]
) -> vp.Document:
    """
    Find the concave hull of a set of points.

    The concave hull is calculated from each layer separately and saved by
    default in the same layer. You can specify which layer(s) to use with
    the `--layer` argument and where to store the concave hulls with the
    `target-layer` argument.

    Args:
        document: the vpype.Document to work on.
        layer: which layer(s) to work on.Default: all.
        target_layer: in which layer to save the concave hull(s).
        Default: the same as the layer used to find the concave hull.
    Examples:
        - Basic usage:
            $ vpype random -a 10cm 10cm concave-hull show
            $ vpype random -a 10cm 10cm concave-hull -t NEW show
    """
    new_document = document.empty_copy(keep_layers=True)
    if target_layer is vpype_cli.LayerType.NEW:
        target_layer = new_document.free_id()

    layer_ids = vpype_cli.multiple_to_layer_ids(layer, document)
    for lid in layer_ids:
        lines = document.layers[lid]
        pts = [(p.real, p.imag) for line in lines for p in line]

        new_document.add(lines, layer_id=lid)

        chull = concave_hull_knn(pts)
        if chull is not None and chull.exterior is not None:
            new_document.add(
                [chull.exterior], layer_id=lid if target_layer is None else target_layer
            )

    return new_document


concave_hull.help_group = "Plugins"
