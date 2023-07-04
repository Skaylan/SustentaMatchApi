from app import app
from app.config.db_config import *
from app.config.app_config import *
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.tables.ogranization import Organization
from app.models.tables.campaign import Campaign
from app.models.tables.campaign_images import CampaignImages
from app.models.schemas.organization_schema import OrganizationSchema
from app.models.schemas.campaign_schema import CampaignSchema
from app.models.schemas.campaign_images_schema import CampaignImagesSchema
from flask import request, jsonify
import jwt
import sys, os
from uuid import uuid4
from app.utils import convert_base64_to_image, convert_image_to_base64

IMAGES_SAVE_PATH = "D://atividades//SustentaMatchApi//app//image_database"


@app.route('/api/v1/create_organization', methods=['POST'])
def create_organization():
    if request.method == 'POST':
        try:
            body = request.get_json()
            name = body['name']
            cnpj = body['cnpj']
            password = body['password']
            re_password = body['re_password']
            address = body['address']
            cep = address[0]
            street_name = address[1]
            state_name = address[2]
            number = address[3]
            city = address[4]
            phone_number = body['phone_number']
            email = body['email']
            organization_type = body['organization_type']
            action_field = body['action_field']
            profile_image_b64_string = body['profile_image_b64_string']

            if password != re_password:
                return jsonify({
                    'message': "password and repassword don't match!",
                    'status': 'bad'
                })
            profile_img_uuid = str(uuid4())
            convert_base64_to_image(img_base64_string=profile_image_b64_string, image_uuid=profile_img_uuid, save_path=IMAGES_SAVE_PATH)

            password_hash = generate_password_hash(password=password)
            org = Organization(
                name=name, 
                cnpj=cnpj, 
                phone_number=phone_number, 
                email=email,
                password_hash=password_hash,
                organization_type=organization_type,
                action_field = action_field,
                cep=cep,
                street_name=street_name,
                city=city,
                number=number,
                state_name=state_name,
                profile_image_uuid=profile_img_uuid
            )

            db.session.add(org)
            db.session.commit()
            db.session.close()
            
            org_info = Organization.query.filter_by(email=email).first()
            schema = OrganizationSchema()
            payload = schema.dump(org_info)
            token = jwt.encode({'email': org_info.email}, str(org_info.email), algorithm='HS256')
            return jsonify({
                'status': 'ok',
                'message': 'Organization created!',
                'token': token,
                'organization_info': payload
                
            }), 201

        except Exception as error:
            print(f'error class: {error.__class__} | error cause: {error.__cause__}')
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({
                    'status': 'error',
                    'message': 'An error has occurred!',
                    'error_class': str(error.__class__),
                    'error_cause': str(error.__cause__)
                }), 500
    


@app.route('/api/v1/get_organizations', methods=['GET'])
def get_all_organzations():
    try:
        organization_schema = OrganizationSchema(many=True)
        orgs = Organization.query.all()
        payload = organization_schema.dump(orgs)
        return jsonify(payload), 200
    
    except Exception as error:
        print(f'error class: {error.__class__} | error cause: {error.__cause__}')
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify({
                'status': 'error',
                'message': 'An error has occurred!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
        }), 500
    

@app.route('/api/v1/get_organization_by_id', methods=['GET'])
def get_organization_by_id():
    if request.method == 'GET':
        try:
            id = request.args.get('user_id')
            id = int(id)
            org = Organization.query.filter_by(id=id).first()
            schema = OrganizationSchema()
            payload = schema.dump(org)
            payload['profile_img_b64_string'] = convert_image_to_base64(IMAGES_SAVE_PATH, payload['profile_image_uuid'])
            return jsonify(payload), 200
        except Exception as error:
            print(f'error class: {error.__class__} | error cause: {error.__cause__}')
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({
                    'status': 'error',
                    'message': 'An error has occurred!',
                    'error_class': str(error.__class__),
                    'error_cause': str(error.__cause__)
            }), 500
            

