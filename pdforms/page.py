# -*- coding: utf-8 -*-

__all__ = ('Page',)

from .fields import BaseField

from pyPdf import PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
    
class PageType(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(PageType, cls).__new__
        metaclass = attrs.get('__metaclass__')

        if metaclass and issubclass(metaclass, PageType):
            return super_new(cls, name, bases, attrs)

        fields = {}

        for attr_name, attr_value in attrs.iteritems():
            if not isinstance(attr_value, BaseField):
                continue

            attr_value.name = attr_name
            fields[attr_name] = attr_value

        attrs['_fields'] = fields
        attrs['_order_fields'] = sorted(
            fields.values(), key=lambda x: x.creation_id)

        return super_new(cls, name, bases, attrs)

class Page(object):
    __metaclass__ = PageType
    
    def __init__(self, instance):
        self.instance = instance

    def save(self):
        packet = StringIO()
        self.canvas = canvas.Canvas(packet, pagesize=A4)

        for field in self._order_fields:
            field.write(self, self.instance)

        self.canvas.save()
        
        packet.seek(0)
        new_pdf = PdfFileReader(packet)

        return new_pdf.getPage(0)
