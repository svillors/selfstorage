from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now
from django.contrib.auth.models import User
from warehouse_app.models import Warehouse, Profile, Order, Box
from .forms import RegisterForm, LoginForm, ProfileForm


def index(request):
    login_form_data = request.session.pop('login_form_data', None)
    login_failed = request.session.pop('login_failed', False)

    if login_form_data:
        login_form = LoginForm(login_form_data)
        login_form.is_valid()
        if login_failed:
            login_form.add_error(None, "Неверный логин или пароль")
    else:
        login_form = LoginForm()

    register_form_data = request.session.pop('register_form_data', None)
    if register_form_data:
        register_form = RegisterForm(register_form_data)
        register_form.is_valid()
    else:
        register_form = RegisterForm()

    show_login_modal = request.session.pop('show_login_modal', False)
    show_reg_modal = request.session.pop('show_reg_modal', False)

    return render(request, 'index.html', {
        'login_form': login_form,
        'register_form': register_form,
        'show_login_modal': show_login_modal,
        'show_reg_modal': show_reg_modal
    })


def faq(request):
    return render(request, 'faq.html')


def boxes(request):
    warehouses = Warehouse.objects.prefetch_related('boxes').all()
    return render(request, 'boxes.html', {'warehouses': warehouses})


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            request.session['register_form_data'] = request.POST
            request.session['show_reg_modal'] = True
            return redirect('index')
    return redirect('index')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['identifier']
            password = form.cleaned_data['password']

            try:
                user_obj = User.objects.get(email=identifier)
                username = user_obj.username
            except User.DoesNotExist:
                username = identifier

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')
            else:
                request.session['login_failed'] = True
        else:
            request.session['login_failed'] = True

        request.session['login_form_data'] = request.POST
        request.session['show_login_modal'] = True
        return redirect('index')
    return redirect('index')


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def profile_view(request):
    user = request.user
    try:
        profile = user.profile
    except:
        profile = Profile.objects.create(user=user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('my-rent')
    else:
        form = ProfileForm(instance=profile)

    orders = Order.objects.filter(customer=user).select_related('box__warehouse')

    return render(request, 'my-rent.html', {
        'user': user,
        'profile': form,
        'orders': orders,
        })


def qr_code(request):
    order = request.order
    return render(request, 'qr_code.html', {'qr_code': order.qr_code.url})


def create_order(request):
    email = request.POST.get('email')
    user = User.objects.get(email=email)
    phone = request.POST.get('phone')
    selected_box = request.POST.get('selected_box')
    box = Box.objects.filter(name=selected_box).first()
    address = request.POST.get('address') if request.POST.get('address') else ''
    items = request.POST.get('items') if request.POST.get('items') else ''

    rental_period = int(request.POST.get('rental_period', 1))
    date_end = now().date() + relativedelta(months=rental_period)

    Order.objects.create(
        customer=user,
        box=box,
        address=address,
        items=items,
        date_end=date_end,
        phone=phone
    )
    box.is_busy = True
    box.save

    return redirect('index')


@login_required
def extend_order(request, order_id):
    if request.method == 'POST':
        months = int(request.POST.get('extension'))
        order = get_object_or_404(Order, id=order_id, customer=request.user)
        order.date_end += relativedelta(months=months)
        order.save()

        messages.success(request, f"Аренда продлена на {months} мес.")
        return redirect('my-rent')
