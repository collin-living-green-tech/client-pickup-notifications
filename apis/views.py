from django.shortcuts import render

# Create your views here.

# a function view to render the
# comingsoon.html page

def index(request):
    return render(request,"apis/comingsoon.html")

