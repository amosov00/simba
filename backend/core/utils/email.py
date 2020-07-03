import smtplib
from http import HTTPStatus
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.parse import urlencode

from fastapi import HTTPException
from sentry_sdk import capture_exception

from config import EMAIL_LOGIN, EMAIL_PASSWORD, EMAIL_PORT, EMAIL_SERVER, HOST_URL


class Email:
    def __init__(self):
        self.email_from = EMAIL_LOGIN
        self.password = EMAIL_PASSWORD
        self.port = EMAIL_PORT
        self.server = EMAIL_SERVER
        self.mailserver = smtplib.SMTP_SSL(self.server, self.port)

    @staticmethod
    def _get_link(code: str, email: str, method: str) -> str:
        if method == "verification":
            params = {f"{method}_code": code, "email": email}
            return f'{HOST_URL}activate?{urlencode(params)}'
        if method == "recover":
            params = {f"{method}_code": code}
            return f'{HOST_URL}recover?{urlencode(params)}'

    def login(self) -> None:
        try:
            self.mailserver.login(self.email_from, self.password)
            return None
        except Exception as e:
            capture_exception(e)
            raise HTTPException(HTTPStatus.INTERNAL_SERVER_ERROR, "Error while sending email")

    def create_message(self, to: str, body: str) -> MIMEMultipart:
        msg = MIMEMultipart()
        msg['From'] = self.email_from
        msg['Subject'] = "Simba"
        msg['To'] = to
        msg.attach(MIMEText(body, 'html'))
        return msg

    def send_message(self, to: str, text: str):
        try:
            self.mailserver.sendmail(self.email_from, to, text)
            return None
        except Exception as e:
            capture_exception(e)
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Error while sending email")

    async def send_verification_code(self, to: str, code: str) -> None:
        self.login()
        msg = self.create_message(
            to,
            "Добрый день! <br>\n" \
            'Перейдите по <a href="{}">этой</a> ссылке для регистрации в Simba<br>\n' \
            "Надеемся вам понравится! До встречи!".format(Email._get_link(code, to, method='verification'))
        )
        self.send_message(to, msg.as_string())
        self.mailserver.quit()
        return None

    # TODO: Do smth with code repetion
    async def send_recover_code(self, to: str, code: str) -> None:
        self.login()
        msg = self.create_message(
            to,
            "Добрый день! <br>\n" \
            'Перейдите по <a href="{}">этой</a> ссылке для восстановления пароля в Simba<br>\n' \
            "До встречи!".format(Email._get_link(code, "", method="recover"))
        )
        self.send_message(to, msg.as_string())
        self.mailserver.quit()
        return None
