"""djangobackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views

app_name = 'djangoapp'
urlpatterns = [
    # this route for the home page that renders static_template.html
    path(route='', view=views.render_static, name='static_template'),

    # this path that renders about.html
    path(route='about/', view=views.about, name='about'),

    # path for contact us view contact.html
    path(route='contact/', view=views.contact, name='about'),

    # path for registration
    path('registration/', views.registration_request, name='registration'),

    # path for login
    path('login/', views.login_request, name='login'),

    # path for logout
    path('logout/', views.logout_request, name='logout'),

    path('dealers/', views.get_dealerships, name='all_dealers'),

    # path for dealer reviews view
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),

    # path for add a review view
    path('addreview/<int:dealer_id>', views.add_review, name='add_review')
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)