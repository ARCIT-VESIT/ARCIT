import random
from twilio.rest import Client
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from otpAuth.forms import OtpAuthForm

account_sid = "ACf704c92aadad13c090e0de80beceb735"
auth_token = "8b08254be48aa7721058af8a9a486f9e"
my_twilio = "+12705132260"

class OtpAuthView(TemplateView):
    template_name = "otpAuthIndex.html"
    
    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        # if request.POST['Phone_number'] is None == False:
        
        otp = random.randint(100000, 999999)
        phoneNumber = '+91' + request.POST['Phone_number']
        client = Client(account_sid, auth_token)
        msg = "Authentication otp is: " + str(otp)
        message = client.messages.create(to=phoneNumber, from_=my_twilio, body=msg)
        
        return render(request, "enterOtp.html", { 'phno': request.POST['Phone_number'], 'storedOtp' : otp })

class VerifyOtpView(TemplateView):
    template_name = "enterOtp.html"    

    def get(self, request):
        return render(request, self.template_name, { 'dirty_status': False })

    def post(self, request):
        otp = request.POST['OTP']
        storedOtp = request.POST['storedOTP']
        status = False
        if otp == storedOtp:
            status = True

        args = { 
            'phno': request.POST['Phone_number'], 
            'otp': otp, 
            'status': status,
            'dirty_status': True
        }

        return render(request, self.template_name, args)