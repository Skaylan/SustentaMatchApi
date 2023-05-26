from app import app
from app.models.tables.ogranization import Organization
import json

with app.test_client() as client:
    HEADERS = {"Content-Type": "application/json"}


    def test_get_organizations_route():
        response = client.get('/api/v1/get_organizations')
        body = response.get_json()
        assert response.status_code == 200
        assert body['status'] == 'ok'
    

    def test_create_organization_route():
        data_to_send = {
            "action_field": "1",
            "address": "pytest address",
            "cnpj": "00000000000000",
            "email": "test_org@email.com",
            'password': '123456789',
            "name": "Organização pytest",
            "organization_type": 1,
            "phone_number": "0000000000"
        }

        response = client.post(
            '/api/v1/create_organization', 
            data=json.dumps(data_to_send),
            headers=HEADERS)
        
        body = response.get_json()

        assert response.status == '201 CREATED'
        assert body['status'] == 'ok'


    def test_delete_organization_route():
        data_to_send = {
            'email': 'test_org@email.com',
            'password': '123456789'
        }

        response = client.delete(
            '/api/v1/delete_organization', 
            data=json.dumps(data_to_send), 
            headers=HEADERS)
        
        body = response.get_json()
        assert response.status_code == 202
        assert body['status'] == 'ok'
        assert body['message'] == 'Organization successfuly deleted!'