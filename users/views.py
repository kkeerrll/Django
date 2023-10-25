import random

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, UserProfileForm, VarificationForm, RestorePasswordForm
from users.models import User


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def get_success_url(self):
        return reverse('users:verification', args=[self.object.pk])

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        code = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        new_user = form.save()
        new_user.code = code
        new_user.save()

        send_mail(
            subject='Код подтверждения',
            message=f'Ваш код подтверждения регистрации {code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )

        return super().form_valid(form)


@login_required
def pass_verification(request, pk):
    user = User.objects.get(pk=pk)
    code = user.code

    if request.method == 'POST':
        form = VarificationForm(request.POST)
        user_code = request.POST.get('code')

        if code == user_code:
            user.is_active = True
            user.save()
            return redirect(reverse('users:login'))

        else:
            return render(request, 'users/verification_form.html', {'form': form, 'pk': pk})

    else:
        form = VarificationForm()

    return render(request, 'users/verification_form.html', {'form': form, 'pk': pk})


@login_required
def restore_password(request):
    if request.method == 'POST':
        form = RestorePasswordForm(request.POST)
        user_email = request.POST.get('email')

        try:
            user = User.objects.get(email=user_email)

        except ObjectDoesNotExist:
            form.add_error('email', 'Такой пользователь не существует')
            return render(request, 'users/restore_password_form.html', {'form': form})

        else:
            password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
            user.set_password(password)
            user.save()

            send_mail(
                subject='Восстановление пароля',
                message=f'Ваш новый пароль {password}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email]
            )
            return redirect(reverse('users:login'))

    else:
        form = RestorePasswordForm()

    return render(request, 'users/restore_password_form.html', {'form': form})


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
