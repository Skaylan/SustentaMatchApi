from app.config.app_config import *
from app.config.db_config import *
from datetime import datetime


class CampaignImages(db.Model):
    __tablename__='campaign_images'
    id = db.Column(db.Integer, primary_key=True)
    img_uuid = db.Column(db.String(40), unique=True, nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())

    def __init__(
        self,
        title: str,
        info_text: str,
        campaign_id: int,
        img_uuid: str
    ) -> None:
        self.title = title
        self.info_text = info_text
        self.campaign_id = campaign_id
        self.img_uuid = img_uuid