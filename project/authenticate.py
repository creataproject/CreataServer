from rest_framework.authtoken.models import Token


class CustomTokenAuthentication():

    def authenticate(self, request):
        if request.META.get('HTTP_AUTHORIZATION', '').startswith('Bearer'):
            token_qs = Token.objects.filter(key=request.META.get('HTTP_AUTHORIZATION', '')[7:])
            if token_qs.exists():
                token = token_qs.first()
                return (token.user, token.key)
        return (None, None)

