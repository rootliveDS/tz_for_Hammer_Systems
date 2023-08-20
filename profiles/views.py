import time, secrets, string, random

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import UserProfile
from .serializers import UserProfileSerializer


class RequestAuthorizationCodeView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        phone_number_clean = ''.join(filter(str.isdigit, phone_number))
        phone_number = phone_number_clean.lstrip('+')

        if not phone_number:
            return Response({'error': 'Phone number is required.'}, status=400)

        authorization_code = ''.join(random.choice('0123456789') for _ in range(4))
        time.sleep(2)

        user, created = UserProfile.objects.get_or_create(phone_number=phone_number)
        if created:
            user.authorization_code = authorization_code
            user.save()
            return Response({'message': 'Authorization code sent successfully.'})
        else:
            return Response({'message': 'User already exists.'})




class VerifyAuthorizationCodeView(APIView):
    def post(self, request, phone_number):
        authorization_code = request.data.get('authorization_code')
        phone_number_clean = ''.join(filter(str.isdigit, phone_number))
        phone_number = phone_number_clean.lstrip('+')

        if not phone_number or not authorization_code:
            return Response({'error': 'Phone number and authorization code are required.'}, status=400)

        try:
            user = UserProfile.objects.get(phone_number=phone_number)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

        if not authorization_code:
            return Response({'error': 'Authorization code is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if user.authorization_code != authorization_code:
            return Response({'error': 'Invalid authorization code.'}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_authorized:
            return Response({'message': 'Phone number is already authorized.'})

        generated_personal_code = self.generate_personal_code()
        user.personal_code = generated_personal_code
        user.is_authorized = True
        user.save()

        return Response({'message': 'Authorization successful.'})

    def generate_personal_code(self):
        alphabet = string.ascii_letters + string.digits
        while True:
            generated_code = ''.join(secrets.choice(alphabet) for _ in range(6))
            if not UserProfile.objects.filter(personal_code=generated_code).exists():
                return generated_code

class UserProfileView(APIView):
    def get(self, request, phone_number):
        phone_number_clean = ''.join(filter(str.isdigit, phone_number))
        phone_number = phone_number_clean.lstrip('+')

        try:
            user = UserProfile.objects.get(phone_number=phone_number)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)

        serializer = UserProfileSerializer(user)
        response_data = serializer.data
        response_data['is_authorized'] = user.is_authorized
        response_data['personal_code'] = user.personal_code
        response_data['invited_phone'] = user.invited_phone

        return Response(response_data)

    def post(self, request, phone_number):
        phone_number_clean = ''.join(filter(str.isdigit, phone_number))
        phone_number = phone_number_clean.lstrip('+')
        personal_code_request = request.data.get('personal_code')
        filtered_users = UserProfile.objects.filter(personal_code=personal_code_request)

        if not personal_code_request:
            return Response({'error': 'Invite code is required.'}, status=400)

        try:
            invite_owner = UserProfile.objects.get(personal_code=personal_code_request)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Invalid invite code.'}, status=400)

        if phone_number == invite_owner.phone_number:
            return Response({'error': 'Unauthorized request.'}, status=401)

        try:
            user = UserProfile.objects.get(phone_number=phone_number)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)

        if invite_owner.phone_number in user.invited_phone:
            return Response({'message': 'The user has already been added to the invite.'})

        user.invited_phone.append(invite_owner.phone_number)
        user.save()

        return Response({'message': 'The user has been added to the invite.'})
