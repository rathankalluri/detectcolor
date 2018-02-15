from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Home Page of App
    url(r'^$', views.index, name='index'),
    url(r'^upload/', views.upload, name='upload'),
]
	
if settings.DEBUG is True:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)