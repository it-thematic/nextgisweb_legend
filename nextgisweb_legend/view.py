from nextgisweb.env import _
from nextgisweb.lib import dynmenu as dm
from nextgisweb.resource import Widget, Resource

from .model import LegendSprite


class Widget(Widget):
    resource = LegendSprite
    operation = ('create', 'update')
    amdmod = "@nextgisweb/legend/editor-widget"


def setup_pyramid(comp, config):
    class LayerMenuExt(dm.DynItem):
        def build(self, args):
            if isinstance(args.obj, LegendSprite):
                yield dm.Label("legend_sprite", _("Legend"))

                yield dm.Link(
                    "legend_sprite/description",
                    _("Description file"),
                    lambda args: args.request.route_url('legend.description', id=args.obj.id))

                yield dm.Link(
                    "legend_sprite/image",
                    _("Image file"),
                    lambda args: args.request.route_url("legend.image", id=args.obj.id))

    Resource.__dynmenu__.add(LayerMenuExt())
