from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from social_network.models import Post
from social_network.serializers import UserSerializer, PostSerializer
from django.contrib.auth import authenticate, login, logout


@api_view(['POST'])
def user_registration(request):
    data = request.data
    serializer = UserSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    serializer.instance.set_password(data['password'])
    serializer.instance.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(['POST'])
# def login_view(request):
#     username = request.data['username']
#     password = request.data['password']
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         return Response()
#     else:
#         data = {
#             'response': 'Invalid login/password'
#         }
#         return Response(data)
#
#
# @api_view(['POST'])
# def logout_view(request):
#     logout(request)
#     return Response()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)

        request.data['author'] = request.user.id
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        # request.data.pop('author', None)
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.pop('partial', False))
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
            # instance.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        instance = self.get_object()
        if request.user.is_authenticated and instance.likes.filter(id=request.user.id).exists():
            instance.likes.remove(request.user)
            # instance.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
