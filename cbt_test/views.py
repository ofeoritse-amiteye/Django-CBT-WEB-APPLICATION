from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from cbt import settings
from cbt_test.models import questions,test,user_score
from django.core.mail import send_mail
import time
from bs4 import BeautifulSoup
from django.db.models import Q

from cbt_test.forms import UserRegistrationForm


def login_user(request):
    logout(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            if user.account_type == 'admin':
                username=user.get_username
                return redirect("/dashboard")
            elif user.account_type =='it_user':
                username=user.get_username
                return redirect("/index")
            elif user.account_type =='staff':
                username=user.get_username
                return redirect("/blank")
        else:
            error="wrong"
            return render(request,'html/login.html',{"error":error})
    return render(request, 'html/login.html')

def add_user(request):
    logout(request)
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registeration succesfull")
            redirect("/login")
            #return redirect('signin')
        else:
            form = UserRegistrationForm() 
            return render(request,"html/add_user.html",{'form': form})
    form = UserRegistrationForm()
    return render(request,"html/add_user.html",{'form': form})

@login_required    
def index(request):
    tests=test.objects.all()
    return render(request, 'html/index.html',{"tests":tests})


@login_required
def question(request):
    if request.method== "POST":
        title=request.POST.get("title")
        user=request.POST.get('user')
        if request.user.account_type == user:
            check=user_score.objects.filter(test=title) and user_score.objects.filter(Name=request.user.username)
            if check:
                tests=test.objects.all()
                message="you have already participated in this activity"
                return render(request, 'html/index.html',{"tests":tests,"message":message})
            else:
                duration=request.POST.get("duration")
                category=request.POST.get("category")
                display = questions.objects.filter(category=category)
                count =questions.objects.count()
                numbers = range(1, count+1)
            return render(request ,"html/questions.html",{"display":display,"numbers":numbers,"duration":duration,"cat":category,"title":title})
        else:
            tests=test.objects.all()
            message="You are not allowed to participate in this activity"
            return render(request, 'html/index.html',{"tests":tests,"message":message})
    else:
        tests=test.objects.all()
        return render(request, 'html/index.html',{"tests":tests})
        

@login_required    
def set_question(request):
    if request.method =="POST":
        no=questions.objects.filter(category="A")
        no2=questions.objects.filter(category="B")
        no3=questions.objects.filter(category="C")
        no4=questions.objects.filter(category="D")
        number=len(no)+1
        number2=len(no2)+1
        number3=len(no3)+1
        number4=len(no4)+1
        chk=request.POST.get("qno")
        cat=request.POST.get("category")
        chk2= questions.objects.filter(category__exact=cat,question_no__exact=chk)
        if chk2:
            error="DUPLICATE ENTRY AT CURRENT NUMBER"
            return render (request, "html/set_question.html",{"number":number,"number2":number2,"number3":number3,"number4":number4,"error":error,"chk":chk2})
        else: 
            reg=questions()
            reg.category=request.POST.get('category')
            reg.question_no=request.POST.get('qno')
            soup = BeautifulSoup(request.POST.get('question'), 'html.parser')
            text = soup.get_text()
            reg.question=text
            reg.answer=request.POST.get('ans')
            reg.opt_a =request.POST.get('opt_a')
            reg.opt_b =request.POST.get('opt_b')
            reg.opt_c =request.POST.get('opt_c')
            reg.opt_d =request.POST.get('opt_d')
            reg.save()
            no=questions.objects.filter(category="A")
            no2=questions.objects.filter(category="B")
            no3=questions.objects.filter(category="C")
            no4=questions.objects.filter(category="D")
            number=len(no)+1
            number2=len(no2)+1
            number3=len(no3)+1
            number4=len(no4)+1
            message="SAVED"
            return render(request,"html/set_question.html",{"number":number,"number2":number2,"number3":number3,"number4":number4,"message":message})
    else:
        no=questions.objects.filter(category="A")
        no2=questions.objects.filter(category="B")
        no3=questions.objects.filter(category="C")
        no4=questions.objects.filter(category="D")
        number=len(no)+1
        number2=len(no2)+1
        number3=len(no3)+1
        number4=len(no4)+1
        return render(request,"html/set_question.html",{"number":number,"number2":number2,"number3":number3,"number4":number4})


@login_required
def score(request):
    if request.method == 'POST':
        cat=request.POST.get("cat")
        if cat == "A":
            noq=questions.objects.filter(category="A")
        elif cat =="B":
            noq=questions.objects.filter(category="B")
        elif cat =="C":
            noq=questions.objects.filter(category="C")
        elif cat =="D":
            noq=questions.objects.filter(category="D")
        count =questions.objects.values_list('answer',flat=True)
        len1=len(noq)
        score=0
        answer=[]
        for x in range(len1+1):
            values = request.POST.get("option"+str(x)) 
            answer.append(values)
        for x in range(len1+1):
            if answer[x] in count :
                score=score+1
        title=request.POST.get("title")
        percent=(score/len1)*100
        if percent >=  50:
            grade = "PASS"
        else:
            grade = "Fail"
        time_used=request.POST.get("time_used")
        uname=request.user.username
        x=user_score()
        x.Name=uname
        x.test=request.POST.get("title")
        x.score=score
        x.grade=grade
        x.user=request.user.account_type
        x.save()
        display = questions.objects.filter(category=cat)
        return render(request,"html/score.html",{"values":answer,"message":"YOU SCORED","count":count,"len":len1,"score":score,"percent":percent,"title":title,"time":time_used,"question":display})
    else:
        return render(request, "html/score.html") 

def signout(request):
        logout(request)
        return redirect('/login')

@login_required
def dashboard(request):
    return render(request , "html/dashboard.html")

@login_required
def set_test(request):
    if request.method == "POST":
        x=test()
        x.title=request.POST.get("title")
        x.category=request.POST.get("category")
        x.duration=request.POST.get("duration")
        x.participant=request.POST.get("participant")
        x.save()
        message="SUCCESFULL"
        return render ( request,"html/dashboard.html",{"message":message})
    return render(request, "html/dashboard.html")


def blank(request):
    return render(request, "html/blank.html")

def result(request):
    x=user_score.objects.filter(user="it_user")
    y=user_score.objects.filter(user="staff")
    if x:
        return render(request, "html/result_analysis.html",{"results":x,"y":y})
    else:
        return render(request, "html/result_analysis.html")
