from .forms import LoginForm, RegisterForm

def auth_forms(request):
    login_form_data = request.session.pop('login_form_data', None)
    register_form_data = request.session.pop('register_form_data', None)

    login_form = LoginForm(initial=login_form_data) if login_form_data else LoginForm()
    register_form = RegisterForm(initial=register_form_data) if register_form_data else RegisterForm()

    return {
        'login_form': login_form,
        'register_form': register_form,
        'show_login_modal': request.session.pop('show_login_modal', False),
        'show_reg_modal': request.session.pop('show_reg_modal', False),
    }
