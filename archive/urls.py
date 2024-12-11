from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'politicians', views.PoliticianViewSet)
router.register(r'statements', views.StatementViewSet)
router.register(r'tags', views.TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 