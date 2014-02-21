# -*- coding: utf-8 -*-

__all__ = ('TextField',)

class BaseField(object):
    CREATION_COUNT = 0
    
    def __init__(self, pos, origin=None):
        self.pos = pos
        self.origin = origin

        if origin:
            self.origin_args = origin.split('.')
        else:
            self.origin_args = None
        
        BaseField.CREATION_COUNT += 1
        self.creation_id = BaseField.CREATION_COUNT
    
    def get_value_from_instance(self, instance):
        if not self.origin_args:
            return

        lobj = instance
        for arg in self.origin_args:
            if isinstance(lobj, dict):
                lobj = lobj.get(arg)
            else:
                lobj = getattr(lobj, arg)

            if not lobj:
                return

        return lobj

    def clean(self, value):
        return value

    def write(self, page, instance):
        if hasattr(page, "get_%s" % self.name):
            value = getattr(page, "get_%s" % self.name)(obj)
        else:
            value = self.get_value_from_instance(instance)

        value = self.clean(value)
        self.draw(page, value)
        
class TextField(BaseField):
    def draw(self, page, value):
        page.canvas.drawString(self.pos[0], 900-self.pos[1], value)
