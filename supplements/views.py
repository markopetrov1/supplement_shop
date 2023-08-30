from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from supplements.models import Supplement, ShoppingCart
from django.db.models import Q, Sum


# Create your views here.


def supplement_details(request, supplement_id):
    supplement = Supplement.objects.filter(pk=supplement_id).first()

    return render(request, "supplement-detail.html", context={"supplement": supplement})


def shopping_cart(request):
    message = None
    if not request.user.is_authenticated:
        return redirect("login")

    if request.POST:
        ShoppingCart.objects.create(
            user=request.user,
            supplement_id=request.POST.get("supplement"),
            quantity=request.POST.get("quantity")
        )

        message = 'Продуктот е успешно додаден во кошничката!'

    products = ShoppingCart.objects.filter(user=request.user.pk).all()

    total_price = products.aggregate(total=Sum('supplement__price'))['total']

    if not total_price:
        total_price = 0

    context = {
        "products": products,
        "total_price": total_price,
        "message": message
    }

    return render(request, "shopping-cart.html", context=context)


def home(request):
    supplements = Supplement.objects.all()

    if request.method == "POST":
        search = request.POST.get("search")
        category = request.POST.get("category")
        if search:
            supplements = Supplement.objects.filter(Q(name__icontains=search) | Q(category__icontains=search)).all()

        if category and category != 'all':
            supplements = Supplement.objects.filter(category=category).all()

    return render(request, "home.html", context={'supplements': supplements})


def register_request(request):
    error_message = None
    message = None

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm-password")

        if password != confirm_password:
            error_message = 'Лозинките не се исти.'
        elif User.objects.filter(email=email).exists():
            error_message = 'Е-маил адресата е веќе зафатена.'
        else:
            user = User.objects.create_user(
                username=email, email=email, password=password,
                first_name=first_name, last_name=last_name
            )
            user.save()

            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                message = "Корисникот е успешно регистриран!"
                messages.success(request, message)
                return redirect("login")

    return render(request, "register.html", context={'error_message': error_message})


def login_request(request):
    error_message = None
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Добредојде назад {request.user.first_name}!")
            return redirect("home")
        else:
            error_message = "Невалидна е-маил адреса или лозинка."

    return render(request, "login.html", context={"error_message": error_message})


def logout_request(request):
    logout(request)
    messages.success(request, "Корисникот е одјавен!")
    return redirect("login")


def confirm_payment(request):
    if request.user:
        ShoppingCart.objects.filter(user=request.user).delete()
    return render(request, "confirm-payment.html")


def payment_info(request):
    return render(request, "payment-info.html")


def add_supplement(request):
    CATEGORY_CHOICES = [
        ('proteins', 'Proteins'),
        ('creatines', 'Creatines'),
        ('vitamins', 'Vitamins'),
        ('amino-acids', 'Amino Acids'),
        ('pre-workout', 'Pre-Workout')
    ]

    if request.method == "POST":
        name = request.POST.get('name')
        brand = request.POST.get('brand')
        code = request.POST.get('code')
        availability = request.POST.get('availability')
        price = request.POST.get('price')
        category = request.POST.get('category')
        description = request.POST.get('description')

        supplement = Supplement(
            name=name,
            brand=brand,
            code=code,
            availability=bool(int(availability)),
            price=int(price),
            category=category,
            description=description,
            photo=request.FILES.get('photo')
        )
        supplement.save()

        return redirect('home')

    return render(request, "add-supplement.html", {'category_choices': CATEGORY_CHOICES})

def edit_supplement(request, supplement_id):
    supplement = Supplement.objects.filter(pk=supplement_id).first()

    if request.method == "POST":
        brand = request.POST.get("brand")
        code = request.POST.get("code")
        availability = request.POST.get("availability")
        price = request.POST.get("price")
        description = request.POST.get("description")

        supplement.brand = brand
        supplement.code = code
        print('availability '+str(availability))
        supplement.price = price
        supplement.description = description

        supplement.save()

        return redirect(f"/supplements/{supplement_id}/")

    return render(request, "edit-supplement.html", context={"supplement": supplement})
