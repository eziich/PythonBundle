from django import forms
from .models import Profile, Media
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm

class RegisterForm(UserCreationForm):
    profile_bio = forms.CharField(max_length=500, required=False)
    profile_picture = forms.ImageField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        profile_bio = self.cleaned_data.get('profile_bio')
        profile_picture = self.cleaned_data.get('profile_picture')

        if commit:
            user.save()
            Profile.objects.create(user=user, profile_bio=profile_bio, profile_picture=profile_picture)

        return user

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data['profile_picture']
        if profile_picture:
            if profile_picture.size > 10 * 1024 * 1024:
                raise forms.ValidationError("Profile picture is too large (max 10 MB)")
            allowed_types = ['image/jpeg', 'image/png', 'image/gif']
            if profile_picture.content_type not in allowed_types:
                raise forms.ValidationError("Unsupported file type. Only JPEG, PNG, and GIF are supported.")
        return profile_picture


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']



class MediaUploadForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['media_title', 'media_description', 'media_type', 'media_file']

    def __init__(self, *args, **kwargs):
        super(MediaUploadForm, self).__init__(*args, **kwargs)
        self.fields['media_file'].required = True

    def clean(self):
        cleaned_data = super().clean()
        media_file = cleaned_data.get('media_file')

        if not media_file:
            raise forms.ValidationError("You must upload a file.")
        return cleaned_data


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This username is already taken!")
        return username

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'profile_bio']

