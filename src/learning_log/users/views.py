from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def logout_view(request):
    '''Faz o logout do usuario logado'''
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def signup(request):
    '''Cadastrando um usuario novo'''
    #nao permitindo que um usuario cadastre outro usuario quando authenticado
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            #salvando dos dados preenchidos pelo user
            new_user = form.save()
            #autenticando e logando o usuario
            authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
            login(request, authenticated_user)
            #redirecionando o usuario autenticado para a index
            return HttpResponseRedirect(reverse('index'))
    
    context = {'form': form}
    return render(request, 'users/signup.html', context)