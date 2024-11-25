from django.shortcuts import render

# home
def home_view(request):
    return render(request, 'fourth_task/home.html')

# shop
def shop_view(request):
    context = {'games': ["Atomic Heart", "Cyberpunk 2077"]}
    return render(request, 'fourth_task/shop.html', context)

# cart
def cart_view(request):
    return render(request, 'fourth_task/cart.html')

