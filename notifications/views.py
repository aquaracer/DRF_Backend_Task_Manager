import os

from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(
        request,
        'index.html',
        context={
            "FIREBASE_apiKey": os.getenv("FIREBASE_apiKey"),
            "FIREBASE_AUTH_DOMAIN": os.getenv("FIREBASE_AUTH_DOMAIN"),
            "FIREBASE_PROJECT_ID": os.getenv("FIREBASE_PROJECT_ID"),
            "FIREBASE_STORAGE_BUCKET": os.getenv("FIREBASE_STORAGE_BUCKET"),
            "FIREBASE_MESSAGING_SENDER_ID": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
            "FIREBASE_APP_ID": os.getenv("FIREBASE_APP_ID"),
            "FIREBASE_MEASUREMENT_ID": os.getenv("FIREBASE_MEASUREMENT_ID"),
        },
    )


def showFirebaseJS(request):
    data = f"""importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-app.js");
           importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-messaging.js");
           var firebaseConfig = {{
                   apiKey: "{os.getenv('FIREBASE_apiKey')}",
                   authDomain: "{os.getenv('FIREBASE_AUTH_DOMAIN')}",
                   projectId:  "{os.getenv('FIREBASE_PROJECT_ID')}",
                   storageBucket: "{os.getenv('FIREBASE_STORAGE_BUCKET')}",
                   messagingSenderId: "{os.getenv('FIREBASE_MESSAGING_SENDER_ID')}", 
                   appId: "{os.getenv('FIREBASE_APP_ID')}",
                   measurementId: "{os.getenv('FIREBASE_MEASUREMENT_ID')}"
            }};
           firebase.initializeApp(firebaseConfig);
           const messaging=firebase.messaging();
           messaging.setBackgroundMessageHandler(function (payload) {{
               console.log(payload);
               const notification=JSON.parse(payload);
               const notificationOption={{
               body:notification.body,
               icon:notification.icon
               }};
               return self.registration.showNotification(payload.notification.title,notificationOption);
           }});"""

    return HttpResponse(data, content_type="text/javascript")
