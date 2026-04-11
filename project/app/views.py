from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import authenticate,login
from app.forms import CustomUserCreationForm

class Register(View):
    template_name = 'registration/register.html'

    def get(self,request):
        context = {
            "form":CustomUserCreationForm()
        }
        return render(request,self.template_name,context)
    def post(self,request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username,password=password)
            login(request,user)
            return redirect('home')
        context = {
            'form':form
        }
        return render(request,self.template_name,context)