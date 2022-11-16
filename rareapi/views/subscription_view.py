from datetime import date
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rareapi.models import Subscription


class SubscriptionView(ViewSet):

    def retrieve(self, request, pk):

        subscription = Subscription.objects.get(pk=pk)
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):

        subscriptions = Subscription.objects.all()
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        sub = Subscription()
        sub.follower = request.auth.user
        sub.author = request.data["author"]
        sub.created_on = date.today()
        sub.ended_on = ""
        sub.save()

        serializer = SubscriptionSerializer(sub)
        return Response(serializer.data)


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('id', 'author', 'follower', 'create_on',
                  'ended_on')
