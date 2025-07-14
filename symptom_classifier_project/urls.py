from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('classifier_app.urls')), # <--- THIS MUST BE EXACTLY 'classifier_app.urls'
]