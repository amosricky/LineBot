from.import views , DB_CRUD
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
import django.urls
from django.urls import reverse

router = DefaultRouter()
router.register(r'user', DB_CRUD.UserViewSet)
router.register(r'goods', DB_CRUD.GoodsViewSet)
router.register(r'image', DB_CRUD.ImageViewSet)
router.register(r'condition', DB_CRUD.ConditionViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url('^callback/', views.callback),
]
