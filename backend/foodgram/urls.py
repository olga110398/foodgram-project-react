from django.contrib import admin
from django.urls import include, path

app_name = 'foodgram'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/', include('users.urls'))
]
