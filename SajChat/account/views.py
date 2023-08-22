from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Account, Friend
from django.conf import settings
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm


def register_view(request, *args, **kwargs):
	user = request.user
	if user.is_authenticated: 
		return HttpResponse(f"You are already authenticated as {user.email}.")
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid(): 
			form.save()

			email = form.cleaned_data.get('email').lower()
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			addfriend = Account.objects.get(email=email)
			friend = Friend.objects.create(profile=addfriend)
			login(request, account)
			destination = get_redirect_if_exists(request)
			if destination:
				return redirect(destination)
			return redirect('home')
		else:
			context['registration_form'] = form

	else:
		form = RegistrationForm()
		context['registration_form'] = form

	return render(request, 'account/register.html', context)


def logout_view(request):
	logout(request)
	return redirect("home")


def login_view(request, *args, **kwargs):
	context = {}

	user = request.user
	if user.is_authenticated: 
		return redirect("home")

	destination = get_redirect_if_exists(request)
	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)
			if user:
				# if user not in Friend:
				# 	Friend.add_friend(user)
				login(request, user)
				destination = get_redirect_if_exists(request)
				if destination:
					return redirect(destination)
				return redirect('home')
		else:
			context['login_form'] = form
	return render(request, "account/login.html", context)


def get_redirect_if_exists(request):
	redirect = None
	if request.GET:
		if request.GET.get("next"):
			redirect = str(request.GET.get("next"))
	return redirect

@login_required(login_url='/login/')
def account_search_view(request, *args, **kwargs):
	context = {}
	if request.method == "GET":
		search_query = request.GET.get("q")
		if len(search_query) > 0:
			search_results = Account.objects.filter(username__icontains=search_query)
			accounts = [] # [(account1, True), (account2, False), ...]
			for account in search_results:
				accounts.append((account, False)) # you have no friends yet
			context['accounts'] = accounts
				
	return render(request, "account/search_results.html", context)

@login_required(login_url='/login/')
def account_view(request, *args, **kwargs):
	context = {}
	user_id = kwargs.get("user_id")
	try:
		account = Account.objects.get(pk=user_id)
	except:
		return HttpResponse("Something went wrong.")
	if account:
		context['id'] = account.id
		context['username'] = account.username
		context['email'] = account.email
		context['hide_email'] = account.hide_email

		# Define template variables
		is_self = False
		is_other = False
		user = request.user
		if user.is_authenticated and user == account:
			is_self = True
		elif user.is_authenticated and user != account:
			is_other = True
		else:
			pass

		# Set the template variables to the values
		context['is_self'] = is_self
		context['is_other'] = is_other
		return render(request, "account/account.html", context)



@login_required(login_url='/login/')
def edit_account_view(request, *args, **kwargs):
	if not request.user.is_authenticated:
		return redirect("login")
	user_id = kwargs.get("user_id")
	account = Account.objects.get(pk=user_id)
	if account.pk != request.user.pk:
		return HttpResponse("You cannot edit someone elses profile.")
	context = {}
	if request.POST:
		form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
		if form.is_valid():
			form.save()
			new_username = form.cleaned_data['username']
			return redirect("account:view", user_id=account.pk)
		else:
			form = AccountUpdateForm(request.POST, instance=request.user,
				initial={
					"id": account.pk,
					"email": account.email, 
					"username": account.username,
					"hide_email": account.hide_email,
				}
			)
			context['form'] = form
	else:
		form = AccountUpdateForm(
			initial={
					"id": account.pk,
					"email": account.email, 
					"username": account.username,
					"hide_email": account.hide_email,
				}
			)
		context['form'] = form
	return render(request, "account/edit_account.html", context)


