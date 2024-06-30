from djoser import email

class ActivationEmail(email.ActivationEmail):
    template_name = 'email_activation/email_activation.html'

class PasswordResetEmail(email.PasswordResetEmail):
    template_name = 'password_reset_email/password_reset_email.html'