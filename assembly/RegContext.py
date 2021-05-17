from django.contrib.auth.forms import UserCreationForm

from assembly.forms import UserRegisterForm,UserLoginForm


def RegContext(request):
    form = UserRegisterForm()

    context={
        'title':'Register',
        'form':form,
    }
    return context
