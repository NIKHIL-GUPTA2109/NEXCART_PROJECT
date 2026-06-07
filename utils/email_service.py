from sib_api_v3_sdk import (
    Configuration,
    ApiClient,
    TransactionalEmailsApi,
    SendSmtpEmail
)
from django.conf import settings
from django.template.loader import render_to_string

def send_welcome_email(to_email, username):

    configuration = Configuration()
    configuration.api_key['api-key'] = settings.BREVO_API_KEY

    api_instance = TransactionalEmailsApi(
        ApiClient(configuration)
    )

    email = SendSmtpEmail(
        sender={
            "name": "NexCart",
            "email": "nikhilgupta002109@gmail.com"
        },
        to=[
            {
                "email": to_email,
                "name": username
            }
        ],
        subject="🎉 Welcome to NexCart – Your Shopping Journey Starts Here!",
        html_content=f"""
        <html>
        <body style="font-family: Arial, sans-serif;">

            <h1 style="color:#2563eb;">
                Welcome to NexCart 🚀
            </h1>

            <p>Hello <strong>{username}</strong>,</p>

            <p>
                Thank you for creating your NexCart account.
                We're excited to have you with us.
            </p>

            <p>
                Discover premium products, great deals,
                and a seamless shopping experience.
            </p>

            <p>
                Happy Shopping! 🛒
            </p>

            <br>

            <p>
                Regards,<br>
                Team NexCart
            </p>

        </body>
        </html>
        """
    )

    api_instance.send_transac_email(email)

def send_order_confirmation_email(user, order):

    configuration = Configuration()
    configuration.api_key['api-key'] = settings.BREVO_API_KEY

    api_instance = TransactionalEmailsApi(
        ApiClient(configuration)
    )

    html_content = render_to_string(
        'orders/emails/order_email.html',
        {
            'username': user.username,
            'order': order
        }
    )

    email = SendSmtpEmail(
        sender={
            "name": "NexCart",
            "email": "nikhilgupta002109@gmail.com"
        },

        to=[
            {
                "email": user.email,
                "name": user.username
            }
        ],

        subject=f"🎉 Order Confirmed #{order.id} | NexCart",

        html_content=html_content
    )

    try:

        response = api_instance.send_transac_email(
            email
        )

        print(
            f"ORDER EMAIL SENT SUCCESSFULLY: {response}"
        )

    except Exception as e:

        print(
            f"ORDER EMAIL ERROR: {e}"
        )

        raise


def send_password_reset_email(
    user,
    reset_link
):

    configuration = Configuration()
    configuration.api_key['api-key'] = settings.BREVO_API_KEY

    api_instance = TransactionalEmailsApi(
        ApiClient(configuration)
    )

    html_content = f"""
    <html>
    <body>

        <h2>Hello {user.username} 👋</h2>

        <p>
            We received a request to reset your NexCart password.
        </p>

        <p>
            Click the button below:
        </p>

        <p>
            <a
                href="{reset_link}"
                style="
                background:#2563eb;
                color:white;
                padding:12px 20px;
                text-decoration:none;
                border-radius:8px;"
            >
                Reset Password
            </a>
        </p>

        <p>
            If you didn't request this,
            simply ignore this email.
        </p>

        <br>

        <p>
            Team NexCart 🚀
        </p>

    </body>
    </html>
    """

    email = SendSmtpEmail(

        sender={
            "name": "NexCart",
            "email": "nikhilgupta002109@gmail.com"
        },

        to=[
            {
                "email": user.email,
                "name": user.username
            }
        ],

        subject="🔐 Reset Your NexCart Password",

        html_content=html_content
    )

    api_instance.send_transac_email(email)