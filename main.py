import json
import flickr_api as flickr

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

if __name__ == "__main__":
    settings = load_settings()
