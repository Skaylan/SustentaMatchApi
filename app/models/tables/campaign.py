from app.config.app_config import *
from app.config.db_config import *
from datetime import datetime

class Campaign(db.Model):
    __tablename__='campaign'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False, nullable=False)
    info_text = db.Column(db.Text, unique=False, nullable=False)
    banner_img_uuid = db.Column(db.String(40), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    image = db.relationship('CampaignImages', backref='imgowner')
    owner_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)

    def __init__(
        self,
        title: str,
        info_text: str,
        owner_id: int,
        banner_img_uuid: str
    ) -> None:
        self.title = title
        self.info_text = info_text
        self.owner_id = owner_id
        self.banner_img_uuid = banner_img_uuid