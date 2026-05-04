from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Tweet,Profile
from .forms import TweetForm,UserRegistrationForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q

def index(request):
    return render(request, 'index.html')


def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request,"tweet_list.html",{'tweets':tweets})

@login_required
def tweet_create(request):
    if request.method =='POST':
        form= TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet= form.save(commit=False)
            tweet.user=request.user
            tweet.save()
            return redirect('tweet_list')

    else:
        form=TweetForm()
    return render(request,"tweet_form.html",{'form':form})

@login_required
def tweet_edit(request,tweet_id):
    tweet=get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method=='POST':
        form=TweetForm(request.POST,request.FILES,instance=tweet)
        if form.is_valid():
            tweet.user=request.user
            tweet.save()
            return redirect('tweet_list')

    else:
        form=TweetForm(instance=tweet)
    
    return render(request,"tweet_form.html",{'form':form})

@login_required
def tweet_delete(request,tweet_id):
    tweet=get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method=='POST':
        tweet.delete()
        return redirect('tweet_list')
    
    return render(request,'tweet_confirm_delete.html',{'tweet':tweet})

def register(request):

    if request.method=="POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])        
            user.save()               
            login(request,user)
            return redirect('tweet_list')
    else:
        form=UserRegistrationForm()
    return render(request,'registration/register.html',{'form':form})

def profile(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    profile_obj = get_object_or_404(Profile, user=user_obj)
    tweets = Tweet.objects.filter(user=user_obj).order_by('-created_at')
    context = {
        'obj': profile_obj,
        'tweets': tweets,
    }
    return render(request, 'view_profile.html', context)

def myprofile(request):
    
    profile_obj = get_object_or_404(Profile, user=request.user)
    tweets = Tweet.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'obj': profile_obj,
        'tweets': tweets,
    }
    return render(request, 'view_profile.html', context)


def search_tweet(request):
    query = request.POST.get('data')
    if query:
        tweets = Tweet.objects.filter(
            Q(text__icontains=query) | Q(user__username__icontains=query)
        ).order_by('-created_at')
    else:
        tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, "tweet_list.html", {"tweets": tweets, "query": query})


