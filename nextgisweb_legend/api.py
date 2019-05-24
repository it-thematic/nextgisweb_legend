# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyramid.response import FileResponse

from nextgisweb.env import env
from nextgisweb.resource import resource_factory, DataScope

from .model import LegendSprite


def legend(request):
    pass


def description_file(request):
    request.resource_permission(DataScope.read)

    fn = env.file_storage.filename(request.context.description_fileobj)

    response = FileResponse(fn, request=request)
    response.content_disposition = (b'attachment; filename=%d.qml'
                                    % request.context.id)


def image_file(request):
    request.resource_permission(DataScope.read)

    fn = env.file_storage.filename(request.context.image_fileobj)

    response = FileResponse(fn, request=request)
    response.content_disposition = (b'attachment; filename=%d.qml'
                                    % request.context.id)


def setup_pyramid(comp, config):
    config.add_route('legend.legend', '/api/resource/{id}/legend', factory=resource_factory).add_view(
        legend, context=LegendSprite, request_method='GET'
    )

    config.add_route('legend.description', '/api/resource/{id}/legend/description', factory=resource_factory).add_view(
        description_file, context=LegendSprite, request_method='GET'
    )

    config.add_route('legend.image', '/api/resource/{id}/legend/image', factory=resource_factory).add_view(
        image_file, context=LegendSprite, request_method='GET'
    )
