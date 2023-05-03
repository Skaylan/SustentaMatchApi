from app.config.app_config import *
from app.config.db_config import *
from app.models.tables.ogranization import Organization


class OrganizationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Organization
        load_instance = True,
        fields = [
            'id', 
            'name', 
            'cnpj', 
            'phone_number', 
            'email', 
            'address', 
            'organization_type', 
            'action_field',
            'created_at',
            'updated_at'
        ]