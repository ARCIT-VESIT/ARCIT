import random
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

from Hospital.forms import HospitalForm
from Doctor.forms import DoctorForm
from DiagnosticDepartment.forms import DiagnosticDepartmentSignupForm
from Patient.forms import UserRegisterationForm

from .forms import UserForm

ACCOUNT_SID = "ACf704c92aadad13c090e0de80beceb735"
AUTH_TOKEN = "7f6552ed5f938239789d59967198882e"
MY_TWILIO = "+12705132260"

User = get_user_model()

def log_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            request.session['loggedin_username'] = username

            user = authenticate(username=username, password=password)
            if user.is_doctor:
                request.session['role'] = 'Doctor'
                request.session['is_doctor'] = True
                return redirect('doctorprofile')
            if user.is_patient:
                request.session['role'] = 'Patient'
                request.session['is_patient'] = True
                return redirect('patientprofile')
            if user.is_hospital:
                request.session['role'] = 'Hospital'
                request.session['is_hospital'] = True
                return redirect('hospitalprofile')
            if user.is_diagnosticDepartment:
                request.session['role'] = 'DD'
                request.session['is_dd'] = True
                return redirect('ddprofile')
        else:
            return render(request, 'Authentication/login.html', {'form': form})
    else:
        form = AuthenticationForm(request)
    return render(request, 'Authentication/login.html', {'form': form})

class RegisterationView(TemplateView):
    '''Common registeration View'''
    template_name='Authentication/registeration.html'
    role = ""

    def identify_action_by_role(self, isHeading, post_request = None):
        role = self.role

        if role == 'D':
            return "Doctor registeration" if isHeading else DoctorForm(post_request)
        if role == 'H':
            return "Hospital registeration" if isHeading else HospitalForm(post_request)
        if role == 'R':
            return "Diagnostic center registeration" if isHeading else DiagnosticDepartmentSignupForm(post_request)    
        return "New patient" if isHeading else UserRegisterationForm(post_request)

    def get(self, request, *args, **kwargs):
        self.role = kwargs.pop('role')

        registeration_form = self.identify_action_by_role(False)
        user_form = UserForm()
        return render(request,'Authentication/registeration.html',{'form':registeration_form, 'form2': user_form, 'heading': self.identify_action_by_role(True)})

    def post(self,request, *args, **kwargs):
        '''request to handle registeration of hospital form'''
        role = self.role = kwargs.pop('role')

        form =  UserForm(request.POST)
        form2 = self.identify_action_by_role(False, request.POST)

        if form.is_valid() and form2.is_valid():

            user = User.objects.create_user(
                form.data['username'],
                form2.data['email'],
                form.data['password1'],
                first_name=form2.data['name'],
                is_doctor = role == 'D',
                is_hospital = role == 'H',
                is_diagnosticDepartment = role == 'R',
                is_patient = role == 'P',
            )

            form_data=form2.save(commit=False)
            if role == 'P':
                form_data.created_by = User.objects.get(username=request.session['loggedin_username'])
            form_data.user=user
            form_data.save()

            return redirect('otpAuth' if role == 'P' else 'login')

        form = self.identify_action_by_role(False, request.POST)
        form2 = UserForm(request.POST)

        args = {'form': form,'form2':form2, 'heading': self.identify_action_by_role(True)}

        return render(request,'Authentication/registeration.html', args)


class OtpAuthView(TemplateView):
    template_url = "Authentication/otp.html"

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
                elif ex.code == 20003:
                    error = "Token expired."
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