@app.route('/api/v1/delete_organization', methods=['DELETE'])
def delete_organization():
    if request.method == 'DELETE':
        try:
            body = request.get_json()
            email = body['email']
            password = body['password']

            org = Organization.query.filter_by(email=email).first()
            if org:
                checked_password = check_password_hash(pwhash=org.password_hash, password=password)
                if checked_password:
                    db.session.delete(org)
                    db.session.commit()
                    db.session.close()

                    return jsonify({
                        'status': 'ok',
                        'message': 'Organization successfuly deleted!'
                    }), 202
                else:
                    return jsonify({
                        'status': 'bad',
                        'message': 'Wrong Password!'
                    }), 500
            else:
                return jsonify({
                    'status': 'bad',
                    'message': f'Organization with email {email} not found!'
                }), 404
            
        except Exception as error:
            print(f'error class: {error.__class__} | error cause: {error.__cause__}')
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({
                    'status': 'error',
                    'message': 'An error has occurred!',
                    'error_class': str(error.__class__),
                    'error_cause': str(error.__cause__)
            }), 500


@app.route('/api/v1/authenticate', methods=['POST'])
def authenticate():
    if request.method == 'POST':
        try:
            body = request.get_json()
            email = body['email']
            password = body['password']

            org = Organization.query.filter_by(email=email).first()
            if org:
                if check_password_hash(pwhash=org.password_hash, password=password):
                    token = jwt.encode({'email': org.email}, str(org.email), algorithm='HS256')
                    schema = OrganizationSchema()
                    payload = schema.dump(org)
                    return jsonify({
                        'status': 'ok',
                        'message': 'Successfuly authenticated!',
                        'token': token,
                        'user_infos': payload
                    }), 200
                else:
                    return jsonify({
                    'status': 'bad',
                    'message': f'Wrong password!'
                }), 404
            else:
                return jsonify({
                    'status': 'bad',
                    'message': f'Organização com email {email} não existe no sistema!'
                }), 404

        except Exception as error:
            print(f'error class: {error.__class__} | error cause: {error.__cause__}')
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({
                    'status': 'error',
                    'message': 'An error has occurred!',
                    'error_class': str(error.__class__),
                    'error_cause': str(error.__cause__)
            }), 500


@app.route('/api/v1/create_campaign', methods=['POST'])
def create_campaign():
    if request.method == 'POST':
        try:
            body = request.get_json()
            title = body['title']
            info_text = body['info_text']
            banner_img_data = body['banner_img_data']
            org_id = body['org_id']
            banner_img_uuid = uuid4()
            
            campaign = Campaign(
                title=title,
                info_text=info_text,
                banner_img_uuid=str(banner_img_uuid),
                owner_id=int(org_id)
            )
            
            convert_base64_to_image(
                img_base64_string=banner_img_data,
                image_uuid=banner_img_uuid,
                save_path='D://atividades//SustentaMatchApi//app//image_database'
            )

            db.session.add(campaign)
            db.session.commit()
            db.session.close()
            
            return jsonify({
                'status': 'ok',
                'message': 'Campaign successfuly created!',
            }), 201
        
        except Exception as error:
            print(f'error class: {error.__class__} | error cause: {error.__cause__}')
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({
                    'status': 'error',
                    'message': 'An error has occurred!',
                    'error_class': str(error.__class__),
                    'error_cause': str(error.__cause__)
            }), 500




@app.route('/api/v1/get_organization_campaigns', methods=['GET'])
def get_campaign():
    try:
        owner_id = request.args.get("owner_id")
        campaigns = Campaign.query.filter_by(owner_id=owner_id).order_by(Campaign.created_at.desc()).all()
        campaigns_schema = CampaignSchema(many=True)
        payload = campaigns_schema.dump(campaigns)

        for i, _ in enumerate(payload):
            payload[i]['banner_img_b64_string'] = convert_image_to_base64(IMAGES_SAVE_PATH, payload[i]['banner_img_uuid'])
        return jsonify(payload)
    except Exception as error:
        print(f'error class: {error.__class__} | error cause: {error.__cause__}')
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify({
                'status': 'error',
                'message': 'An error has occurred!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
        }), 500


