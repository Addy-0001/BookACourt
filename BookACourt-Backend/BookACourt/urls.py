"""
URL configuration for BookACourt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]


admin.site.site_header = "Book A Court Main Admin Panel"
admin.site.site_title = 'Book A Court Admin'
admin.site.index_title = 'Welcome to Book A Court Admin Panel'
admin.site.unregister_group = None

# change favicon for admin panel
admin.site.site_url = None
admin.site.site_favicon = '/static/images/favicon.ico'

# change admin footer
admin.site.footer = "Book A Court © 2024. All rights reserved."
