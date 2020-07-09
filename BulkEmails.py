# -*- coding: UTF-8 -*-

from json import load
from csv import DictReader
from datetime import datetime
from os import path, remove
import codecs
from time import sleep

from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class BulkEmails():

    def __init__(self):
        #####
        print("-- Start session --")
        self.log = []
        self.email_error = []

        if (path.exists("config.json")):
            print("Openning config.json file ... [\u2713]")
            self.config = {}
            with open("config.json") as json_file:
                self.config = load(json_file)

        else:
            print("Openning config.json file ... [\u2717]")
            exit(1)

    def server_connect(self):
        #####
        print("Opening connection to the SMTP server ... ", end="", flush=True)

        try:
            self.smtp_server = SMTP(self.config["server"], int(self.config["port"]))
            self.smtp_server.starttls()
            self.smtp_server.login(
                self.config["username"], self.config["password"])
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.log.append(
                "[ {} ] [ Info ] Successfully connecting to the server ({}:{})".format(
                    current_time, self.config["server"], str(self.config["port"])))
            print("[\u2713]")

        except Exception as error:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.log.append("[ {} ] [ Error ] A problem occured while connecting to the server ({}:{})".format(
                current_time, self.config["server"], str(self.config["port"])))
            self.log.append("[ {} ] [ Error ] {}".format(
                current_time, str(error)))
            print("[\u2717] (a problem occured! see the logs)")

    def server_disconnect(self):
        print("Disconnection from the SMTP server ... ", end="", flush=True)

        try:
            self.smtp_server.quit()
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.log.append(
                "[ {} ] [ Info ] Successfully disconnecting from the server ({}:{})".format(
                    current_time, self.config["server"], str(self.config["port"])))
            print("[\u2713]")

        except Exception as error:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.log.append("[ {} ] [ Error ] A problem occured while disconnecting from the server ({}:{})".format(
                current_time, self.config["server"], str(self.config["port"])))
            self.log.append("[ {} ] [ Error ] {}".format(
                current_time, str(error)))
            print("[\u2717] (a problem occured! see the logs)")

    def send_test(self, email_address):
        #####
        self.server_connect()

        print("Sending a test email to {} ... ".format(
            email_address), end="", flush=True)

        email = MIMEMultipart()
        email["From"] = self.config["from"]
        email["To"] = email_address
        email["Subject"] = "[ Bulk Emails App ] Test Message :)"

        email.attach(
            MIMEText("Hi, this is just a simple test email !", "plain", "utf-8"))
        email_text = email.as_string()

        try:
            self.smtp_server.sendmail(
                self.config["from"], email["To"], email_text)
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.log.append(
                "[ {} ] [ Info ] Successfully sending test email to {}".format(current_time, email_address))
            print("[\u2713]")

        except Exception as error:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.log.append(
                "[ {} ] [ Error ] A problem occured while sending test email to {}".format(current_time, email_address))
            self.log.append("[ {} ] [ Error ] {}".format(
                current_time, str(error)))
            print("[\u2717] (a problem occured! see the logs)")

        self.server_disconnect()

    def bulk_emails(self, mail_template, mail_data, subject):
        #####
        self.server_connect()

        for idx in range(len(mail_data["email"])):
            print("Sending email to {} ... ".format(
                mail_data["email"][idx]), end="", flush=True)

            email = MIMEMultipart()
            email["From"] = self.config["from"]
            email["To"] = mail_data["email"][idx]
            email["Subject"] = subject

            mail_body = mail_template
            for key in list(mail_data.keys()):
                mail_body = mail_body.replace(
                    "%{}%".format(key), mail_data[key][idx])

            email.attach(MIMEText(mail_body, "plain", "utf-8"))
            email_text = email.as_string()

            try:
                self.smtp_server.sendmail(
                    self.config["from"], email["To"], email_text)
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.log.append("[ {} ] [ Info ] Successfully sending email to {}".format(
                    current_time, mail_data["email"][idx]))
                print("[\u2713]")

            except Exception as error:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.log.append("[ {} ] [ Error ] A problem occured while sending email to {}".format(
                    current_time, mail_data["email"][idx]))
                self.log.append("[ {} ] [ Error ] {}".format(
                    current_time, str(error)))
                self.email_error.append(mail_data["email"][idx])
                print("[\u2717] (a problem occured! see the logs)")

        self.server_disconnect()

    def send_emails(self, text_path, data_path, subject, limit=None):
        #####
        if (path.exists(data_path)):
            print("Openning data file : {} ... [\u2713]".format(data_path))

            mail_data = {}
            with open(data_path, mode="r", encoding="utf-8") as csv_file:
                reader = DictReader(csv_file)

                for row in reader:
                    for column, value in row.items():
                        mail_data.setdefault(column, []).append(value)

        else:
            print("Openning data file : {} ... [\u2717]".format(data_path))
            exit(1)

        if (path.exists(text_path)):
            print(
                "Openning mail template file : {} ... [\u2713]".format(text_path))

            with codecs.open(text_path, "r", encoding="utf8") as text_file:
                mail_template = text_file.read()

        else:
            print(
                "Openning mail template file : {} ... [\u2717]".format(text_path))
            exit(1)

        if(limit):
            time_wait = 60

            for idx in range(0, len(list(mail_data.values())[0]), limit):
                sub_mail_data = {}

                if((idx+(limit-1)) < len(list(mail_data.values())[0])):
                    for key in list(mail_data.keys()):
                        sub_mail_data.update(
                            {key: mail_data[key][idx:idx+limit]})

                else:
                    for key in list(mail_data.keys()):
                        sub_mail_data.update({key: mail_data[key][idx:]})

                self.bulk_emails(mail_template, sub_mail_data, subject)

                if((idx + limit) < len(list(mail_data.values())[0])):
                    print("Waiting {} seconds before sending ... ".format(
                        time_wait), end="", flush=True)
                    sleep(time_wait)
                    print("[\u2713]")

        else:
            self.bulk_emails(mail_template, mail_data, subject)

    def write_logs(self):
        #####
        print("Saving the logs ... ", end="", flush=True)

        with open("logs.txt", "a+") as log_file:
            for line in self.log:
                log_file.write("{}\n".format(line))

            if(len(self.email_error) > 0):
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_file.write("[ {} ] [ Error ] A problem occured while sending email to: {}".format(
                    current_time, ", ".join(self.email_error)))

            log_file.close()

        print("[\u2713]")

    def __del__(self):
        #####
        print("-- End session --")
