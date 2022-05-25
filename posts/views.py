from django.db.models import Count
from rest_framework import generics, filters
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from django_rest_framework.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):

    serializer_class = PostSerializer
    permission_classes = [
                          permissions.IsAuthenticatedOrReadOnly
                         ]
    queryset = Post.objects.annotate(
        comment_count=Count('comment', distinct=True),
        like_count=Count('likes', distinct=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend
    ]
    filterset_fields = [
        'owner__followed__owner__profile',
        'likes__owner__profile',
        'owner__profile'
    ]
    ordering_fields = [
        'like_count',
        'comment_count',
        'like__created_at'
    ]
    search_fields = [
        'owner__username',
        'title'
    ]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')
