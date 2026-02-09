from django.http import JsonResponse
from django.shortcuts import HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken


def v3_token(request):
    if request.user.is_authenticated:
        refresh = RefreshToken.for_user(request.user)

        return JsonResponse({
            'token': str(refresh.access_token)
        })

    return HttpResponse('Unauthorized', status=401)
