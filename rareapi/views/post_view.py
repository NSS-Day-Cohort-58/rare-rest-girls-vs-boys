from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rareapi.models import Post


class PostView(ViewSet):

    def retrieve(self, request, pk):

        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):

        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'user', 'category', 'title',
                  'publication_date', 'image_url', 'content')
