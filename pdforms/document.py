__all__ = ('Document',)



from pyPdf import PdfFileWriter, PdfFileReader
from .fields import BaseField

class Document(object):
    pages = []
    origin = None
    
    def __init__(self, instance):
        self.instance = instance

    def get_origin(self):
        return self.origin
    
    def save(self, to):
        origin = self.get_origin()
        
        if not origin:
            raise RuntimeError("Please implement get_origin method or origin attribute")

        try:
            existing_pdf = PdfFileReader(file(origin, "rb"))
        except IOError:
            raise RuntimeError(u"Failed to open origin file")

        output = PdfFileWriter()
                
        for page_id, page_class in enumerate(self.pages):
            new_page = page_class(self.instance).save()
            
            base_page = existing_pdf.getPage(0)
            base_page.mergePage(new_page)
            output.addPage(base_page)

        if isinstance(to, basestring):
            outputStream = file(to, "wb")
        else:
            outputStream = to
        
        output.write(outputStream)
        outputStream.close()
