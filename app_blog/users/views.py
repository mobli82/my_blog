from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistartionForm, UserUpdateProfileForm

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

@login_required
def profile(request):

    if request.method == 'POST':
        update_profile_form = UserUpdateProfileForm(request.POST, instance=request.user)
        
        if update_profile_form.is_valid():
            update_profile_form.save()
            messages.success(request, f'Account hass been updated !!')
            return redirect('posts')
        
    else:
        update_profile_form = UserUpdateProfileForm(instance=request.user)

    return render(request, 'users/profile.html', {'update_profile_form': update_profile_form})
