# from app.config.app_config import *
# from app.config.db_config import *
# from datetime import datetime

# class Connections(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     organization_ong_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)
#     organization_company_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)
#     created_at = db.Column(db.DateTime(), default=datetime.now())
#     updated_at = db.Column(db.DateTime(), default=datetime.now())


#     def __init__(
#             self,
#             organizarion_ong_id: int,
#             organization_company_id: int
#     ):
#         self.organization_ong_id = organizarion_ong_id
#         self.organization_company_id = organization_company_id