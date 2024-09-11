from django.shortcuts import render


def dashboard(request):
        context = {}
        return render(request, 'home/dashboard.html', context)