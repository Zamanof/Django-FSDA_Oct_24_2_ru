from django.urls import path

from . import views
urlpatterns = [
    path('contact/', views.contact_page, name='contact_page'),
    path('contact/success/', views.contact_success, name='contact_success'),
    path('noteform/', views.note_form, name='note_form'),
]