"""daanbaksho URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from re import template
from django.contrib import admin
from django.urls import path
from accounts.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from donations import views as don_views
from posts.views import *
from projects.views import *

urlpatterns = [
    path('dashboard/', dashboard, name = 'dashboard'),

    path('posts/', PostListView.as_view(), name = 'post-list'),

    path('posts/<int:pk>/', PostDetailView.as_view(), name = 'post-detail'),

    path('posts/<int:pk>/update/', PostUpdateView.as_view(), name = 'post-update'),

    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name = 'post-delete'),

    path('posts/new/', PostCreateView.as_view(), name = 'post-create'),

    # Media
    path('post-media/', MediaListView.as_view(), name = 'media-list'),

    path('post-media/<int:pk>/', MediaDetailView.as_view(), name = 'media-detail'),

    path('post-media/<int:pk>/update/', MediaUpdateView.as_view(), name = 'media-update'),

    path('post-media/<int:pk>/delete/', MediaDeleteView.as_view(), name = 'media-delete'),

    path('post-media/new/', MediaCreateView.as_view(), name = 'media-create'),

    # projects
    
    path('projects/', ProjectListView.as_view(), name = 'projects-list'),

    path('projects/view-all', viewProjectDonations, name = 'projects-donations-list'),

    path('projects/<int:pk>/', ProjectDetailView.as_view(), name = 'projects-detail'),

    path('projects/<int:pk>/update/', ProjectUpdateView.as_view(), name = 'projects-update'),

    path('projects/<int:pk>/delete/', ProjectDeleteView.as_view(), name = 'projects-delete'),

    path('projects/new/', ProjectCreateView.as_view(), name = 'projects-create'),

    path('donate/project/<int:pk>/', ProjectDonation, name='donate-project'),

    # Other

    path('admin/', admin.site.urls),

    path('donorsignup/', donorSignUp, name='donorsignup'),

    path('volunteersignup/', volunteerSignUp, name='volunteersignup'),

    path('signup/', signup, name='signup'),

    path('profile/', profile, name='profile'),

    # path('projects/', don_views.projects, name='projects'),

    path('donation/history/donor/money/', don_views.donorMoneyDonationHistory, name='donorMoneyDonationHistory'),

    path('donation/history/donor/food/', don_views.donorFoodDonationHistory, name='donorFoodDonationHistory'),

    path('donation/history/donor/cloth/', don_views.donorClothDonationHistory, name='donorClothDonationHistory'),

    path('donation/history/volunteer/food/', don_views.volunteerFoodDonationPickUpHistory, name='volunteerFoodDonationHistory'),

    path('donation/history/volunteer/cloth/', don_views.volunteerClothDonationPickUpHistory, name='volunteerClothDonationHistory'),

    path('volunteer-confirmation/', volunteerConfirmation, name='volunteer_confirmation'),

    path('volunteer-list/', volunteerList, name='volunteer_list'),

    path('', home, name='home'),

    path('donate/', don_views.donate, name='donate'),

    path('donate/money/', don_views.donateMoney.as_view(), name='donate_money'),
    
    path('donate/food/', don_views.donateFood, name='donate_food'),

    path('donate/cloth/', don_views.donateCloth, name='donate_cloth'),

    path('donation/verification/money/', don_views.moneyDonationVerification, name='money_donation_verification'),
    
    path('donation/verification/food/', don_views.foodDonationVerification, name='food_donation_verification'),

    path('donation/verification/cloth/', don_views.clothDonationVerification, name='cloth_donation_verification'),
    
    path('donation/verification/project/', don_views.projectDonationVerification, name='project_donation_verification'),

    path('donation/assignment/food/', don_views.volunteerFoodDonationAssignment, name='volunteer_food_donation_assignment'),

    path('donation/assignment/cloth/', don_views.volunteerClothDonationAssignment, name='volunteer_cloth_donation_assignment'),

    path('donation/pickup/food/', don_views.volunteerFoodDonationPickUpConfirmation, name='volunteer_food_donation_pickup'),

    path('donation/pickup/cloth/', don_views.volunteerClothDonationPickUpConfirmation, name='volunteer_cloth_donation_pickup'),

    path('donation/delivery/food/', don_views.volunteerFoodDonationDeliveryConfirmation, name='volunteer_food_donation_delivery'),

    path('donation/delivery/cloth/', don_views.volunteerClothDonationDeliveryConfirmation, name='volunteer_cloth_donation_delivery'),

    path('donation/received/food/', don_views.donCoFoodDonationReceivedConfirmation, name='donco_food_donation_received'),

    path('donation/received/cloth/', don_views.donCoClothDonationReceivedConfirmation, name='donco_cloth_donation_received'),

    path('donation/inventory/cloth/<int:pk>/', don_views.clothInventoryFunc, name='cloth-inventory'),

    path('donation/inventory/food/<int:pk>/', don_views.foodInventoryFunc, name='food-inventory'),
    
    path('activate/<uidb64>/<token>', activate, name='activate'),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),

    path('password-reset-done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)