import secrets
import string

def generate_custom_id():
    segment_length = 5
    num_segments = 4
    characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    segments = [''.join(secrets.choice(characters) for _ in range(segment_length)) for _ in range(num_segments)]
    return '-'.join(segments)