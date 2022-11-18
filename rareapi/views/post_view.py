from datetime import date
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rareapi.models import Post, Rare_User, Category, Subscription, Tag
from django.contrib.auth.models import User
from rest_framework.decorators import action


class PostView(ViewSet):

    def retrieve(self, request, pk):

        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):

        posts = []

        if 'status' in request.query_params:
            
            rare_user = Rare_User.objects.get(user=request.auth.user)

            if request.query_params['status'] == "created":
                posts = Post.objects.filter(user=rare_user.id)

            if request.query_params['status'] == "subscribed":
                subscriptions = Subscription.objects.filter(follower=rare_user.id)
                
                for subscription in subscriptions:
                    author_posts = Post.objects.filter(user=subscription.author)
                    posts.extend(author_posts)
        else:
            posts = Post.objects.all()

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):


        post = Post()
        post.user = Rare_User.objects.get(user=request.auth.user)
        post.category = Category.objects.get(pk=request.data["category_id"])
        post.title = request.data["title"]
        post.publication_date = date.today()
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]

        if request.auth.user.is_staff:
            post.approved=True
        else:
            post.approved=False

        post.save()

        serializer = PostSerializer(post)
        return Response(serializer.data)


    @action(methods=['post'], detail=True)
    def addTag(self, request, pk):
    
        tag = Tag.objects.get(pk=request.data["tag_id"])
        post = Post.objects.get(pk=request.data["post_id"])
        post.tags.add(tag)

        return Response({'message': 'Tag added'}, status=status.HTTP_201_CREATED)

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

class PostTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'label')

class PostSerializer(serializers.ModelSerializer):

    user = RareUserSerializer(many=False)
    category = CategorySerializer(many=False)
    tags = PostTagSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'user', 'category', 'title',
                  'publication_date', 'image_url', 'content', 'approved', 'tags')
