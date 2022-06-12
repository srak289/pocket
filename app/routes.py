from flask import request, redirect, url_for, session, send_file
import os

from . import app, sqldriver
from .models import *

from .scanner import Scanner
from .utils import render_template

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
            sqldriver.create(
                Network,
                name=safe['name'],
                addr=safe['addr']
            )
            return redirect(url_for('networks'))
        else:
                # this should do an error thing
                # check morningbrew login for code
            return redirect(url_for('networks'))
    else:
        networks = sqldriver.read(Network)
        print(f'Found {networks}')
        return render_all('networks.html', networks=networks)

@app.route('/network/<int:id>')
def network(id):
    n = sqldriver.read(Network, id=id)[0]
    print(f'Page for network {n}')
    hosts = sqldriver.read(Host, network_id=n.id)
    return render_all('network.html', Port=Port, n=n, hosts=hosts)

@app.route('/delete/network/<int:id>')
def del_network(id):
    n = sqldriver.delete(Network, id=id)[0]
    return redirect(url_for('index'))

@app.route('/results')
def results():
    res = sqldriver.read(Network)
    return render_all('results.html', content=res)

@app.route('/devices')
def devices():
    res = sqldriver.read(Hosts)
    return render_all('devices.html', content=res)

@app.route('/report/<int:id>')
def report(id):
    hosts = sqldriver.read(Host, network_id=id)
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
    n = sqldriver.read(Network, id=id)[0]
    s = Scanner(n.addr)
    results = s.scan_network()
    for r in results:
        h = sqldriver.create(
            Host,
            addr=r['host'],
            network_id=n.id
        )
        for p in r['ports']:
            x = sqldriver.create(
                Port,
                host_id=h.id,
                port_num=p['port'],
                port_stat=p['status']
            )
    return redirect(f'/network/{id}')

@app.route('/hosts', methods=['GET', 'POST'])
def hosts():
    if request.method == 'POST':
        safe = strip(request.method)
        sqldriver.create(Host,
            name=safe['name'],
            addr=safe['addr']
        )
    else:
        hosts = sqldriver.read(Host)
        return render_all('hosts.html', hosts=hosts)

@app.route('/host/<int:id>')
def host(id):
    h = sqldriver.read(Host, id=id)[0]
    ports = sqldriver.read(Port, host_id=h.id)
    return render_all('host.html', host=h, ports=ports)

@app.route('/delete/host/<int:id>')
def del_host(id):
    h = sqldriver.delete(Host, id=id)
    return redirect(url_for('index'))

