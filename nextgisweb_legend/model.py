# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from shutil import copyfileobj

from nextgisweb import db
from nextgisweb.env import env
from nextgisweb.file_storage import FileObj
from nextgisweb.models import declarative_base
from nextgisweb.render import IRenderableStyle
from nextgisweb.resource import DataScope, Resource, ResourceScope, Serializer, SerializedProperty

from .util import _

Base = declarative_base()


class LegendSprite(Base, Resource):
    identity = 'legend_sprite'
    cls_display_name = _("Legend")

    __scope__ = DataScope

    description_fileobj_id = db.Column(db.Integer, db.ForeignKey(FileObj.id), nullable=True)
    description_fileobj = db.relationship(FileObj, foreign_keys=[description_fileobj_id])

    image_fileobj_id = db.Column(db.Integer, db.ForeignKey(FileObj.id), nullable=True)
    image_fileobj = db.relationship(FileObj, foreign_keys=[image_fileobj_id, ])

    @classmethod
    def check_parent(cls, parent):
        return IRenderableStyle.providedBy(parent)


DataScope.read.require(
    DataScope.read,
    attr='parent', cls=LegendSprite)


class _description_file_attr(SerializedProperty):  # NOQA

    def setter(self, srlzr, value):
        srcfile, _ = env.file_upload.get_filename(value['id'])
        fileobj = env.file_storage.fileobj(component='legend')
        srlzr.obj.description_fileobj = fileobj
        dstfile = env.file_storage.filename(fileobj, makedirs=True)

        with open(srcfile, 'r') as fs, open(dstfile, 'w') as fd:
            copyfileobj(fs, fd)


class _image_file_attr(SerializedProperty):  # NOQA

    def setter(self, srlzr, value):
        srcfile, _ = env.file_upload.get_filename(value['id'])
        fileobj = env.file_storage.fileobj(component='legend')
        srlzr.obj.image_fileobj = fileobj
        dstfile = env.file_storage.filename(fileobj, makedirs=True)

        with open(srcfile, 'r') as fs, open(dstfile, 'w') as fd:
            copyfileobj(fs, fd)


class LegendSerializer(Serializer):
    identity = LegendSprite.identity
    resclass = LegendSprite

    description_file = _description_file_attr(read=None, write=ResourceScope.update)
    image_file = _image_file_attr(read=None, write=ResourceScope.update)
