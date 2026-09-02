from django.shortcuts import render, redirect

from accounts.forms import RegisterForm, LoginForm


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            request.session['registered_user'] = form.cleaned_data['username']
            return redirect('accounts:register_success')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['active_user'] = form.cleaned_data['username_or_mail']
            return redirect('accounts:dashboard')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def register_success(request):
    return render(
        request,
        'accounts/register_success.html',
        {'username': request.session.get('registered_user', 'New user')},
    )

def dashboard_view(request):
    return render(
        request,
        'accounts/dashboard.html',
        {'active_user': request.session.get('active_user','Guest')},
    )