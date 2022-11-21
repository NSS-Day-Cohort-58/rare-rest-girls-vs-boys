from datetime import date
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rareapi.models import Subscription
from rareapi.models import Rare_User


class SubscriptionView(ViewSet):

    def retrieve(self, request, pk):

        subscription = Subscription.objects.get(pk=pk)
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        subscriptions = []
        if "status" in request.query_params:
            if request.query_params["status"] == "active":
                rare_author = Rare_User.objects.get(
                    user=request.query_params["author"])
                rare_follower = Rare_User.objects.get(user=request.auth.user)
                subs = Subscription.objects.filter(author=rare_author,
                                                   follower=rare_follower)
                for sub in subs:
                    if sub.ended_on > date.today():
                        subscriptions.append(sub)
                        break
                    else:
                        subscriptions = []
        else:
            subscriptions = Subscription.objects.all()

        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        sub = Subscription()
        follower = Rare_User.objects.get(user=request.auth.user)
        author = Rare_User.objects.get(pk=request.data["author"])
        sub.follower = follower
        sub.author = author
        sub.created_on = date.today()
        sub.save()

        serializer = SubscriptionSerializer(sub)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        updated_sub = Subscription.objects.get(pk=pk)
        updated_sub.ended_on = date.today()
        updated_sub.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('id', 'author', 'follower', 'created_on',
                  'ended_on')
