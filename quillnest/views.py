from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from blogs.models import Contact


# Create your views here.
def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == "POST":
        first_name = request.POST["fname"]
        last_name = request.POST["lname"]
        email = request.POST["email"]
        message = request.POST["message"]

        contact_obj = Contact.objects.create(first_name=first_name, last_name=last_name, email=email, message=message)
        messages.success(request, "Your mail send successfully...!")

        # Send thank you mail for contact us
        subject = "Thank you for contact us"
        message_email = f"Hello {first_name} {last_name},\nThank you for conact us.\nWe will replay your mail as soon as possible.\n\nThank you\nadmin"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        send_mail(subject, message_email, from_email, recipient_list, fail_silently=True)
    return render(request, 'contact.html')