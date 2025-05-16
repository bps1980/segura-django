from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings

@csrf_exempt
def quick_dev_service(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        subject = f"New $99 Dev Request from {name}"
        body = f"""
        Name: {name}
        Email: {email}
        Message: {message}
        """

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            ['brennen@seguramgmt.com'],
            fail_silently=False
        )

        return render(request, "services/quick_dev_service.html", {
            "success": True
        })

    return render(request, "services/quick_dev_service.html")