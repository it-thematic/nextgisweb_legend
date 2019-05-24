# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import nextgisweb.dynmenu as dm
from nextgisweb.resource import Widget, Resource

from .model import LegendSprite
from .util import _


class Widget(Widget):
    resource = LegendSprite
    operation = ('create', 'update')
    amdmod = 'ngw-legend/LegendWidget'


def setup_pyramid(comp, config):
    class StyleMenuExt(dm.DynItem):
        def build(self, args):
            if isinstance(args.obj, LegendSprite):
                yield dm.Label('legend_sprite', _(u"Legend"))

                if args.obj.description_fileobj is not None:
                    yield dm.Link('legend_sprite/description', _(u"Description file"),
                                  lambda args: args.request.route_url('legend.description', id=args.obj.id))

                if args.obj.image_fileobj is not None:
                    yield dm.Link('legend_sprite/image', _(u"Image file"),
                                  lambda args: args.request.route_url("legend.image", id=args.obj.id))

    Resource.__dynmenu__.add(StyleMenuExt())
