from rest_framework import renderers
import json

class UserRenderer(renderers.JSONRenderer):
    charset='utf-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = {}
        
        # Check if there are errors
        if isinstance(data, dict) and 'non_field_errors' in data:
            # Collect non_field_errors
            response['errors'] = ' '.join(data['non_field_errors'])
        elif isinstance(data, dict) and 'errors' in data:
            # Flatten the specific errors
            for field, messages in data['errors'].items():
                response['errors'] = response.get('errors', '') + ' '.join(messages) + ' '
        
        # If there are still no errors, return the original data
        if not response:
            response = data

        return json.dumps(response)