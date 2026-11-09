from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("""
        <h1>Government Grievance Intelligence & Prioritization System</h1>
        <p>Django backend server is running successfully!</p>
        <ul>
            <li><a href="/admin/">Go to Django Admin Panel</a></li>
        </ul>
    """)