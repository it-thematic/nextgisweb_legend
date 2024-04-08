from json import loads, dumps
from shutil import copyfileobj
from uuid import uuid4

import zope.event.classhandler

from nextgisweb.env import Base, _, env
from nextgisweb.lib import db
from nextgisweb.file_storage import FileObj

from nextgisweb.resource import (
    DataScope,
    Resource,
    ResourceScope,
    Serializer,
    SerializedProperty,
    ValidationError,
)
from nextgisweb.resource.events import (
    AfterResourceCollectionPost,
    AfterResourcePut,
)


class LegendSprite(Base, Resource):
    identity = 'legend_sprite'
    cls_display_name = _("Legend")

    __scope__ = DataScope

    description_fileobj_id = db.Column(db.Integer, db.ForeignKey(FileObj.id), nullable=True)
    description_fileobj = db.relationship(FileObj, foreign_keys=[description_fileobj_id], cascade='all')

    image_fileobj_id = db.Column(db.Integer, db.ForeignKey(FileObj.id), nullable=True)
    image_fileobj = db.relationship(FileObj, foreign_keys=[image_fileobj_id], cascade='all')

    @classmethod
    def check_parent(cls, parent):
        return isinstance(parent, Resource)


class _description_file_attr(SerializedProperty):  # NOQA

    def setter(self, srlzr, value):
        srcfile, _ = env.file_upload.get_filename(value['id'])
        fileobj = env.file_storage.fileobj(component='legend')
        srlzr.obj.description_fileobj = fileobj
        dstfile = env.file_storage.filename(fileobj, makedirs=True)

        with open(srcfile, 'r') as fs, open(dstfile, 'w') as fd:
            desc = loads(fs.read(), encoding='utf-8')
            if not isinstance(desc, list):
                raise ValidationError(_('Legend\'s description must be a list'))
            fd.write(dumps((desc)))


class _image_file_attr(SerializedProperty):  # NOQA

    def setter(self, srlzr, value):
        srcfile, _ = env.file_upload.get_filename(value['id'])
        fileobj = env.file_storage.fileobj(component='legend')
        srlzr.obj.image_fileobj = fileobj
        dstfile = env.file_storage.filename(fileobj, makedirs=True)

        with open(srcfile, 'rb') as fs, open(dstfile, 'wb') as fd:
            copyfileobj(fs, fd)


class LegendSpriteSerializer(Serializer):
    identity = LegendSprite.identity
    resclass = LegendSprite

    description_file = _description_file_attr(read=None, write=ResourceScope.update)
    image_file = _image_file_attr(read=None, write=ResourceScope.update)


def normalize_description(desc, legend_id):
    """
    Фунция нормализации идентификаторов объектов

    Если такого поля нет, то она его добавит. Иначе изменит существующие значение на uuid

    :param dict desc:
    :param int legend_id: идентификатор ресурса легенды
    :return:
    """
    desc['id'] = str(uuid4())
    desc['legend_id'] = legend_id
    desc.setdefault('children', [])
    for child in desc['children']:
        normalize_description(child, legend_id=legend_id)


def on_normalize_resource(resource):
    with open(env.file_storage.filename(resource.description_fileobj), 'r') as fs:
        desc = loads(fs.read(), encoding='utf-8')
    for el in desc:
        normalize_description(el, legend_id=resource.id)

    with open(env.file_storage.filename(resource.description_fileobj), 'w') as fd:
        fd.write(dumps(desc))


@zope.event.classhandler.handler(AfterResourceCollectionPost)
def on_item_post(event):
    """
    Событие после создания ресурса

    :param AfterResourceCollectionPost event:
    :return:
    """
    if event.resource.identity == LegendSprite.identity:
        on_normalize_resource(event.resource)


@zope.event.classhandler.handler(AfterResourcePut)
def on_item_post(event):
    """
    Событие после обновления ресурса

    :param AfterResourcePut event:
    :return:
    """
    if event.resource.identity == LegendSprite.identity:
        on_normalize_resource(event.resource)
