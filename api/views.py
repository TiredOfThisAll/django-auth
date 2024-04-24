from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout

import redis

from .utils.hash import hash_password, verify_password
from .utils.user_codes import generate_invite_code, generate_verification_code


r = redis.Redis(host='localhost', port=6379, decode_responses=True)

@api_view(["POST"])
def send_code(request):
    phone_number = request.POST["phone_number"]
    if CustomUser.objects.filter(phone_number=phone_number).exists():
        return Response({"error": "This phone is already occupied"}, 418)
    code = generate_verification_code()
    r.set(phone_number, code)

    return Response({"code_send": "true"}, 200)


@api_view(["POST"])
def verify_code(request):
    code = request.POST["inserted_code"]
    phone_number = request.POST["phone_number"]
    stored_code = r.get(request.POST["phone_number"])

    if stored_code and stored_code == code:
        r.delete(phone_number)
        token = '123321'
        r.set(phone_number, token)
        return Response({"auth": True, "token": token}, 200)
    else:
        return Response({"error": 'Invalid auth code'}, 418)


@api_view(["POST"])
def create_user(request):
    given_token = request.POST.get('token')
    phone_number = request.POST.get('phone_number')
    stored_token = r.get(phone_number)

    if not stored_token or stored_token != given_token:
        return Response({"error": 'Invalid token or phone number'}, 418)
    
    r.delete(phone_number)

    user_data = {}
    user_data["first_name"] = request.POST.get('first_name')
    user_data["last_name"] = request.POST.get('last_name')
    user_data["phone_number"] = request.POST.get('phone_number')
    user_data["username"] = request.POST.get('username')
    user_data["password"] = request.POST.get('password')

    for key, value in user_data.items():
        if not value:
            return Response({'error': f'{key} must be provided'}, 418)

    if CustomUser.objects.filter(phone_number=user_data["phone_number"]).exists():
        return Response({'error': 'This phone number is already occupied'}, 418)

    if CustomUser.objects.filter(username=user_data["username"]).exists():
        return Response({'error': 'This login is already occupied'}, 418)
    

    user = CustomUser.objects.create(
        first_name=user_data["first_name"],
        last_name=user_data["last_name"],
        phone_number=user_data["phone_number"],
        username=user_data["username"],
        password=hash_password(user_data["password"]),
        invite_code=generate_invite_code(6),
    )

    serializer = UserSerializer(user)
    return Response(serializer.data, status=201)


@api_view(["POST"])
def verificate_user(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    if not login or not password:
        return Response({'error': 'All requested fields must be provided'}, 418)
    
    user = CustomUser.objects.filter(username=username).first()

    if not user:
        return Response({'error': 'Invalid login'}, 418)
    
    if not verify_password(password, user.password):
        return Response({'error': 'Invalid password'}, 418)
    
    token, created = Token.objects.get_or_create(user=user)

    login(request, user)

    return Response({'token': token.key, "user_id": user.id}, 200)


@api_view(["GET"])
def get_user_by_id(request, id):
    if not request.user.is_authenticated:
        return Response({'error': 'You have to login or provide auth token'})
    try:
        user = CustomUser.objects.get(id=id)
    except CustomUser.DoesNotExist:
        return Response(status=404)

    serializer = UserSerializer(user)
    return Response(serializer.data, 200)


@api_view(["POST"])
def apply_invite_code(request, id):
    if not request.user.is_authenticated:
        return Response({'error': 'You have to login or provide auth token'})

    invite_code = request.POST.get("invite_code")

    if not invite_code:
        return Response({'error': 'You have to provide invite code'}, 418)
    
    user = CustomUser.objects.filter(id=id).first()

    if not user:
        return Response({'error': 'No user was found with this id'}, 418)

    if user.invited_by:
        return Response({'error': 'This user has already applied another invite code'}, 418)
    
    if not CustomUser.objects.filter(invite_code=invite_code).exists():
        return Response({'error': 'You have to provide a valid invite code'}, 418)

    user.invited_by = invite_code
    user.save()

    serializer = UserSerializer(user)

    return Response(serializer.data, status=200)


@api_view(["GET"])
def get_invited_users(request, id):
    if not request.user.is_authenticated:
        return Response({'error': 'You have to login or provide auth token'})

    if int(id) != request.user.id:
        return Response({"error": f"this page is not accessible for user with id {id}"})
    invite_code = request.POST.get("invite_code")

    if not invite_code:
        return Response({'error': 'You have to provide invite code'}, 418)
    
    invited_users = CustomUser.objects.filter(invited_by=invite_code)

    phone_numbers = []

    for user in invited_users:
        phone_numbers.append(user.phone_number)
    
    return Response({"phone_numbers": phone_numbers}, 200)


@api_view(["GET"])
def logout_user(request):
    if not request.user.is_authenticated:
        return Response({'error': 'You have to login or provide auth token'})

    logout(request)
    return Response({"status": "Successfully logged out"}, 200)
