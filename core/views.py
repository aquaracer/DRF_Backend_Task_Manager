from django.shortcuts import render
import os


def google_login(request):
    """ Страница входа через Google"""

    return render(
        request, 'oauth/google_login.html', context={
            'GOOGLE_CLIENT_ID': os.getenv('GOOGLE_CLIENT_ID'),
            'HOST': os.getenv('HOST')
        }
    )

