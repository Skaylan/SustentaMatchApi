from app.config.app_config import *
from app.config.db_config import *
from app.models.tables.campaign import Campaign


class CampaignSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Campaign
        load_instance = True,
        fields = (
            'id', 
            'title', 
            'info_text', 
            'banner_img_uuid', 
            'created_at', 
            'updated_at', 
            'owner_id'
        )