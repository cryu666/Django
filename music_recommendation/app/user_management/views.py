from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import csv
import os

def registerPage(request):
    csv_file_path = os.path.join(os.path.dirname(__file__), 'accounts.csv')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']  # Use password1 for the password field

            # Check if the username already exists in the CSV file
            with open(csv_file_path, 'r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    if row['username'] == username:
                        messages.error(request, '用户名已存在')
                        return render(request, 'register.html', {'form': form})
            
            # Write the new user's account information to the CSV file
            with open(csv_file_path, 'a', newline='') as file:
                csv_writer = csv.writer(file)
                l = [username, password]
                csv_writer.writerow(l)
            messages.success(request, '注册成功，请登录')
            return redirect('login')
    else:
        form = UserCreationForm()      

    return render(request, 'register.html', {'form': form})

def loginPage(request):
    csv_file_path = os.path.join(os.path.dirname(__file__), 'accounts.csv')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # 尝试验证用户
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                if row['username'] == username and row['password'] == password:
                    request.session['user_id'] = username
                    messages.success(request, '登录成功')
                    return redirect('home')
                
        messages.error(request, '无效的用户名或密码')
        return redirect('login')
    
    return render(request, 'login.html')

def logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']
        messages.success(request, '您已成功登出')
    return redirect('home')
