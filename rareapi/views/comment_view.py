from datetime import date
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rareapi.models import Comment
from rareapi.models import Post


class CommentView(ViewSet):

    def retrieve(self, request, pk):

        comment = Comment.objects.get(pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):

        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        assigned_post = Post.objects.get(pk=request.data["post"])

        comment = Comment()
        comment.content = request.data["content"]
        comment.created_on = date.today()
        comment.author = request.auth.user
        comment.post = assigned_post
        comment.save()

        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def destroy(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'content',
                  'created_on')
