from datetime import datetime
import exifread
import flickr_api as flickr
import json
import os

settings = {}

def load_settings():
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    if 'api_key' in settings:
        flickr.set_keys(api_key=str(settings['api_key']), api_secret=str(settings['api_secret']))
    if 'token_key' in settings:
        handler = flickr.auth.AuthHandler.create(str(settings['token_key']), str(settings['token_secret']))
        flickr.set_auth_handler(handler)
    return settings

def guess_time(path):
    with open(path, 'rb') as f:
        dates = []
        tags = exifread.process_file(f, details=False, stop_tag='EXIF DateTimeOriginal')
        for tag in ('EXIF DateTimeOriginal', 'EXIF DateTimeDigitized', 'Image DateTime'):
            if tag in tags:
                try:
                    dates.append(datetime.strptime(str(tags[tag]), '%Y:%m:%d %H:%M:%S'))
                except ValueError: pass
        if dates:
            return min(dates)
        else:
            return datetime.fromtimestamp(min(os.path.getctime(path), os.path.getmtime(path)))

def upload():
    upload_dir = settings.get('upload_dir', 'upload')
    success_dir = settings.get('success_dir', 'success')
    files = [os.path.join(upload_dir, file) for file in os.listdir(upload_dir)]
    for file in sorted(files, key=guess_time):
        try:
            content_type = 2 if file.lower().endswith('.png') else 1
            print(flickr.upload(photo_file=file, content_type=content_type))
        except flickr.FlickrError as e:
            print(file, e)
            break
        else:
            filename = os.path.basename(file)
            os.rename(file, os.path.join(success_dir, filename))

if __name__ == "__main__":
    settings = load_settings()
    upload()
