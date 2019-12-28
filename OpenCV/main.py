from dropboxUploader import Uploader
from auth import DB_ACCESS_TOKEN
from camera import Camera
from gmail_sender import Sender
from yolo import detect_img

def get_timestamp():
	import datetime
	now = datetime.datetime.now()
	now = now.strftime('%Y年%m月%d日 %H:%M:%S')
	return now

def upload_detect_image(path):
	out_filename = get_timestamp()+".jpg"
	detect_img(img_path=path,out_filepath="camera_image/"+out_filename)
	dropbox = Uploader(DB_ACCESS_TOKEN)
	with open("camera_image/"+out_filename,"rb") as image_file :
		link = dropbox.upload(image_file.read(),"/webcam/"+out_filename,link=True)
	return link

def send_link(link):
	me = "hogehoeg@hoge.com"
	gmail = Sender(mail_from=me,mail_to=me)
	gmail.send_message("変化を検出しました： {}".format(link),"security web camera")

def main():
	camera = Camera()
	path = camera.get_alteranation_image_path()
	link = upload_detect_image(path)
	send_link(link)

if __name__ == "__main__":
	main()