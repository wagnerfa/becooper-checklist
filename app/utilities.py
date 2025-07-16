from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


def send_email(destinatario, corpo):
    smtp_host = 'smtp.office365.com'
    smtp_port = 587
    usuario = 'noreply@becooper.coop.br'
    senha = 'Cooper@100'

    assunto = 'Teste'

    mensagem = MIMEMultipart()
    mensagem['From'] = usuario
    mensagem['To'] = destinatario
    mensagem['Subject'] = assunto

    mensagem.attach(MIMEText(corpo, 'plain'))

    with smtplib.SMTP(smtp_host, smtp_port) as servidor_smtp:
        servidor_smtp.set_debuglevel(1)
        servidor_smtp.starttls()
        servidor_smtp.login(usuario, senha)
        servidor_smtp.send_message(mensagem)
