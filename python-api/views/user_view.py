import jwt
from pyramid.view import view_config
from pyramid.response import Response
from models.user import User
import os

@view_config(route_name='register', request_method='POST', renderer='json')
def register_view(request):
    data = request.json_body
    user = User(
        email=data['email'],
        name=data['name'],
        phone=data['phone'],
        billing_address=data.get('billing_address'), 
        city=data.get('city'), 
        state=data.get('state'), 
        postal_code=data.get('postal_code'), 
        country=data.get('country')
    )
    user.set_password(data['password'])
    user.save()  # Save user to MongoDB
    return {'message': 'User registered successfully'}

@view_config(route_name='login', request_method='POST', renderer='json')
def login_view(request):
    data = request.json_body
    user = User.find_by_email(data['email'])
    
    if user and user.check_password(data['password']):
        token = user.generate_auth_token(os.getenv('SECRET_KEY'))
        return {'token': token}
    
    return Response('Invalid credentials', status=401)

@view_config(route_name='verify_reset_token', request_method='POST', renderer='json')
def verify_reset_token_view(request):
    data = request.json_body
    user = User.find_by_email(data['email'])
    
    if user and user.verify_reset_token(data['token']):
        return {'message': 'Token is valid'}
    
    return Response('Invalid or expired token', status=401)

@view_config(route_name='user_details', request_method='GET', renderer='json')
def user_details_view(request):
    token = request.headers.get('Authorization').split(' ')[1]  # Assuming the token is sent as a Bearer token
    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        user = User.find_by_email(payload['email'])
        
        if user:
            return {
                'name': user.name,
                'email': user.email,
                'phone': user.phone,
                'user_image': user.user_image,
                # Add any other fields you want to expose
            }
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return Response('Invalid token', status=401)
    
    return Response('User not found', status=404)

def auth(config):
    config.add_route('register', '/signup')
    config.add_route('login', '/login')
    config.add_route('verify_reset_token', '/verify-reset-token')
    config.add_route('user_details', '/user/details')
    config.scan()
