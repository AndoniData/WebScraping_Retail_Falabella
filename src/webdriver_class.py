from urllib.parse import urlparse
import json
# import logging as log

# log.basicConfig(level=log.INFO)
# logger = log.getLogger(__name__)

class WebDriver(object):
    def __init__(self, request):
        if not request:
            raise ValueError("Request object cannot be None")
        
        if not hasattr(request, 'method') or not request.method:
            raise ValueError("Request must have a valid method")
        
        if not hasattr(request, 'url') or not request.url:
            raise ValueError("Request must have a valid URL")
        
        if not hasattr(request, 'headers'):
            raise ValueError("Request must have headers attribute")
        
        self.request = request
        self.method = request.method
        self.headers = request.headers.items()
        self.cookies = request.headers.get('Cookie', None)
        self.url = request.url
        self.body = self._get_body()
        self.params = self._get_params()

    def _get_body(self):
        if not self.request.body:
            return None
        else:
            try:
                return self.request.body.decode('utf-8') if isinstance(self.request.body, bytes) else self.request.body
            except Exception as e:
                #logger.error(f"Error decoding request body: {e}")
                return None

    def _get_params(self):
        if not self.url:
            return {}
        
        try:
            parsed_url = urlparse(self.url)
            params = {}
            if parsed_url.query:
                for param in parsed_url.query.split('&'):
                    if '=' in param:
                        key, value = param.split('=', 1)
                        params[key] = value
                    else:
                        # Handle parameters without values
                        params[param] = ''
            return params
        except Exception as e:
            #logger.error(f"Error parsing URL parameters: {e}")
            return {}       

    def dict_format(self):
        try:
            return {
                'method': self.method,
                'headers': dict(self.headers) if self.headers else {},
                'cookies': self.cookies,
                'url': self.url,
                'body': self.body,
                'params': self.params
            }
        except Exception as e:
            #logger.error(f"Error creating dictionary format: {e}")
            return {
                'method': getattr(self, 'method', None),
                'headers': {},
                'cookies': getattr(self, 'cookies', None),
                'url': getattr(self, 'url', None),
                'body': getattr(self, 'body', None),
                'params': getattr(self, 'params', {})
            }
    
    def __repr__(self):
        try:
            # Create a safe dictionary for JSON serialization
            safe_dict = {}
            for key, value in self.__dict__.items():
                if key == 'request':
                    # Skip the request object as it might not be JSON serializable
                    continue
                try:
                    # Test if the value is JSON serializable
                    json.dumps(value)
                    safe_dict[key] = value
                except (TypeError, ValueError):
                    # If not serializable, convert to string representation
                    safe_dict[key] = str(value)
            
            return json.dumps(safe_dict, indent=4)
        except Exception as e:
            #logger.error(f"Error in __repr__: {e}")
            return f"WebDriver object (error in representation: {str(e)})"
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print(f"Exception occurred in context manager: {exc_type.__name__}: {exc_value}")
            pass
        return False

