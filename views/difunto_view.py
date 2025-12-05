from flask import render_template

def list(difuntos):
    return render_template("difuntos/index.html", difuntos=difuntos)

def create():
    return render_template('difuntos/create.html')

def edit(difunto):
    return render_template('difuntos/edit.html', difunto=difunto)
