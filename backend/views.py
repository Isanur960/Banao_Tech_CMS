from django.http import request
from django.http.response import Http404
from django.shortcuts import redirect, render, HttpResponse
from django.contrib import messages
from django.views import View
from django.contrib.auth.models import User
from . models import Airticle
from django.contrib.auth import authenticate, login, logout
import random

# Create your views here.


def validate_pwd(pwd):
    if len(pwd)>=8:
        if pwd.isalnum():
            return "valid"
        else:
            return "invalid"
    else:
        return "small"
    
class Index(View):
    def get(self, request):
        return render(request, 'index.html')


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.INFO, 'Successfully Logged In')
            return redirect('Dashboard')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid Credentials')
            return render(request, 'login.html')

operator = ["*","-","+"]

def make_cookie(request):
    r1 = int(random.random()*10)
    r2 = int(random.random()*10)
    r3 = int(random.randrange(0, 3))
    d = {'r1': str(r1), 'r2': str(r2), 'r3': str(operator[r3])}
    res = render(request, 'signup.html', {'data': d})
    res.set_cookie("st", r1)
    res.set_cookie("nd", r2)
    res.set_cookie("op", r3)
    return res

class SignUp(View):
    def get(self, request):
        return make_cookie(request)
        

    def post(self, request):
        rc1 = request.COOKIES['st']
        rc2 = request.COOKIES['nd']
        rc3 = request.COOKIES['op']
        res = -1 
        if int(rc3) == 0:
            res = int(rc1) * int(rc2)
        elif int(rc3) == 1:
            res = int(rc1) - int(rc2)
        elif int(rc3) == 2:
            res = int(rc1) + int(rc2)
        username = request.POST.get('username')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        captcha = request.POST.get('captcha')
        if res != int(captcha):
            messages.add_message(request, messages.ERROR, 'Wrong captcha')
            return make_cookie(request)
        try: 
            User.objects.get(username=username)
            messages.add_message(request, messages.ERROR, 'Username already Exists')
            return make_cookie(request)
        except:
            pass
        if password == cpassword :
            val_res = validate_pwd(password)
            if val_res == "invalid":
                messages.add_message(request, messages.ERROR, 'Password should be AlphaNumeric')
                return make_cookie(request)
            elif val_res == "small":
                messages.add_message(request, messages.ERROR, 'Password should be atleast 8 character long')
                return make_cookie(request)
            elif val_res == "valid":
                pass
            else:
                messages.add_message(request, messages.ERROR, 'Something went wrong')
                return make_cookie(request)
        else:
            messages.add_message(request, messages.ERROR, 'Password and Confirm password should match')
            return make_cookie(request)

        usr = User.objects.create_user(username=username, password= password)
        usr.save()
        messages.add_message(request, messages.INFO, 'SignUp succesfull')
        return make_cookie(request)


class Dashboard(View):
    def get(self, request):
        if request.user.is_authenticated :
            user = request.user
            posts = Airticle.objects.filter(user=user)
            return render(request, 'dashboard.html',{'posts':posts})

        else:
            return redirect('Login')


class AddAirticle(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'add-airticle.html')
        else:
            return redirect('Login')

    def post(self, request):
        if request.user.is_authenticated:
            title = request.POST.get('title')
            desc = request.POST.get('description')
            img = request.FILES['airticle-image']
            user = User.objects.get(username= request.user)
            ispublic = request.POST.get('public_check')
            if ispublic is None:
                ispublic = False
            elif ispublic == 'on':
                ispublic = True
            try:
                airticle = Airticle(title=title,description=desc,img=img,public=ispublic,user = user)
                airticle.save()
                messages.add_message(request, messages.INFO, 'Addition succesfull')
                return redirect('Dashboard')
            except:
                messages.add_message(request, messages.ERROR, 'Addition Failed')
            return render(request, 'add-airticle.html')
        else:
            return redirect('Login')
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('Login')

class UserSearch(View):
    def get(self,request):
        pass

    def post(self,request):
        if request.user.is_authenticated:
            u_name = request.POST.get('search')
            result = User.objects.filter(username__icontains=u_name)
            return render(request, "searchpage.html", {'users': result})
        else:
            return redirect('Login')

class UserPosts(View):
    def get(self,request):
        if request.user.is_authenticated:
            id = request.GET.get('id')
            result = Airticle.objects.filter(user=id).filter(public=True)
            return render(request, "user-post.html", {'posts': result})
        else:
            return redirect('Login')

    def post(self,request):
        return Http404("Not found")
