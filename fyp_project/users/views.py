import imp
from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import UserRegistrationForm

# Create your views here.

def registerPlacecomUser(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Created, Welcome {username}!')
            return redirect('/home/recruiter/', username=username)
    else:
        form = UserRegistrationForm()

    return render(request, 'user-templates/register.html', {'form': form})

