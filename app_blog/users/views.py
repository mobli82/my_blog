from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistartionForm

# Create your views here.

def register(request):

    if request.method == 'POST':
        form = UserRegistartionForm(request.POST)

        if form.is_valid():
            messages.success(request, f'Your Account has been created successfully')
            form.save()
    
    else:
        form = UserRegistartionForm()


    return render(request, 'users/register.html', {'form': form})