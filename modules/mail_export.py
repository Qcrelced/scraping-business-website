import smtplib
import os
from time import *
from datetime import datetime
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def mail_export(filename):
    # Paramètres de connexion
    email = "samueletsamy@gmail.com"
    password = "vski nvpi qgcn yrcl"
    chemin_fichier = os.path.join(os.getcwd(), filename)
    print(chemin_fichier)

    # Créer le message
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = "declercq1103@gmail.com"
    msg['Subject'] = "Sujet de l'e-mail"

    # Ajouter le corps de l'e-mail
    msg.attach(MIMEText('Corps de l\'e-mail', 'plain'))

    with open(chemin_fichier, 'rb') as file:
        # Ajouter le fichier Excel
        part = MIMEApplication(file.read(), _subtype="xlsx")
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % file)
        msg.attach(part)

    # Connexion au serveur SMTP et envoi
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(email, password)
    server.send_message(msg)
    server.quit()