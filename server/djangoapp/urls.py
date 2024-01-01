from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    path('static/', views.static_view, name='static'), 
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),      
    path('registration/', views.registration_request, name='registration'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),

    path(route='', view=views.get_dealerships, name='index'),
    #paths by ElliottRN
    # path for dealer reviews view
    path(route='dealer/<int:dealer_id>/', view=views.get_dealer_details, name='dealer_details'),
    
    # path for add a review view
    path(route='add_dealer_review/<int:dealer_id>/', view=views.add_review, name='add_review')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
