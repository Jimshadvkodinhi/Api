from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/' , include('api.v1.users.urls')),
    path('api/v1/products/' , include('api.v1.products.urls'))
]
