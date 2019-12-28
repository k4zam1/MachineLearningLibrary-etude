import dropbox

class Uploader:
	def __init__(self,token):
		self.__DB_ACCESS_TOKEN = token
		self.__sharedLinkSetting = dropbox.sharing.SharedLinkSettings(requested_visibility=dropbox.sharing.RequestedVisibility.public)
		self.dbx = dropbox.Dropbox(self.__DB_ACCESS_TOKEN)

	def upload(self,file,path,link=False):
		self.dbx.files_upload(file,path)
		if link :
			link_data = self.dbx.sharing_create_shared_link_with_settings(path=path, settings=self.__sharedLinkSetting)
			return link_data.url