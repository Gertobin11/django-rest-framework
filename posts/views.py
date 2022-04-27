from rest_framework import generics
from rest_framework import permissions
from django_rest_framework.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):

    serializer_class = PostSerializer
    permission_classes = [
                          permissions.IsAuthenticatedOrReadOnly
                         ]
    queryset = Post.objects.all()


class PostDetail(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
