from django.urls import path
from .views import home_view, register_view, login_view, logout_view, dashboard_view, follow_view, follow_view_display, \
    search_user, upload_view, profile_view, update_profile, update_media, delete_media, update_user, like_post, \
    comment_post, reply_to_comment, profile_likedusers, profie_commentedusers, profile_viewed, unfollow_view


urlpatterns = [
    path('register/', register_view, name='register'),
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('search_user/', search_user, name='search_user'),
    path('logout/', logout_view, name='logout'),
    path('upload/', upload_view, name='upload'),
    path('profile/', profile_view, name='profile'),
    path('update_profile/', update_profile, name='update_profile'),
    path('update_personal/', update_user, name='update_personal'),
    path('update_media/<int:media_id>/', update_media, name='update_media'),
    path('delete_media/<int:media_id>/', delete_media, name='delete_media'),
    path('like_post/<int:media_id>/', like_post, name='like_post'),
    path('comment_post/<int:media_id>/', comment_post, name='comment_post'),
    path('reply_to_comment/<int:comment_id>/', reply_to_comment, name='reply_to_comment'),
    path('profile_likedusers/<int:media_id>/', profile_likedusers, name='profile_likedusers'),
    path('profile_commentedusers/<int:media_id>/', profie_commentedusers, name='profile_commentedusers'),
    path('profile_viewed/<str:username>/', profile_viewed, name='profile_viewed'),
    path('follow/<str:username>/', follow_view, name='follow_view'),
    path('following/', follow_view_display, name='follow_view_display'),
    path('unfollow/<str:username>/', unfollow_view, name='unfollow_view'),
]
