from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.permissions import IsAuthorOrReadOnly
from api.serializers import NoteSerializer, CategorySerializer, TagSerializer
from notes.models import Note, Category, Tag


class NoteViewSet(viewsets.ModelViewSet):
    queryset = (Note
                .objects
                .select_related('category', 'author')
                .prefetch_related('tags'))
    serializer_class = NoteSerializer
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            return queryset.filter(status = 'published')
        return queryset
    def perform_create(self, serializer):
        serializer.save(author = self.request.user)



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)