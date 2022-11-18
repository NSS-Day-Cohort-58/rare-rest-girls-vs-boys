from datetime import date
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rareapi.models import Comment, Post, Rare_User



class CommentView(ViewSet):

    def retrieve(self, request, pk):

        comment = Comment.objects.get(pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        logged_in_user = Rare_User.objects.get(user=request.auth.user)
        logged_user_id = logged_in_user.pk


        if "post" in request.query_params:
            post_id = request.query_params["post"]
            comments = Comment.objects.filter(post=post_id) #comments is all the comments for that post
        
        else:

            comments = Comment.objects.all()

    
        for comment in comments:
             if logged_user_id == comment.author_id:
                 comment.created = True 
             else:
                 comment.created = False
            
                    

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        assigned_post = Post.objects.get(pk=request.data["post"])
        author = Rare_User.objects.get(user=request.auth.user)

        comment = Comment()
        comment.content = request.data["content"]
        comment.created_on = date.today()
        comment.author = author
        comment.post = assigned_post
        comment.save()

        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def destroy(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk):
        """handles PUT request to comments"""

        comment = Comment.objects.get(pk=pk)
        comment.post = Post.objects.get(pk=request.data["post"])
        comment.author = Rare_User.objects.get(pk=request.data["author"])
        comment.content = request.data["content"]
        comment.created_on = request.data["createdOn"]
       
        comment.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class CommentSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'content',
                  'created_on', 'created')
