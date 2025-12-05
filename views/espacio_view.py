from flask import render_template

def list(espacios):
    return render_template('espacios/index.html', espacios = espacios)

def create():
    return render_template('espacios/create.html')

def edit(espacio):
    return render_template('espacios/edit.html', espacio=espacio)

