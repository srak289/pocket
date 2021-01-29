from app import db

class Network(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    addr = db.Column(db.String(24))
    hosts = db.relationship('Host', backref='network', cascade="all, delete-orphan")

class Host(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ports = db.relationship('Port', backref='host', cascade="all, delete-orphan")
    network_id = db.Column(db.String(32), db.ForeignKey('network.id'))
    addr = db.Column(db.String(16))

class Port(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.String, db.ForeignKey('host.id'))
    port_num = db.Column(db.Integer)
    port_stat = db.Column(db.String(32))

db.create_all()
