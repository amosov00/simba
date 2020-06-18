import smtplib

from config import EMAIL_LOGIN, EMAIL_PASSWORD, EMAIL_PORT, EMAIL_SERVER, HOST_URL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.parse import urlencode


class Email:
    def __init__(self):
        self.login = EMAIL_LOGIN
        self.password = EMAIL_PASSWORD
        self.port = EMAIL_PORT
        self.server = EMAIL_SERVER

    @staticmethod
    def _get_link(code: str, email: str, method: str) -> str:
        if method == "verification":
            params = {f"{method}_code": code, "email": email}
            return f'{HOST_URL}activate?{urlencode(params)}'
        if method == "recover":
            params = {f"{method}_code": code, "id": email}
            return f'{HOST_URL}recover?{urlencode(params)}'

    async def send_verification_code(self, to: str, code: str) -> None:
        mailserver = smtplib.SMTP_SSL(self.server, self.port)

        mailserver.login(self.login, self.password)
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['Subject'] = "Simba"
        msg['To'] = to
        body = "Добрый день! <br>\n" \
               "Перейдите по ссылке для регистрации в Simba: {}<br>\n" \
               "Надеемся вам понравится! До встречи!".format(Email._get_link(code, to, method='verification'))
        msg.attach(MIMEText(body, 'html'))
        text = msg.as_string()
        mailserver.sendmail(self.login, to, text)
        mailserver.quit()

    # TODO: Do smth with code repetion
    async def send_recover_code(self, to: str, code: str, user_id: str) -> None:
        mailserver = smtplib.SMTP_SSL(self.server, self.port)

        mailserver.login(self.login, self.password)
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['Subject'] = "Simba"
        msg['To'] = to
        body = "Добрый день! <br>\n" \
               "Перейдите по ссылке для восстановления пароля в Simba: {}<br>\n" \
               "До встречи!".format(Email._get_link(code, user_id, method="recover"))
        msg.attach(MIMEText(body, 'html'))
        text = msg.as_string()
        mailserver.sendmail(self.login, to, text)
        mailserver.quit()
