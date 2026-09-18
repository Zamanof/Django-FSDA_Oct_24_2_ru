from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import NoteViewSet, CategoryViewSet, TagViewSet

router = DefaultRouter()

router.register("notes", NoteViewSet, basename="notes")

router.register("categories", CategoryViewSet, basename="categories")
router.register("tags", TagViewSet, basename="tags")

urlpatterns = [
    path('', include(router.urls)),
]