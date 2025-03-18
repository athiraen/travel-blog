from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import blog_listmodel
from .forms import blog_listform
from .forms import Profile
from .forms import ProfileUpdateForm
from itertools import chain




def index(request):
    return render(request,"index.html")
def contact(request):
    return render(request,"contact.html")
def loginn(request):
    return render(request,"login.html")

def sign_up(request): 
    if request.method == 'POST':
        f_name=request.POST['Fname']
        l_name=request.POST['Lname']
        u_name=request.POST['Uname']
        email=request.POST['email']
        password1=request.POST['password']
        password2=request.POST['cpassword']
        profile_picture = request.FILES.get('profile_picture')

        if password1==password2:
            if User.objects.filter(username=u_name).exists():
                messages.info(request,"username alredy exist")
                return redirect('sign_up')
            elif User.objects.filter(email=email).exists():
                messages.info(request,"email alredy exist")
                return redirect('sign_up')

            else:
                user=User.objects.create_user(first_name=f_name,last_name=l_name,username=u_name,email=email,password=password1)
                user.save()
                Profile.objects.create(user=user, profile_picture=profile_picture)
                return redirect('log_in')
            
        else:
            messages.info(request,"password are not matching") 
            return render(request,'sign_up.html')
    else:
        return render(request,'sign_up.html')
    

def log_in(request):
    if request.method=="POST":
        u_name=request.POST['Uname']
        password1=request.POST['password']
        user=auth.authenticate(username=u_name,password=password1)
        if user is not None:
            auth.login(request,user)
            return redirect('index')
        else:
            messages.info(request,'invalid username or password')
            return redirect('log_in')
    else:
        return render(request,'log_in.html')
    
def logout(request):
    auth.logout(request)
    return redirect('index')
 


def add_blog(request):
    if request.method == 'POST':
        form = blog_listform(request.POST, request.FILES,)
        if form.is_valid():
            blog_instance = form.save(commit=False)
            if request.user.is_authenticated:
                blog_instance.author = request.user
            blog_instance.save()
            return redirect('blog')  
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = blog_listform()  

    return render(request, 'add_blog.html', {'form': form})


def blog_list(request):
    if request.user.is_authenticated:
        user_blogs = blog_listmodel.objects.filter(author=request.user).order_by('-updated_at')
        other_blogs = blog_listmodel.objects.exclude(author=request.user).order_by('-updated_at')
        blogs = chain(user_blogs, other_blogs)
    else:
        blogs = blog_listmodel.objects.all().order_by('-created_at')

    return render(request, 'blog_list.html', {'blogs': blogs})



def blog_detials(request,id):
    blog=get_object_or_404(blog_listmodel, id=id) 
    context={'blog':blog} 
    return render(request,'blog_details.html',context)

def delete(request, id):
    blog_listmodel.objects.filter(id=id).delete()  
    return redirect('blog') 


def edit_blog(request, id):
    instance_to_be_edited = get_object_or_404(blog_listmodel, id=id) 
    if request.method == 'POST':
        form = blog_listform(request.POST, request.FILES, instance=instance_to_be_edited)  
        if form.is_valid():
            form.save()  
            return redirect('blog')  
    else:
        form = blog_listform(instance=instance_to_be_edited)  
    
    return render(request, 'edit_blog.html', {'frm': form})  


def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)  
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')  
    else:
        form = ProfileUpdateForm(instance=profile)
    
    return render(request, "profile.html", {"form": form, "profile": profile})


def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        username = request.POST['username']
        email = request.POST['email']
        
        if username != user.username and User.objects.filter(username=username).exists():
            messages.info(request,"username alredy exist")
            return redirect('edit_profile')
        if email != user.email and User.objects.filter(email=email).exists():
            messages.info(request,"email alredy exist")
            return redirect('edit_profile')
        
        user.first_name = request.POST['first_name']
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.save()

        profile = user.profile  
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
            profile.save()

        messages.success(request, 'Your profile has been updated!')
        return redirect('profile')  
    
   
    profile = request.user.profile
    return render(request, 'edit_profile.html', {'profile': profile})

