from django.shortcuts import render

# home
def home_view(request):
    return render(request, 'third_task/home.html')

# shop
def shop_view(request):
    items = {
        "Игровая приставка": "Современная консоль нового поколения.",
        "Игровая мышь": "Высокоточная мышь для киберспорта.",
        "Монитор": "Монитор с высоким разрешением и частотой обновления.",
    }
    return render(request, 'third_task/shop.html', {'items': items})

# cart
def cart_view(request):
    return render(request, 'third_task/cart.html')
