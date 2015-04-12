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

def upload():
    upload_dir = settings.get('upload_dir', 'upload')
    success_dir = settings.get('success_dir', 'success')
    for file in os.listdir(upload_dir):
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
