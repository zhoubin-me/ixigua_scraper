import glob, os
from youtube_upload.client import YoutubeUploader

UPLOAD_LIST = 'vupdate2.txt'
UPLOAD_FOLDER = 'Colorful_Update'

def main():
    uploader = YoutubeUploader(secrets_file_path="D:\\secret.json")
    uploader.authenticate()

    with open(UPLOAD_LIST, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        title = line.split('\t')[0].strip()
        path = os.path.join("D:", UPLOAD_FOLDER, title + '.mp4')
        if os.path.exists(path):
            print(f"Uploading: {title}")
            options = {
                "title" : title, # The video title
                "description" : "", # The video description
                "tags" : ["Warcraft III: Reforged"],
                "categoryId" : "20",
                "language": 'zh-CN',
                "audio_language": 'zh-CN',
                "privacyStatus" : "public", # Video privacy. Can either be "public", "private", or "unlisted"
                "kids" : False # Specifies if the Video if for kids or not. Defaults to False.
            }
            uploader.upload(path, options) 
            print(f"Uploaded: {title}")


def show():
    fs = glob.glob('D:\\Colorful\\*.mp4')
    for f in fs[:20]:
        title = os.path.basename(f).split('.')[0]
        print(f"Uploading: {title}")


if __name__ == '__main__':
    main()