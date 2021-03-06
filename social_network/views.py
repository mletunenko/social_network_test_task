from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import action
from social_network.models import Post
from social_network.serializers import UserSerializer, PostSerializer
import requests
from social_network.config import API_KEY



@api_view(['POST'])
def user_registration(request):
    data = request.data
    query = f'https://api.hunter.io/v2/email-verifier?email={data["email"]}&api_key={API_KEY}'
    response = requests.get(query)
    if response.status_code==200:
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer.instance.set_password(data['password'])
        serializer.instance.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response('Bad email', status=status.HTTP_400_BAD_REQUEST)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)

        data = dict(request.data.items())
        data['author'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        data = dict(request.data.items())
        data['author'] = request.user.id
        serializer = self.get_serializer(instance, data=data, partial=kwargs.pop('partial', False))
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        instance = self.get_object()
        if request.user.is_authenticated and not instance.likes.filter(id=request.user.id).exists():
            instance.likes.add(request.user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        instance = self.get_object()
        if request.user.is_authenticated and instance.likes.filter(id=request.user.id).exists():
            instance.likes.remove(request.user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
