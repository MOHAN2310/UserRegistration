import os
from dotenv import load_dotenv
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from pathlib import Path

load_dotenv('dev.env')

mail_config = ConnectionConfig(
    MAIL_USERNAME= str(os.getenv('MAIL_USERNAME')),
    MAIL_PASSWORD=str(os.getenv('MAIL_PASSWORD')),
    MAIL_SERVER=str(os.getenv('MAIL_SERVER')),
    MAIL_PORT=587,
    MAIL_FROM="mohanraj.balajiv@gmail.com",
    MAIL_FROM_NAME="MohanrajB",
      MAIL_STARTTLS=True,
      MAIL_SSL_TLS=False,
)


mail = FastMail(config=mail_config)


def create_message(recipients: list[str], subject: str, body: str):
    message = MessageSchema(
        recipients=recipients, subject=subject, body=body, subtype=MessageType.html
    )
    return message