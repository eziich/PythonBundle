from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, MediaUploadForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Media, Follow, Profile, Like, Comment, CommentReply
from django.contrib import messages

def home_view(request):
    return render(request, 'home/home.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            profile_picture = request.FILES.get('profile_picture')

            if User.objects.filter(username=username).exists():
                form.add_error('username', 'This username is already in use')
            elif User.objects.filter(email=email).exists():
                form.add_error('email', 'This email address is already in use')
            elif password1 != password2:
                form.add_error('password2', 'Password mismatch')
            else:
                user = form.save(commit=False)
                user.set_password(password1)
                user.save()
                profile = Profile.objects.create(user=user, profile_picture=profile_picture)
                login(request, user)
                return redirect('dashboard')  # Adjust the redirect URL as per your project
    else:
        form = RegisterForm()
    return render(request, 'register/register.html', {'form': form})


def login_view(request):
    error_message = None

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
        else:
            error_message = "You have not entered a valid username or password!"

    else:
        form = AuthenticationForm()
    return render(request, 'login/login.html', {'form': form, 'error_message': error_message})

@login_required()
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    all_media = Media.objects.exclude(media_uploader=request.user).order_by('-id')

    for media in all_media:
        media.is_following = request.user.following.filter(follow_followed=media.media_uploader).exists()

    context = {
        'all_media': all_media,
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required()
def search_user(request):
    if request.method == 'GET':
        search_query = request.GET.get('search_query', '')

        users = User.objects.filter(username__icontains=search_query)
        return render(request, 'search/search_user.html', {'users': users, 'search_query': search_query})

    return render(request, 'search/search_user.html', {})


@login_required
def upload_view(request):
    if request.method == 'POST':
        form = MediaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            media = form.save(commit=False)
            media.media_uploader = request.user
            media.save()
            return redirect('dashboard')
    else:
        form = MediaUploadForm()
    return render(request, 'upload/upload.html', {'form': form})


@login_required()
def profile_view(request):
    user_profile = Profile.objects.get(user=request.user)
    user_media = Media.objects.filter(media_uploader=request.user)


    for media in user_media:
        media.likes_count = Like.objects.filter(media=media).count()
        media.comments = Comment.objects.filter(media=media)

    context = {
        'user_profile': user_profile,
        'user_media': user_media,

    }
    return render(request, 'profile/profile.html', context)


@login_required
def follow_view(request, username):
    followed_user = get_object_or_404(User, username=username)

    if not request.user.following.filter(follow_followed=followed_user).exists():
        Follow.objects.create(follow_follower=request.user, follow_followed=followed_user)

    return redirect('dashboard')

@login_required
def follow_view_display(request):
    # Collect all users the current user is following
    followed_users = request.user.following.all().values_list('follow_followed', flat=True)

    # Pass data to the template, even if the queryset is empty
    if followed_users:
        # Collect all media posted by users the current user is following
        followed_users_media = Media.objects.filter(media_uploader__in=followed_users)
    else:
        followed_users_media = []

    return render(request, 'follow/follow.html', {'followed_users_media': followed_users_media})




@login_required()
def update_media(request, media_id):
    media = get_object_or_404(Media, id=media_id)

    if request.method == 'POST':
        new_description = request.POST.get('new_description')
        media.media_description = new_description
        media.save()
        return redirect('profile')

    return render(request, 'profile/update_media.html', {'media': media})

@login_required()
def delete_media(request, media_id):
    media = get_object_or_404(Media, id=media_id)

    if request.method == 'POST':
        media.delete()
        return redirect('profile')

    return render(request, 'delete_media.html', {'media': media})


@login_required()
def profile_viewed(request, username=None):
    if username:

        user_profile = get_object_or_404(Profile, user__username=username)
        user_media = Media.objects.filter(media_uploader=user_profile.user)
    else:

        user_profile = get_object_or_404(Profile, user=request.user)
        user_media = Media.objects.filter(media_uploader=request.user)

    context = {
        'user_profile': user_profile,
        'user_media': user_media,
    }

    return render(request, 'profile/profile_viewed.html', context)

@login_required
def update_user(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been successfully updated')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    context = {'form': form}
    return render(request, 'profile/update_personal.html', context)

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been successfully updated')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    context = {'form': form}
    return render(request, 'profile/update_profile.html', context)


@login_required
def like_post(request, media_id):
    media = get_object_or_404(Media, pk=media_id)

    if request.user in media.media_likes.all():
        return redirect('dashboard')
    else:
        media.media_likes.add(request.user)
        return redirect('dashboard')



@login_required
def comment_post(request, media_id):
    media = get_object_or_404(Media, pk=media_id)

    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')

        if comment_text:
            comment = Comment.objects.create(
                media=media,
                user=request.user,
                comment_description=comment_text
            )
        else:
            return redirect('dashboard')

    return redirect('dashboard')


@login_required
def reply_to_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == 'POST':
        reply_text = request.POST.get('reply_text')

        if reply_text:
            reply = CommentReply.objects.create(
                comment=comment,
                user=request.user,
                reply_description=reply_text
            )
            return redirect('dashboard')
        else:
            return redirect('dashboard')

    return redirect('dashboard')


@login_required()
def profile_likedusers(request, media_id):
    media = get_object_or_404(Media, pk=media_id)


    media_file_url = media.media_file.url
    liked_users = media.media_likes.all()

    print("Media File URL:", media_file_url)

    context = {
        'media': media,
        'liked_users': liked_users,
    }

    return render(request, 'profile/profile_likedusers.html', context)

@login_required()
def profie_commentedusers(request, media_id):
    media = get_object_or_404(Media, pk=media_id)
    comments = Comment.objects.filter(media=media)
    return render(request, 'profile/profile_commentedusers.html', {'media': media, 'comments': comments})

@login_required
def unfollow_view(request, username):
    unfollowed_user = get_object_or_404(User, username=username)

    follow_instance = request.user.following.filter(follow_followed=unfollowed_user).first()

    if follow_instance:
        follow_instance.delete()

    return redirect('dashboard')




