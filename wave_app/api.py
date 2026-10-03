from wave_app.constants import WAVE_NAME
from django.urls import reverse
import urllib.parse
import requests

def create_wave_qr_code(request, wave_id):
    """ Generate QR code using goqr.me API """
    SIZE = 500
    COLOR = '00f'
    MARGIN = 15
    FORMAT = 'svg'
    
    wave_url = request.scheme + '://' + request.get_host() + reverse(WAVE_NAME, kwargs={'wave_id': wave_id})
    wave_url_encoded = urllib.parse.quote(wave_url)
    api_url = f'https://api.qrserver.com/v1/create-qr-code/?data={wave_url_encoded}&size={SIZE}&color={COLOR}&margin={MARGIN}&format={FORMAT}'
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            qr = response.text
            replaced = qr.replace('<?xml version="1.0" standalone="no"?>', '')
            return(replaced)
        else:
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None 