from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import connection
from django.contrib.auth import logout
from django.db import connection
from .models import Note
import hashlib  # Weak cryptography for demonstration

# Add this new home view at the top
def home(request):
    if request.user.is_authenticated:
        notes = Note.objects.filter(user=request.user)
    else:
        notes = Note.objects.filter(is_private=False)
    return render(request, 'home.html', {'notes': notes})

def user_logout(request):
    logout(request)
    return redirect('home')



# FLAW 1: Broken Access Control
# No authentication check, anyone can access any note
def view_note(request, note_id):
    note = Note.objects.get(id=note_id) 
    return render(request, 'view_note.html', {'note': note})

# FLAW 2: Cryptographic Failure
# Using weak MD5 hashing for passwords
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # VULNERABLE: Using MD5 for password hashing
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        user = User.objects.create(username=username)
        user.password = hashed_password  # Directly setting password hash
        user.save()
        return redirect('login')
    return render(request, 'register.html')

# FLAW 3: SQL Injection
# Using raw SQL query with string concatenation

def search_notes(request):
    search_term = request.GET.get('q', '')
    # VULNERABLE: Direct string concatenation in SQL
    with connection.cursor() as cursor:
        # Updated the table name from blogapp_note to notes_note
        cursor.execute(f"SELECT * FROM notes_note WHERE content LIKE '%{search_term}%'")
        notes = cursor.fetchall()
    return render(request, 'search_results.html', {'notes': notes})

# FLAW 4: Insecure Design
# No rate limiting on login attempts
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        user = User.objects.get(username=username, password=hashed_password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

# FLAW 5: Security Misconfiguration
# Exposing detailed error messages and debug info
def create_note(request):
    try:
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            note = Note.objects.create(
                user=request.user,
                title=title,
                content=content
            )
            return redirect('view_note', note_id=note.id)  # Redirect to the created note's page
        else:
            # Handle GET request by rendering the note creation form
            return render(request, 'create_note.html')  # Ensure this template exists
    except Exception as e:
        # Render error details (intentionally insecure for demonstration purposes)
        return render(request, 'error.html', {'error_details': str(e)})