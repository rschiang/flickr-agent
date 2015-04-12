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

        tags = exifread.process_file(f)     # EXIFRead won't throw errors
        for tag in ('EXIF DateTimeOriginal', 'EXIF DateTimeDigitized', 'Image DateTime'):
            if tag in tags:
                try:
                    dates.append(datetime.strptime(tags[tag], '%Y:%m:%d %H:%M:%S'))
                except ValueError: pass

        if not dates:
            return min(os.path.getctime(path), os.path.getmtime(path))
        else:
            return min(dates)

def upload():
    upload_dir = settings.get('upload_dir', 'upload')
    success_dir = settings.get('success_dir', 'success')
    files = sorted(os.listdir(upload_dir), key=guess_time)
    for file in files:
        try:
            path = os.path.join(upload_dir, file)
            content_type = 2 if file.lower().endswith('.png') else 1
            print(flickr.upload(photo_file=path, content_type=content_type))
        except flickr.FlickrError as e:
            print(file, e)
            break
        else:
            os.rename(path, os.path.join(success_dir, file))

if __name__ == "__main__":
    settings = load_settings()
    upload()
