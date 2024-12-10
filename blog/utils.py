import requests

def get_client_ip(request):
    """
    Extract the client's IP from the request. 
    If running on localhost, this may return '127.0.0.1'.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_public_ip():
    """
    Fetch the current public IP using an external service.
    Useful for local development or requests originating from localhost.
    """
    try:
        response = requests.get('https://api.ipify.org?format=json')
        data = response.json()
        return data.get('ip', None)
    except requests.RequestException:
        return None

def get_user_country(request):
    """
    Detect the user's country based on their IP address.
    Uses the public IP if the request comes from localhost.
    """
    ip = get_client_ip(request)
    
    # If IP is localhost, fallback to public IP
    if ip == "127.0.0.1":
        ip = get_public_ip()

    if ip:
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}")
            data = response.json()
            if data.get('status') == 'success':
                return data.get('country', 'Unknown')
        except requests.RequestException:
            pass
    
    return "Unknown"
