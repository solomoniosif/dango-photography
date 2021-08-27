from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.views.generic.edit import CreateView, FormView

from .forms import CustomUserCreationForm


class UserLoginView(LoginView):
	template_name = 'registration/login.html'
	fields = '__all__'
	redirect_authenticated_user = True

	def get_success_url(self):
		return reverse_lazy('photos:home')


class SignUpView(CreateView):
	template_name = 'registration/signup.html'
	form_class = CustomUserCreationForm
	success_url = reverse_lazy('photos:home')

	def form_valid(self, form):
		user = form.save()
		if user is not None:
			login(self.request, user)
		return super(SignUpView, self).form_valid(form)
