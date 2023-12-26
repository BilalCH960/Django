from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.decorators.cache import cache_control
from .forms import Form



# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
  if request.user.is_superuser:
    return redirect(adminpanel)
  # if 'username' in request.session:
  if request.user.is_authenticated:
    return render(request,'index.html')
  return redirect(handlelogin)
  


# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def handlelogin(request):
#   if request.user.is_authenticated:
#     return redirect(index)
  

#   if request.method=="POST":
#     uname=request.POST.get("username")
#     pass1=request.POST.get("pass1")
#     myuser=authenticate(username=uname,password=pass1)
#     if myuser is not None:
#         # request.session['username'] = uname 
#         login(request,myuser)
#         # if myuser.is_superuser:
#         #   return redirect(adminpanel)
#         # else:
#         return redirect (index)
#         messages.success(request,'You have Logged in Successfully.')
#         return redirect('/')  

#     else:
#       messages.error(request,'Invalid Credentials.')
#       return redirect('/login')

#   return render(request,'login.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def handlesignup(request):
  if request.user.is_authenticated:
    return redirect(index)
  if request.method=="POST":
    uname=request.POST.get("username")
    fname=request.POST.get("firstname")
    lname=request.POST.get("lastname")
    email=request.POST.get("email")
    password=request.POST.get("pass1")
    confirmpassword=request.POST.get("pass2")
    if len(password) < 8:
      messages.warning(request,"Password must be minimum 8 characters")
      return redirect('/signup')
    elif password!=confirmpassword:
      messages.warning(request,"Password does not match")
      return redirect('/signup')

    try:
      if User.objects.get(username=uname):
        messages.info(request,"This Username is already taken")
        return redirect('/signup')
    except:
      pass

    try:
      if User.objects.get(email=email):
        messages.info(request,"This Email is already taken")
        return redirect('/signup')
    except:
      pass

    myuser=User.objects.create_user(username=uname,first_name=fname,last_name=lname,email=email,password=password)
    messages.success(request,"You have signed up successfully. Please Login")
    return redirect('/login')

  return render(request,'signup.html')



def handlelogout(request):
  # if 'username' in request.session:
  #   request.session.flush()
  logout(request)
  messages.info(request,"You have Logged out Successfully")
  return redirect("/login")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def handlelogin(request):
  if request.user.is_superuser:
    return redirect(adminpanel)
  elif request.user.is_authenticated:
    return redirect(index)
  

  if request.method=="POST":
    uname=request.POST.get("username")
    pass1=request.POST.get("pass1")
    myuser=authenticate(username=uname,password=pass1)
    if myuser is not None:
        # request.session['username'] = uname 
        login(request,myuser)
        if myuser.is_superuser:
          return redirect(adminpanel)
        else:
          return redirect (index)
        messages.success(request,'You have Logged in Successfully.')
        return redirect('/')  

    else:
      messages.error(request,'Invalid Credentials.')
      return redirect('/login')

  return render(request,'login.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminpanel(request):
  if not request.user.is_superuser:
    return redirect(index)
  users = User.objects.all()
  if request.method=="POST":
    search_word=request.POST.get("search")
    users = User.objects.filter(username__icontains=search_word)
  return render(request,'admin.html',{'user':users}) 


def updateuser(request,id):

  users = User.objects.get(id=id) 
  # froms=Form(instance=users)
  if request.method=="POST":
    username=request.POST.get('username')
    firstname=request.POST.get('firstname')
    lastname=request.POST.get('lastname')
    email=request.POST.get('email')

    users.username=username
    users.first_name=firstname
    users.last_name=lastname
    users.save()
    messages.success(request,"updated succesfully !")
  return render(request,'edit.html',{'i':users})



def deleteuser(request,id):
  users = User.objects.get(id=id)

  users.delete()
  return redirect("/adminn")


# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
def createuser(request):
  print("hellooo")

  if request.method=="POST":
    print("hiiiiiiiiiiiiiiii")
    uname=request.POST.get("username")
    fname=request.POST.get("firstname")
    lname=request.POST.get("lastname")
    email=request.POST.get("email")
    password=request.POST.get("pass1")
    confirmpassword=request.POST.get("pass2")
    if len(password) < 8:
      messages.warning(request,"Password must be minimum 8 characters")
      return redirect('/create')
    elif password!=confirmpassword:
      messages.warning(request,"Password does not match")
      return redirect('/create')

    try:
      if User.objects.get(username=uname):
        messages.info(request,"This Username is already taken")
        return redirect('/create')
    except:
      pass

    try:
      if User.objects.get(email=email):
        messages.info(request,"This Email is already taken")
        return redirect('/create')
    except:
      pass

    myuser=User.objects.create_user(username=uname,first_name=fname,last_name=lname,email=email,password=password)
    messages.success(request,"User created")
    return redirect('/adminn')

  return render(request,'admincreate.html')
