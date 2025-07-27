from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from dateutil.relativedelta import relativedelta
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.contrib.auth.models import User
from warehouse_app.models import Warehouse, Profile, Order, Box
from promo.models import Promo
from .forms import RegisterForm, LoginForm, ProfileForm, CallbackRequestForm


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

    if request.method == 'POST':
        callback_form = CallbackRequestForm(request.POST)
        if callback_form.is_valid():
            callback_form.save()
            messages.success(request, "Заявка отправлена! Мы свяжемся с вами в ближайшее время.")
            return redirect('index')
    else:
        callback_form = CallbackRequestForm()

    return render(request, 'index.html', {
        'login_form': login_form,
        'register_form': register_form,
        'callback_form': callback_form,
        'show_login_modal': show_login_modal,
        'show_reg_modal': show_reg_modal
    })


def faq(request):
    return render(request, 'faq.html')


def boxes(request):
    warehouses = Warehouse.objects.prefetch_related('boxes').all()
    show_login_modal = request.session.pop('show_login_modal_boxes', False)
    login_required_message = request.session.pop('login_required_message', None)
    error_messages = request.session.pop('error_messages', None)
    promo_codes = list(Promo.objects.values('code', 'discount'))
    return render(request, 'boxes.html', {
        'warehouses': warehouses,
        'show_login_modal_boxes': show_login_modal,
        'login_required_message': login_required_message,
        'error_messages': error_messages,
        'promo_codes': promo_codes
    })


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
    if request.method == 'POST':
        if not request.user.is_authenticated:
            request.session['login_required_message'] = "Это действие требует входа в аккаунт"
            request.session['show_login_modadsl_boxes'] = True
            return redirect('boxes')

        error_messages = []

        phone_validator = RegexValidator(regex=r'^(\+?7|8)\d{10}$')

        user = request.user
        try:
            phone = request.POST.get('phone')
            phone_validator(phone)
        except ValidationError:
            error_messages.append(
                'Неправильно введён номер телефона, допустимые' \
                ' форматы: +7XXXXXXXXXX, 7XXXXXXXXXX или 8XXXXXXXXXX'
            )

        selected_box = request.POST.get('selected_box')
        box = Box.objects.filter(name=selected_box).first()
        if not box:
            error_messages.append('Вы не выбрали бокс для аренды')
        if box and box.is_busy:
            error_messages.append('Выбранный бокс уже занят. ' \
                                  'Пожалуйста, выберите другой.')
        if error_messages:
            request.session['error_messages'] = error_messages
            return redirect('boxes')

        comment = request.POST.get('comment', '')
        address = request.POST.get('address', '')
        items = request.POST.get('items', '')

        promo_code_input = request.POST.get('promo_code', '').strip().upper()
        promocode = (
            Promo.objects.filter(code=promo_code_input).first()
            if promo_code_input
            else None
        )

        rental_period = int(request.POST.get('rental_period', 1))
        date_end = now().date() + relativedelta(months=rental_period)

        Order.objects.create(
            customer=user,
            box=box,
            address=address,
            items=items,
            date_end=date_end,
            phone=phone,
            comment=comment,
            promocode=promocode
        )
        box.is_busy = True
        box.save()

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
