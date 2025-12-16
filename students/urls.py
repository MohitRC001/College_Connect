from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_students, name='all_students'),

    path('register/', views.register, name='register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    
    path('profile/', views.profile, name='profile'),
    path('view_profile/<str:student_id>', views.view_profile, name='view_profile'),
    path('sent_follow_requests/', views.sent_follow_requests, name='sent_follow_requests'),
    path('received_follow_requests/', views.received_follow_requests, name='received_follow_requests'),
    path('send_follow_requests/<str:student_id>', views.send_follow_requests, name='send_follow_requests'),
    path('delete_follow_requests/<str:student_id>', views.delete_follow_requests, name='delete_follow_requests'),
    path('accept_follow_requests/<str:request_id>', views.accept_follow_requests, name='accept_follow_requests'),
    path('reject_follow_requests/<str:request_id>', views.reject_follow_requests, name='reject_follow_requests'),
    path('followers/', views.followers, name='followers'),
    path('followings/', views.followings, name='followings'),
    path('unfollow/<str:student_id>', views.unfollow, name='unfollow'),
    path('remove_follower/<str:student_id>', views.remove_follower, name='remove_follower'),
    path("explore/", views.explore_students, name="explore_students"),

    path('add_skill/', views.add_skill, name='add_skill'),
    path('edit_skill/<int:skill_id>/', views.edit_skill, name='edit_skill'),
    path('delete_skill/<int:skill_id>/', views.delete_skill, name='delete_skill'),
    path('all_skills/', views.all_skills, name='all_skills'),

    path('add_interest/', views.add_interest, name='add_interest'),
    path('edit_interest/<int:interest_id>/', views.edit_interest, name='edit_interest'),
    path('delete_interest/<int:interest_id>/', views.delete_interest, name='delete_interest'),
    path('all_interests/', views.all_interests, name='all_interests'),

    path('add_experience/', views.add_experience, name='add_experience'),
    path('edit_experience/<int:exp_id>/', views.edit_experience, name='edit_experience'),
    path('delete_experience/<int:exp_id>/', views.delete_experience, name='delete_experience'),
    path('all_experiences/', views.all_experiences, name='all_experiences'),
]


