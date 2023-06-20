from app.config.app_config import *
from app.config.db_config import *
from app.models.tables.connections import *
from datetime import datetime


class Organization(db.Model):
    __tablename__ = 'organization'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    cnpj = db.Column(db.String(14), unique=True, nullable=False)
    street_name = db.Column(db.Text, unique=False, nullable=False)
    city = db.Column(db.Text, unique=False, nullable=False)
    cep = db.Column(db.String(8), unique=False, nullable=False)
    number = db.Column(db.String(10), unique=False, nullable=False)
    state_name = db.Column(db.String(100), unique=False, nullable=False)
    phone_number = db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.Text, unique=False, nullable=False)
    organization_type = db.Column(db.String(100), unique=False, nullable=False)
    action_field = db.Column(db.String(100), unique=False, nullable=False)
    profile_image_uuid = db.Column(db.String(100), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    campaign = db.relationship('Campaign', backref='owner')



    def __init__(
        self, 
        name: str, 
        cnpj: str,
        street_name: str,
        cep: str,
        number: str,
        city: str,
        state_name: str,
        phone_number: str, 
        email: str,
        password_hash: str,
        organization_type: str,
        action_field: str,
        profile_image_uuid:str
    ):
        self.name = name
        self.cnpj = cnpj
        self.street_name = street_name
        self.cep = cep
        self.number = number
        self.city = city
        self.state_name = state_name
        self.phone_number = phone_number
        self.email = email
        self.password_hash = password_hash
        self.organization_type = organization_type
        self.action_field = action_field
        self.profile_image_uuid = profile_image_uuid