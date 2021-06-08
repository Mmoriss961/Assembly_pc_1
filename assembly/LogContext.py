from assembly.forms import UserLoginForm

def LogContext(request):
    form1 = UserLoginForm()
    context={

        'form1':form1,
    }
    return context