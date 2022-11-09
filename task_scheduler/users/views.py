from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer


class UserApiView(APIView):

    def get(self, request):
        users = User.objects.all()
        return Response(UserSerializer(users, many=True).data)
