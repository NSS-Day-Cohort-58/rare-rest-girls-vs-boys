"""View module for handling tags"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Tag



class TagView(ViewSet):
    """Rare tag view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single tag"""

        tag = Tag.objects.get(pk=pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all tags"""

        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)


class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for tags"""

    class Meta: 
        model = Tag
        fields = ('id', 'label')

