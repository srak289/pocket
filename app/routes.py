from flask import request, redirect, url_for, session
from flask_mako import render_template

import asyncio

from scanner import Scanner

from app import app, db
from app.models import Device

pages = {
    'Devices':'/',
}

html_escape_table = {
    '&': '&amp;',
    '"': '&quot;',
    "'": '&apos;',
    '>': '&gt;',
    '<': '&lt;'
}

def render_all(t, **kwargs):
    return render_template(t, **kwargs, pages=pages)

def strip(d):
    safe = {}
    for k, v in d.items():
        v = "".join(html_escape_table.get(c, c) for c in v)
        safe.update({k:v})

    return safe

@app.route('/')
def index():
    devices = Device.query.filter_by().all()

    return render_all('device.html', devices)

@app.route('/update')
def update():
    # scan ip range and update db
    
    return redirect(url_for('index'))
