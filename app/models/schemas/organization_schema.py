from app.config.app_config import *
from app.config.db_config import *
from app.models.tables.ogranization import Organization
from app.models.schemas.campaign_schema import CampaignSchema

class OrganizationSchema(ma.SQLAlchemyAutoSchema):
    campaigns = ma.Nested(CampaignSchema, many=True)
    class Meta:
        model = Organization
        load_instance = True,
        # fields = [
        #     'id', 
        #     'name', 
        #     'cnpj', 
        #     'phone_number', 
        #     'email', 
        #     'address', 
        #     'organization_type', 
        #     'action_field',
        #     'created_at',
        #     'updated_at',
        #     'campaign'
        # ]