from flask import request, redirect, url_for, session
from flask_mako import render_template

import asyncio

from app import app, db, s

pages = {
    'Home':'/home',
    'Scan':'/scan',
    'Devices':'/devices',
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
@app.route('/home')
@app.route('/index')
def index():

    return render_all('index.html')

@app.route('/scan')
def scan():
    res = Network.query.filter_by().all()
    return render_all('results.html', content=res)

@app.route('/update/<net:string>')
def update(net):
    # scan ip range and update db
    results = s.scan_network(net)
    for r in results:
        print(r)
    
    return redirect(url_for('index'))
