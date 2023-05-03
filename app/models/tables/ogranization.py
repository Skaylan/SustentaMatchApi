from app.config.app_config import *
from app.config.db_config import *
from app.models.tables.connections import *
from datetime import datetime


class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    cnpj = db.Column(db.String(14), unique=True, nullable=False)
    address = db.Column(db.Text, unique=True, nullable=False)
    phone_number = db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    organization_type = db.Column(db.Integer, unique=False, nullable=False)
    action_field = db.Column(db.String(100), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    # connections = db.relationship('Connections', backref='conn')


    def __init__(
        self, 
        name: str, 
        cnpj: str, 
        address: str, 
        phone_number: str, 
        email: str, 
        organization_type: int,
        action_field: str
    ):
        self.name = name
        self.cnpj = cnpj
        self.address = address
        self.phone_number = phone_number
        self.email = email
        self.organization_type = organization_type
        self.action_field = action_field