# views/pago_view.py
from flask import render_template

def list(pagos):
    return render_template('pagos/index.html', pagos=pagos)

def create(servicios, usuarios):
    # servicios: lista de servicios a pagar, usuarios si necesitas ver quien registra
    return render_template('pagos/create.html', servicios=servicios, usuarios=usuarios)

def edit(pago, servicios, usuarios):
    return render_template('pagos/edit.html', pago=pago, servicios=servicios, usuarios=usuarios)

def recibo(pago):
    return render_template('pagos/recibo.html', pago=pago)
