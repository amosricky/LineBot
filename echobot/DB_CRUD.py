from echobot.serializers import UserSerializer,GoodsSerializer,ImageSerializer,ConditionSerializer
from echobot.models import user , goods ,image ,goods_condition
from rest_framework import viewsets

class UserViewSet(viewsets.ModelViewSet):
    queryset = user.objects.all()
    serializer_class = UserSerializer

class GoodsViewSet(viewsets.ModelViewSet):
    queryset = goods.objects.all()
    serializer_class = GoodsSerializer

class ImageViewSet(viewsets.ModelViewSet):
    queryset = image.objects.all()
    serializer_class = ImageSerializer

class ConditionViewSet(viewsets.ModelViewSet):
    queryset = goods_condition.objects.all()
    serializer_class = ConditionSerializer