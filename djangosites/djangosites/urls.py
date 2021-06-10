from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from .views import logins, cikisyap
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('chat/', include('chat.urls')),
    path('admin/', admin.site.urls),
    path('login/', logins, name="login"),
    path("logout/",cikisyap),
]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)