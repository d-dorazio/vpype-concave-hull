from typing import List, Optional, Union

import click
import vpype as vp
import vpype_cli

from . import concave_hull


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
def vpype_concave_hull(
    document: vp.Document, layer: Union[int, List[int]], target_layer: Optional[int]
) -> vp.Document:
    new_document = document.empty_copy(keep_layers=True)
    if target_layer is vpype_cli.LayerType.NEW:
        target_layer = new_document.free_id()

    layer_ids = vpype_cli.multiple_to_layer_ids(layer, document)
    for lid in layer_ids:
        lines = document.layers[lid]
        pts = [(p.real, p.imag) for line in lines for p in line]

        new_document.add(lines, layer_id=lid)

        chull = concave_hull(pts)
        if chull is not None and chull.exterior is not None:
            new_document.add(
                [chull.exterior], layer_id=lid if target_layer is None else target_layer
            )

    return new_document
