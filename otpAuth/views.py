import random
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model

ACCOUNT_SID = "ACf704c92aadad13c090e0de80beceb735"
AUTH_TOKEN = "5aebbe12ac22b77f331218e9c12c7541"
MY_TWILIO = "+12705132260"

User = get_user_model()

class OtpAuthView(TemplateView):
    template_url = "otpAuthentication.html"

    def clear_session_otp(self, request):
        if request.session.has_key('generated_otp'):
            del request.session["generated_otp"]

    def get(self, request, *args, **kwargs):
        self.clear_session_otp(request)
        return render(request, self.template_url)

    def post(self, request):
        user = User.objects.get(username=request.session['loggedin_username'])

        if 'Otp' not in request.POST:
            request.session['generated_otp'] = random.randint(100000, 999999)
            phone_number = '+91' + request.POST['Phone_number']
            client = Client(ACCOUNT_SID, AUTH_TOKEN)
            msg = f"{str(request.session['generated_otp'])} is your authentication otp."

            try:
                client.messages.create(to=phone_number, from_=MY_TWILIO, body=msg)
                return render(request, self.template_url, { "phone_number": request.POST['Phone_number'], })

            except TwilioRestException as ex:
                error = ""
                if ex.code == 21211:
                    error = f"The phone number {phone_number} is invalid"
                elif ex.code == 21608:
                    error = f"The phone number {phone_number} is not verified through twilio."
                else:
                    error = "Something went wrong."

                if request.session.has_key('generated_otp'):
                    self.clear_session_otp(request)

                return render(request, self.template_url, {"error": error})

        if int(request.POST['Otp']) == int(request.session['generated_otp']):
            request.session['phoneNumber'] = request.POST['Phone_number']
            return redirect("PatientHistory" if user.is_doctor else "DiagnosticDepartmentUpload")

        args = {
            "phone_number": request.POST['Phone_number'],
            "error": "Incorrect otp"
        }
        return render(request, self.template_url, args)
