from rest_framework import renderers
import json

class UserRenderer(renderers.JSONRenderer):
    charset='utf-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        if 'ErrorDetail' in str(data):
            # Flatten the non_field_errors and other field errors into a single message
            if isinstance(data, dict) and 'non_field_errors' in data:
                response = json.dumps({'errors': ' '.join(data['non_field_errors'])})
            if isinstance(data, dict) and 'username' in data:
                response = json.dumps({'errors': ' '.join(data['username'])})
            if isinstance(data, dict) and 'email' in data:
                response = json.dumps({'errors': ' '.join(data['email'])})
            else:
                response = json.dumps({'errors': data})
        else:
            response = json.dumps(data)
        return response