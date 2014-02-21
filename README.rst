======
PDForm
======

A simple tool to fill forms in pdf format!.

Dependencies
============
- pyPDF

Example
=======

    import pdforms

    class Page01(pdforms.Page):
        nome_pessoa = pdforms.TextField(
            pos=(80, 189),
            origin="pessoa.nome")

        nome_unidade = pdforms.TextField(
            pos=(175, 213),
            origin="unidade.nome")

    class MyDocument(pdforms.Document):
        pages = (Page01,)
       origin = "origin.pdf"


    obj = {'pessoa': {'nome': "Wilson Pinto Junior"},
           'unidade': {'nome': "CRAS centro"}}
    
    MyDocument(obj).save('destination.pdf')
