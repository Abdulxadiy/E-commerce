from .serializers import SMSSerializer, VerifySMSSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.core.cache import cache
from django.conf import settings
from custom_auth.types import User
import requests
import random
SMS_KEY = settings.SMS_KEY


class SMSLoginViewSet(viewsets.ViewSet):
    def send_sms(self, request):
        serializer = SMSSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']

            # Generate a random 6-digit verification code
            verification_code = random.randint(100000, 999999)

            # Send SMS via InfoBip
            url = 'https://43vvd1.api.infobip.com/sms/2/text/advanced'

            headers = {
                "Authorization": f"App {SMS_KEY}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }

            payload = {
                "messages": [
                    {
                        "from": "E-commerce",
                        "destinations": [
                            {
                                "to": phone_number
                            }
                        ],
                        "text": f"Your verification code is: {verification_code}"
                    }
                ]
            }

            try:
                response = requests.post(url, headers=headers, json=payload)

                if response.status_code == 200:
                    # Check if messages were sent
                    response_data = response.json()
                    if response_data.get('messages'):
                        # Store the verification code and phone number in cache for 5 minutes
                        cache.set(phone_number, verification_code, timeout=300)
                        
                        # Print code to terminal console for local debugging
                        print("\n" + "="*50)
                        print(f"DEBUG SMS VERIFICATION CODE FOR {phone_number}: {verification_code}")
                        print("="*50 + "\n")
                        
                        resp_payload = {"message": "Verification code sent successfully."}
                        if settings.DEBUG:
                            resp_payload["code"] = verification_code  # Expose to API in DEBUG mode
                            
                        return Response(resp_payload, status=status.HTTP_200_OK)
                    else:
                        return Response({"error": "No messages sent"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                return Response({"error": f"Failed to send SMS. Status: {response.status_code}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                return Response({"error": f"Exception: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def verify_sms(self, request):
        serializer = VerifySMSSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            verification_code = serializer.validated_data['verification_code']

            # Retrieve the stored verification code from cache
            stored_code = cache.get(phone_number)

            if stored_code and str(stored_code) == str(verification_code):
                # If the code is correct, authenticate the user
                user, created = User.objects.get_or_create(phone_number=phone_number)

                if created:
                    user.save()

                # Generate JWT token
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return Response({
                    "message": "Verification successful.",
                    "access_token": access_token,
                    "refresh_token": str(refresh)
                }, status=status.HTTP_200_OK)

            return Response({"error": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
