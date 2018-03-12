from rest_framework import serializers
from echobot.models import user , goods ,image ,goods_condition

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ('userID','TimeStamp')

class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = goods
        fields = ('goodsID' , 'title' , 'price' , 'webLink')

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = image
        fields = ('goodsID' , 'imageLink')

class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = goods_condition
        fields = ('goodstitle' , 'price')