from datetime import date
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rareapi.models import Post, Rare_User, Category, Subscription
from django.contrib.auth.models import User


class PostView(ViewSet):

    def retrieve(self, request, pk):

        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):

        posts = []

        if 'status' in request.query_params:
            if request.query_params['status'] == "created":
                posts = Post.objects.filter(user=request.auth.user)

            if request.query_params['status'] == "subscribed":

                rare_user = Rare_User.objects.get(user=request.auth.user)
                subscriptions = Subscription.objects.filter(follower_id=rare_user['id'])
                
                for subscription in subscriptions:
                    author_posts = Post.objects.filter(user=subscription.author_id)
                    posts.extend(author_posts)
        else:
            posts = Post.objects.all()

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        post = Post()
        post.user = request.auth.user
        post.category = request.data["category"]
        post.title = request.data["title"]
        post.publication_date = date.today()
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        post.save()

        serializer = PostSerializer(post)
        return Response(serializer.data)

    def destroy(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class RareUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rare_User
        fields = ('id', 'user', 'category', 'title',
                  'publication_date', 'image_url', 'content')

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'user', 'category', 'title',
                  'publication_date', 'image_url', 'content')

class RareUserSerializer(serializers.ModelSerializer):
    class Meta:

        model = Rare_User
        fields = ('id', 'user', 'active', 'profile_image_url',
                  'created_on', 'bio', 'full_name', 'username', 'email')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'label')


class PostSerializer(serializers.ModelSerializer):

    user = RareUserSerializer(many=False)
    category = CategorySerializer(many=False)

    class Meta:
        model = Post
        fields = ('id', 'user', 'category', 'title',
                  'publication_date', 'image_url', 'content')
