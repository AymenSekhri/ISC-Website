from django.shortcuts import render
import bcrypt
# Create your views here.




def Home(request):
    
    return render(request,"MainApp/index.html")