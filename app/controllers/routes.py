from app import app
from app.config.db_config import *
from app.config.app_config import *
from werkzeug.security import generate_password_hash
from app.models.tables.ogranization import Organization
from app.models.schemas.organization_schema import OrganizationSchema
from flask import request, jsonify


@app.route('/api/v1/create_organization', methods=['POST'])
def create_organization():
    if request.method == 'POST':
        try:
            body = request.get_json()
            name = body['name']
            cnpj = body['cnpj']
            password = body['password']
            address = body['address']
            phone_number = body['phone_number']
            email = body['email']
            organization_type = body['organization_type']
            action_field = body['organization_type']
            password_hash = generate_password_hash(password=password)

            org = Organization(
                name=name, 
                cnpj=cnpj, 
                address=address, 
                phone_number=phone_number, 
                email=email,
                password_hash=password_hash,
                organization_type=organization_type,
                action_field = action_field
            )
            db.session.add(org)
            db.session.commit()
            db.session.close()

            return jsonify({
                'status': 'ok',
                'message': 'Organization created!',
            }), 201

        except Exception as error:
            print(f'error class: {error.__class__} | error cause: {error.__cause__}')
            return jsonify({
                    'status': 'error',
                    'message': 'An error has occurred!',
                    'error_class': str(error.__class__),
                    'error_cause': str(error.__cause__)
                }), 500
    


@app.route('/api/v1/get_organizations', methods=['GET'])
def get_all_organzations():
    try:
        orgs = Organization.query.all()
        schema = OrganizationSchema(many=True)
        payload = schema.dump(orgs)
        return jsonify({
            'organizations': payload,
            'status': 'ok'
        }), 200
    
    except Exception as error:
        print(f'error class: {error.__class__} | error cause: {error.__cause__}')
        return jsonify({
                'status': 'error',
                'message': 'An error has occurred!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
        }), 500
