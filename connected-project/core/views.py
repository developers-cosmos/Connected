from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost, FollowersCount
from itertools import chain
import random

def home(request):
    return render(request, 'core/home.html')

@login_required(login_url='login')
def profile(request, pk):
    try:
        user = User.objects.get(username=pk)
        user_profile = Profile.objects.get(user=user)

        # posts data
        user_posts = Post.objects.filter(user=pk)
        user_post_length = len(user_posts)

        follower = request.user.username
        if FollowersCount.objects.filter(follower=follower, user=pk).first():
            follow_button_text = 'Unfollow'
        else:
            follow_button_text = 'Follow'

        user_followers = len(FollowersCount.objects.filter(user=pk))
        user_following = len(FollowersCount.objects.filter(follower=pk))

    except User.DoesNotExist:
        return render(request, "core/404.html")

    context = {
        "user_object": user,
        'user_profile': user_profile,
        'posts': user_posts,
        'user_post_length': user_post_length,
        'follow_button_text': follow_button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, "core/profile.html", context)

@login_required(login_url='login')
def explore(request):
    user_profile = Profile.objects.get(user=request.user)
    user_following_list = []
    feed = []
    liked_posts = []
    liked_posts_ids = []

    user_following = FollowersCount.objects.filter(follower=request.user.username)
    for follow_obj in user_following:
        user_following_list.append(follow_obj.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    liked_posts.append(LikePost.objects.filter(username=request.user.username))
    feed_list = list(chain(*feed))
    liked_posts = list(chain(*liked_posts))

    for like in liked_posts:
        liked_posts_ids.append(int(like.post_id))

    # suggest users
    all_users = User.objects.all()
    user_following_all = []
    current_user = User.objects.filter(username=request.user.username)

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    suggestions_list = [x for x in list(suggestions_list) if ( x not in list(current_user))]

    random.shuffle(suggestions_list)
    user_ids = []
    username_profile_list = []

    for users in suggestions_list:
        user_ids.append(users.id)

    for ids in user_ids:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))

    return render(request, 'core/explore.html', {'user_profile': user_profile, 'posts': feed_list, 'liked_posts_ids': liked_posts_ids, 'suggestions_username_profile_list': suggestions_username_profile_list[:10]})

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect(f"profile/{username}")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "core/login.html")

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.warning(request, 'Email Taken')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.warning(request, 'Username Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # log user in and redirect to profile page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                # create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()

                messages.success(request, 'Profile created successfully')
                return redirect('login')
        else:
            messages.error(request, 'Password Not Matching')
            return redirect('register')
    else:
        return render(request, 'core/register.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def edit_profile(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        profile_picture = request.FILES.get("profile_picture")
        bio = request.POST.get("bio")
        location = request.POST.get("location")

        if profile_picture:
            user_profile.image = profile_picture

        if bio:
            user_profile.bio = bio

        if location:
            user_profile.location = location

        messages.success(request, 'Profile is updated successfully')
        user_profile.save()
        return redirect('edit_profile')

    return render(request, "core/edit_profile.html", {'user_profile': user_profile})

@login_required(login_url='login')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect(f'/profile/{user}')
    else:
        return redirect('explore')

@login_required(login_url='login')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    post = get_object_or_404(Post, pk=post_id)

    like, created = LikePost.objects.get_or_create(post_id=post_id, username=username)

    if not created:
        delete_like = LikePost.objects.get(post_id=post_id, username=username)
        delete_like.delete()
        post.likes -= 1
        post.save()
    else:
        like.save()
        post.likes += 1
        post.save()

    return redirect('explore')

@login_required(login_url='login')
def follow(request):
    follower = request.POST['follower']
    user = request.POST['user']
    follow, created = FollowersCount.objects.get_or_create(user=user, follower=follower)
    if not created:
        delete_follower = FollowersCount.objects.get(follower=follower, user=user)
        delete_follower.delete()
    else:
        follow.save()
    return redirect(f'/profile/{user}')

@login_required(login_url='login')
def search(request):
    query = request.POST['username']

    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    try:
        users = User.objects.filter(username__icontains=query)
    except User.DoesNotExist:
        return render(request, "core/404.html")

    username_profile = []
    username_profile_list = []

    for user in users:
        username_profile.append(user.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    username_profile_list = list(chain(*username_profile_list))
    return render(request, 'core/search.html', {'query': query, 'user_profile': user_profile, 'username_profile_list': username_profile_list})

@login_required(login_url='login')
def delete_post(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return redirect('profile', pk=request.user.username)
