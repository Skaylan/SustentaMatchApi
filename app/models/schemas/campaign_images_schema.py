from app.config.app_config import *
from app.config.db_config import *
from app.models.tables.campaign_images import CampaignImages

class CampaignImagesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CampaignImages
        load_instance = True,
        fields = (
            'id',
            'img_uuid',
            'campaign_id',
            'created_at' 
        )