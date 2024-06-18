from django.utils.timezone import now
from datetime import timedelta
import secrets
import string


def generate_custom_id():
    segment_length = 5
    num_segments = 4
    characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    segments = [''.join(secrets.choice(characters) for _ in range(segment_length)) for _ in range(num_segments)]
    return '-'.join(segments)


# Function to format time in 12-hour format
def format_time(datetime_obj):
    return datetime_obj.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')

# Function to format date and time based on conditions
def format_date_and_time(datetime_obj, serializer_type):
    today = now().date()
    start_of_current_year = today.replace(month=1, day=1)

    # Calculate the difference in days from today to the start of the current year
    days_into_year = (today - start_of_current_year).days
    
    # Determine the date one year ago from today, considering the start of the year
    not_current_year = today - timedelta(days=days_into_year + 1)
    if datetime_obj and datetime_obj.date() == today:
        if serializer_type == "message":
            return format_time(datetime_obj)  # Just the time for today
        else:
            return f'Today at {format_time(datetime_obj)}'
    elif datetime_obj and datetime_obj >= now() - timedelta(days=7):  # Within the last 7 days
        return f"{datetime_obj.strftime('%a')} at {format_time(datetime_obj)}"  # Day abbreviation and time
    elif datetime_obj and datetime_obj.date() >= not_current_year:  # Within current year but more than 7 days ago
        day = datetime_obj.day
        formatted_day = str(day) if day > 9 else f'0{day}' 
        return f"{datetime_obj.strftime('%b')} {formatted_day} at {format_time(datetime_obj)}"  # Month abbreviation, day, and time
    else:
        # Not current year or previous years, include the year in the format
        if datetime_obj:
            day = datetime_obj.day
            formatted_day = str(day) if day > 9 else f'0{day}'
            return f"{datetime_obj.strftime('%b')} {formatted_day}, {datetime_obj.strftime('%Y')} at {format_time(datetime_obj)}"