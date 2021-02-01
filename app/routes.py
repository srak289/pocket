from flask import request, redirect, url_for, session, send_file
from flask_mako import render_template
import pdb
import os

import asyncio

from app import app, db, s, path
from app.models import *

from app.scanner import Scanner

pages = {
    'Home':'/home',
    'Results':'/results',
    'Devices':'/devices',
    'Networks':'/networks'
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

    return render_all('index.html', content='lol')

@app.route('/networks', methods=['GET', 'POST'])
def networks():
    if request.method == 'POST':
        safe = strip(request.form)
        if s.check_network(safe['addr']):
            n = Network(name=safe['name'], addr=safe['addr'])
            db.session.add(n)
            db.session.commit()
            return redirect(url_for('networks'))
        else:
                # this should do an error thing
                # check morningbrew login for code
            return redirect(url_for('networks'))
    else:
        networks = Network.query.all()
        print(f'Found {networks}')
        return render_all('networks.html', networks=networks)

@app.route('/network/<int:id>')
def network(id):
    n = Network.query.filter_by(id=id).one()
    print(f'Page for network {n}')
    hosts = Host.query.filter_by(network_id=n.id).all()
    return render_all('network.html', Port=Port, n=n, hosts=hosts)

@app.route('/delete/network/<int:id>')
def del_network(id):
    n = Network.query.filter_by(id=id).one()
    db.session.delete(n)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/result')
def result():
    res = Network.query.all()
    return render_all('results.html', content=res)

@app.route('/report/<int:id>')
def report(id):
    hosts = Host.query.filter_by(network_id=id).all()
    for i in hosts:
        print(i)    
    tmp = os.path.join(path, 'templates/tmp.csv')
    with open(tmp, 'wb') as f:
        f.write(render_template('report.csv', hosts=hosts, Port=Port))
    print(open(tmp, 'rb').read())
    return send_file(tmp)

@app.route('/update/network/<int:id>')
def update_network(id):
    # scan ip range and update db
    n = Network.query.filter_by(id=id).one()
    s = Scanner(n.addr)
    results = s.scan_network()
    for r in results:
        h = Host(addr=r['host'], network_id=n.id)
        db.session.add(h)
        db.session.commit()
        for p in r['ports']:
            x = Port(host_id=h.id, port_num=p['port'], port_stat=p['status'])
            db.session.add(x)
        db.session.commit()
    return redirect(f'/network/{id}')

@app.route('/hosts', methods=['GET', 'POST'])
def hosts():
    if request.method == 'POST':
        safe = strip(request.method)
        db.session.add(Host(name=safe['name'], addr=safe['addr']))
    else:
        hosts = Host.query.all()
        return render_all('hosts.html', hosts=hosts)

@app.route('/host/<int:id>')
def host(id):
    h = Host.query.filter_by(id=id).one()
    ports = Port.query.filter_by(host_id=h.id).all()
    return render_all('host.html', host=h, ports=ports)

@app.route('/delete/host/<int:id>')
def del_host(id):
    h = Host.query.filter_by(id=id).one()
    db.session.remove(h)
    db.session.commit()
    return redirect(url_for('index'))

