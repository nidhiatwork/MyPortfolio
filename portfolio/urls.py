from django.urls import path, include
from . import views
from django.conf import settings  
from django.conf.urls.static import static  
urlpatterns = [
    path('', views.index, name='index'),
    path('image_to_text', views.image_to_text, name='image_to_text'),
]
if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  