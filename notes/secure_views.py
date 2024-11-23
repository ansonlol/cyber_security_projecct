from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.core.cache import cache
from django.http import HttpResponseForbidden
from .models import Note
import logging

logger = logging.getLogger(__name__)

# FIX 1: Proper Access Control
@login_required
def view_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if note.user != request.user and note.is_private:
        return HttpResponseForbidden("You don't have permission to view this note")
    return render(request, 'view_note.html', {'note': note})

# FIX 2: Proper Password Hashing
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Using Django's built-in password hashing
        user = User.objects.create_user(
            username=username,
            password=password  # Django handles secure hashing automatically
        )
        return redirect('login')
    return render(request, 'register.html')

# FIX 3: Prevention of SQL Injection
def search_notes(request):
    search_term = request.GET.get('q', '')
    # Using Django's ORM for safe queries
    notes = Note.objects.filter(
        Q(content__icontains=search_term) & 
        (Q(user=request.user) | Q(is_private=False))
    )
    return render(request, 'search_results.html', {'notes': notes})

# FIX 4: Secure Design with Rate Limiting
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        
        # Implement rate limiting
        attempts_key = f"login_attempts_{username}"
        attempts = cache.get(attempts_key, 0)
        
        if attempts >= 5:  # Limit to 5 attempts
            return render(request, 'login.html', 
                {'error': 'Too many login attempts. Please try again later.'})
        
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            cache.delete(attempts_key)
            return redirect('home')
        else:
            cache.set(attempts_key, attempts + 1, 300)  # 5 minutes timeout
            
    return render(request, 'login.html')

# FIX 5: Proper Error Handling and Configuration
@login_required
def create_note(request):
    try:
        if request.method == 'POST':
            title = request.POST['title']
            content = request.POST['content']
            note = Note.objects.create(
                user=request.user,
                title=title,
                content=content
            )
            return redirect('view_note', note_id=note.id)
    except Exception as e:
        # Log the actual error for debugging
        logger.error(f"Error creating note: {str(e)}")
        # Show generic error message to user
        return render(request, 'error.html', 
            {'error_message': 'An error occurred while creating the note.'})