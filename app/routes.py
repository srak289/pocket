from flask import request, redirect, url_for, session
from flask_mako import render_template
from functools import wraps
from app import app, db
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

app_cls = []
[ app_cls.append(cls) for cls in db.Model._decl_class_registry.values() if isinstance(cls, type) and issubclass(cls, db.Model) ]

def exec_cls(f):
    @wraps(f)
    def decorated_function(cls, *args, **kwargs):
        for clss in app_cls:
            if cls.capitalize() == clss.__name__:
                cls = clss
                break
            else:
                cls = None
                    # should probably raise exception
                print(f'ERROR {name} is None')
                return redirect(url_for('index'))
        return f(cls=cls, *args, **kwargs)
    return decorated_function

#def login_req(func):
#    @wraps(func)
#    def decorated_function(*args, **kwargs):
#        if 'user' not in session:
#            print('no user in session')
#            return redirect(url_for('login'))
#        else:
#            print(f'User {session["user"]} in session')
#        return func(*args, **kwargs)
#    return decorated_function

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
        n = Network(name=safe['name'], addr=safe['addr'])
        print(f'Adding {n}')
        db.session.add(n)
        db.session.commit()
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
    return render_all('network.html', n=n, hosts=hosts)

@app.route('/delete/network/<int:id>')
def del_network(id):
    n = Network.query.filter_by(id=id).one()
    db.session.delete(n)
    db.session.commit()
    return redirect(url_for('index'))

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
    db.session.remove(n)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/result')
def result():
    res = Network.query.all()
    return render_all('results.html', content=res)

@app.route('/update/network/<int:id>')
def update_network(id):
    n = Network.query.filter_by(id=id).one()
    s = Scanner(n.addr)
    results = s.scan_network()
    for r in results:
        h = Host(network_id=n.id, addr=r['host'])
        db.session.add(h)
        for p in r['ports']:
            x = Port(host_id=h.id, port_num=p['port'], port_stat=p['status'])
            db.session.add(x)
    db.session.commit()
    return render_all('results.html', content=results)

@app.route('/<string:name>')
def read_many(name):
    if name[:-1] == 's':
        if request.method == 'POST':
            safe = strip(request.method)
            db.session.add(Host(name=safe['name'], addr=safe['addr']))
        else:
            hosts = Host.query.all()
            return render_all('hosts.html', hosts=hosts)
    else:
        pass

@app.route('/class/<string:cls>')
@exec_cls
def test(cls):
    print(f'---{cls}---')
    if cls is not None:
        print(cls.query.all())
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/<string:name>/<int:id>')
def read_one(name, id):
    h = Host.query.filter_by(id=id).one()
    ports = Port.query.filter_by(host_id=h.id).all()
    return render_all('host.html', host=h, ports=ports)

@app.route('/update/<string:name>/<int:id>')
def update_one(name, id):
    pass

@app.route('/delete/<string:name>/<int:id>')
def delete_one(name, id):
    h = Host.query.filter_by(id=id).one()
    db.session.remove(n)
    db.session.commit()
    return redirect(url_for('index'))
