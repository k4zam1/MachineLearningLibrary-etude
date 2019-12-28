import httplib2
import os

import apiclient
import oauth2client
from oauth2client import file
from oauth2client import tools

import base64
from email.mime.text import MIMEText
from email.utils import formatdate
import traceback

class Sender:
	def __init__(self,mail_from,mail_to,application_name="GmailSender",client_secret_path="client_secret.json"):
		self.SCOPES ="https://www.googleapis.com/auth/gmail.send"
		self.CLIENT_SECRET_FILE = client_secret_path
		self.APPLICATION_NAME = application_name
		self.MAIL_FROM = mail_from
		self.MAIL_TO = mail_to
		self.credentials = None

		script_dir =os.path.abspath(os.path.dirname(__file__)) 
		credential_dir = os.path.join(script_dir, ".credentials")

		if not os.path.exists(credential_dir):
			os.makedirs(credential_dir)
		credential_path = os.path.join(credential_dir,
									"my-gmail-sender.json")

		store = file.Storage(credential_path)
		credentials = store.get()
		if not credentials or credentials.invalid:
			flow = oauth2client.client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE,self.SCOPES)
			flow.user_agent = self.APPLICATION_NAME
			credentials = tools.run_flow(flow, store)
			print("Storing credentials to " + credential_path)
		self.credentials = credentials
		self.http = self.credentials.authorize(httplib2.Http())
		self.service = apiclient.discovery.build("gmail", "v1", http=self.http)

	def __create_message(self,text,subject):
		message = MIMEText(text)
		message["from"] = self.MAIL_FROM
		message["to"] = self.MAIL_TO
		message["subject"] = subject
		message["Date"] = formatdate(localtime=True)

		byte_msg = message.as_string().encode(encoding="UTF-8")
		byte_msg_b64encoded = base64.urlsafe_b64encode(byte_msg)
		str_msg_b64encoded = byte_msg_b64encoded.decode(encoding="UTF-8")

		return {"raw": str_msg_b64encoded}
	
	def send_message(self,text,subject):
		try:
			result = self.service.users().messages().send(
				userId=self.MAIL_FROM,
				body=self.__create_message(text,subject)
			).execute()
			print("Message Id: {}".format(result["id"]))

		except apiclient.errors.HttpError:
			print("------start trace------")
			traceback.print_exc()
			print("------end trace------")


def main():
	me = "taa57500@gmail.com"
	gmail = Sender(mail_from=me,mail_to=me)
	gmail.send_message("hello","test message")


if __name__ == "__main__":
    main()