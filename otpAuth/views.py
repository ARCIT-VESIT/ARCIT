import random
from twilio.rest import Client
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model

from otpAuth.forms import OtpAuthForm
from Patient.models import Patients

account_sid = "ACf704c92aadad13c090e0de80beceb735"
auth_token = "4780b31c2485030454daf4f67504a569"
my_twilio = "+12705132260"

User = get_user_model()

class OtpAuthView(TemplateView):
    doctor_template_name = "otpAuthIndex.html"
    dd_template_name = "DiagnosticDepartment/otpAuthIndex.html"
    success_doctor_template_name = "enterOtp.html"
    success_dd_template_name = "DiagnosticDepartment/enterOtp.html"
    
    def get(self, request):
        user = User.objects.get(username=request.session['loggedin_username'])
        if user.is_doctor:
            print('ran doct')
            return render(request, self.doctor_template_name)
        elif user.is_diagnosticDepartment:
            print('ran dd')
            return render(request, self.dd_template_name)
        else:
            return render(request, self.doctor_template_name)

    def post(self, request):
        # if request.POST['Phone_number'] is None == False:
        
        otp = random.randint(100000, 999999)
        phoneNumber = '+91' + request.POST['Phone_number']
        client = Client(account_sid, auth_token)
        msg = "Authentication otp is: " + str(otp)
        client.messages.create(to=phoneNumber, from_=my_twilio, body=msg)

        user = User.objects.get(username=request.session['loggedin_username'])

        if user.is_doctor:
            print('ran doct')
            return render(request, self.success_doctor_template_name, { 'phno': request.POST['Phone_number'], 'storedOtp' : otp })
        elif user.is_diagnosticDepartment:
            print('ran dd')
            return render(request, self.success_dd_template_name, { 'phno': request.POST['Phone_number'], 'storedOtp' : otp})

class VerifyOtpView(TemplateView):
    doctor_template_name = "enterOtp.html"
    dd_template_name = "DiagnosticDepartment/enterOtp.html"

    def get(self, request):
        user = User.objects.get(username=request.session['loggedin_username'])
        if user.is_doctor:
            print('ran doct')
            return render(request, self.doctor_template_name, { 'dirty_status': False })
        elif user.is_diagnosticDepartment:
            print('ran dd')
            return render(request, self.dd_template_name, { 'dirty_status': False })
        else:
            return render(request, self.doctor_template_name, { 'dirty_status': False })

    def post(self, request):
        otp = request.POST['OTP']
        storedOtp = request.POST['storedOTP']
        status = False
        phoneNumber = request.POST['Phone_number']  

        if otp == storedOtp:
            status = True

        args = { 
            'phno': phoneNumber, 
            'otp': otp, 
            'status': status,
            'dirty_status': True
        }

        user = User.objects.get(username=request.session['loggedin_username'])

        if status == True:
            request.session['phoneNumber'] = phoneNumber
            if user.is_doctor:
                return redirect("PatientHistory")
            elif user.is_diagnosticDepartment:
                return redirect("DiagnosticDepartmentUpload")
               
        else:
            return render(request, self.doctor_template_name, args)