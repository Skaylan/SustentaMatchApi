from app import app
from app.models.tables.ogranization import Organization
import json

with app.test_client() as client:
    HEADERS = {"Content-Type": "application/json"}


    def test_get_organizations_route():
        body = client.get('/api/v1/get_organizations')
        _json = body.get_json()
        assert body.status_code == 200
        assert _json['status'] == 'ok'
    

    def test_create_organization_route():
        data_to_send = {
            "action_field": "1",
            "address": "pytest address",
            "cnpj": "00000000000000",
            "email": "pytest@email.com",
            "id": 2,
            "name": "Organização pytest",
            "organization_type": 1,
            "phone_number": "9999999999"
        }

        body = client.post(
            '/api/v1/create_organization', 
            data=json.dumps(data_to_send),
            headers=HEADERS)
        
        _json = body.get_json()

        assert body.status == '201 CREATED'
        assert _json['status'] == 'ok'