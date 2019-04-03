import os
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

from django.utils.html import strip_tags


class Email:

    client = os.getenv('CLIENT_DOMAIN')

    def get_activate_account_link(self, token, uid):
        """
        :rtype: object
        """
        return "{}/{}?token={}&uid={}".format(
            Email.client, os.getenv("CLIENT_ACTIVATE_ACCOUNT_ROUTE"), token,
            uid)

    def send_account_activation_email(self,
                                      user,
                                      request=None,
                                      send_email=True):
        """
        :param user:
        :param request:
        :param send_email: Testing will pass this as false in order to prevent actually sending an email to mock users
        :return:
        """

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.username)).decode("utf-8")

        if send_email:
            email = user.email
            username = user.username
            from_email = os.getenv("EMAIL_HOST_SENDER")

            email_subject = 'Activate your Seven Eleven account.'
            email_message = render_to_string(
                'email_verification.html', {
                    'activation_link':
                    Email().get_activate_account_link(token, uid),
                    'title':
                    email_subject,
                    'username':
                    username
                })
            text_content = strip_tags(email_message)
            msg = EmailMultiAlternatives(
                email_subject, text_content, from_email, to=[email])
            msg.attach_alternative(email_message, "text/html")
            msg.send()

        return token, uid