@app.route('/api/v1/get_organizations_by_args', methods=['GET'])
def get_campaigns_by_args():
    ORG_TYPE = ['ong', 'empresa']
    ACTION_FIELDS = ['meio ambiente', 'tecnologia', 'saude', 'educacao', 'direitos humanos']
    try:
        org_type = request.args.get('org_type')
        action_field = request.args.get('action_field')
        print(org_type, action_field)
        if org_type in ORG_TYPE and action_field in ACTION_FIELDS:
            orgs = Organization.query.filter_by(organization_type=org_type).filter_by(action_field=action_field).all()
        elif org_type == 'ong' and action_field == 'all':
            orgs = Organization.query.filter_by(organization_type='ong').all()
        elif org_type == 'empresa' and action_field == 'all':
            orgs = Organization.query.filter_by(organization_type='empresa').all()
        else:
            orgs = Organization.query.all()
            
        org_schema = OrganizationSchema(many=True)
        payload = org_schema.dump(orgs)

        for i, item in enumerate(payload):
            payload[i]['profile_img_b64_string'] = convert_image_to_base64(IMAGES_SAVE_PATH, payload[i]['profile_image_uuid'])
        
        return jsonify(
            {   'status': 'ok',
                'organizations': payload
            }
        )
    except Exception as error:
        print(f'error class: {error.__class__} | error cause: {error.__cause__}')
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify({
                'status': 'error',
                'message': 'An error has occurred!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
        }), 500
    

@app.route('/api/v1/get_campaign_by_id', methods=['GET'])
def get_campaign_by_id():
    try:
        id = request.args.get('campaign_id')
        campaign = Campaign.query.filter_by(id=id).first()
        campaign_schema = CampaignSchema(many=False)
        payload = campaign_schema.dump(campaign)
        payload['banner_img_b64_string'] = convert_image_to_base64(IMAGES_SAVE_PATH, payload['banner_img_uuid'])
        return jsonify({
            'status': 'ok',
            'campaign': payload
        })
    except Exception as error:
        print(f'error class: {error.__class__} | error cause: {error.__cause__}')
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify({
                'status': 'error',
                'message': 'An error has occurred!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
        }), 500
    


@app.route('/api/v1/add_campaign_image', methods=['POST'])
def add_campaign_image():
    try:
        body = request.get_json()
        campaign_id = body['campaign_id']
        img_base64_string = body['img_base64_string']
        img_uuid = str(uuid4())
        convert_base64_to_image(img_base64_string=img_base64_string, image_uuid=img_uuid, save_path=IMAGES_SAVE_PATH)
        new_campaign_image = CampaignImages(campaign_id=campaign_id, img_uuid=img_uuid)
        db.session.add(new_campaign_image)
        db.session.commit()
        db.session.close()

        return jsonify({
            'status': 'ok',
            'message': 'Image successfuly added!'
        })
    
    except Exception as error:
        print(f'error class: {error.__class__} | error cause: {error.__cause__}')
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify({
                'status': 'error',
                'message': 'An error has occurred!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
        }), 500


@app.route('/api/v1/get_campaign_images', methods=['GET'])
def get_campaign_images():
    try:
        campaign_id = request.args.get('campaign_id')
        images = CampaignImages.query.filter_by(campaign_id=campaign_id).all()
        campaign_images_schema = CampaignImagesSchema(many=True)
        payload = campaign_images_schema.dump(images)

        for i, item in enumerate(payload):
            payload[i]['img_base64_string'] = convert_image_to_base64(IMAGES_SAVE_PATH, payload[i]['img_uuid'])

        return jsonify({
                'status': 'ok',
                'campaign_images': payload
            }
        )
    except Exception as error:
        print(f'error class: {error.__class__} | error cause: {error.__cause__}')
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify({
                'status': 'error',
                'message': 'An error has occurred!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
        }), 500

@app.route('/api/v1/delete_campaign_image', methods=['DELETE'])
def delete_campaign_image():
    try:
        img_uuid = request.args.get('image_id')
        image_to_delete = CampaignImages.query.filter_by(img_uuid=img_uuid).first()
        os.remove(os.path.join(IMAGES_SAVE_PATH, f'{img_uuid}.png'))
        db.session.delete(image_to_delete)
        db.session.commit()
        db.session.close()
        return jsonify({   
                'status': 'ok',
                'message': 'Image successfuly deleted!'
            }
        )
    except Exception as error:
        print(f'error class: {error.__class__} | error cause: {error.__cause__}')
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify({
                'status': 'error',
                'message': 'An error has occurred!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
        }), 500