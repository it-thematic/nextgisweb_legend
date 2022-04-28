# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from json import dumps, loads

from pyramid.response import FileResponse, Response
from pyramid.httpexceptions import HTTPBadRequest

from nextgisweb.env import env
from nextgisweb.resource import resource_factory, ResourceScope, Resource
from nextgisweb.models import DBSession

from .model import LegendSprite


def legend(request):
    if 'styles' not in request.GET.keys():
        raise HTTPBadRequest("Parameter 'styles' not found.")
    try:
        styles = map(int, request.GET.getall('styles'))
    except ValueError:
        raise HTTPBadRequest("Invalid 'styles' parameter. Only numbers.")

    result = []

    legend_list = DBSession.query(Resource).filter(Resource.parent_id.in_(styles)).order_by(Resource.parent_id, Resource.display_name)

    for legend in legend_list:
        legend_description = env.file_storage.filename(legend.description_fileobj)
        with open(legend_description, mode='r') as f:
            description = loads(f.read(), encoding='utf-8')
            if type(description) != list:
                description = list(description)
            element = dict(
                id=legend.id,
                type='legend',
                legend_id=legend.id,
                style_id=legend.parent.id,
                name=legend.display_name or legend.keyname,
                children=description
            )
            result.append(element)

    return Response(dumps(result), content_type='application/json', charset='utf-8')


def description_file(request):
    request.resource_permission(ResourceScope.read)

    fn = env.file_storage.filename(request.context.description_fileobj)

    response = FileResponse(fn, request=request)
    response.content_disposition = ('attachment; filename=%d.json' % request.context.id)

    return response


def image_file(request):
    request.resource_permission(ResourceScope.read)

    fn = env.file_storage.filename(request.context.image_fileobj)

    response = FileResponse(fn, request=request)
    response.content_disposition = ('attachment; filename=%d.png' % request.context.id)

    return response


def setup_pyramid(comp, config):
    config.add_route(
        'legend.legend', '/api/resource/legend',
    ).add_view(legend, request_method='GET')

    config.add_route(
        'legend.description', r'/api/resource/{id:\d+}/legend/description',
        factory=resource_factory
    ).add_view(description_file, context=LegendSprite, request_method='GET')

    config.add_route(
        'legend.image', r'/api/resource/{id:\d+}/legend/image',
        factory=resource_factory
    ).add_view(image_file, context=LegendSprite, request_method='GET')
