from app.config.app_config import *
from app.config.db_config import *


class ActionFields(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, unique=False, nullable=False)

    def __init__(
            self,
            title: str,
            description: str
    ):
        self.title = title
        self.description = description
