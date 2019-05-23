# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from nextgisweb.component import Component, require

from .model import Base
from .util import COMP_ID


class LegendComponent(Component):
    identity = COMP_ID
    metadata = Base.metadata

    @require('resource')
    def setup_pyramid(self, config):
        from . import view, api
        view.setup_pyramid(self, config)
        api.setup_pyramid(self, config)


def pkginfo():
    return dict(components=dict(
        legend='nextgisweb_legend'))


def amd_packages():
    return (
        ('ngw-legend', 'nextgisweb_legend:amd/ngw-legend'),
    )
