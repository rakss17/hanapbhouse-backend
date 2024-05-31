from djoser import email

class ActivationEmail(email.ActivationEmail):
    template_name = 'email_activation/email_activation.html'