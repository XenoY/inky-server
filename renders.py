import subprocess
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import requests

def render_calendar(month="Juli"):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('calendar.html')
    
    today = datetime.now().strftime("%d.%m.%Y")
    html_out = template.render(month=month, date=today)
    
    html_file = f'temp_{month}.html'
    with open(html_file, 'w') as f:
        f.write(html_out)
    
    png_file = f'static/calendar_{month}.png'
    cmd = ['wkhtmltoimage', '--width', '1600', '--height', '1200', html_file, png_file]
    subprocess.run(cmd, check=True)
    
    print(f'Bild generiert: {png_file}')

def build_html(month="Juli"):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('calendar.html')
    
    today = datetime.now().strftime("%d.%m.%Y")
    html_out = template.render(events=[{
                    "title": "Test",
                    "start": "08:15",
                    "backgroundColor": "#FF0000",
                    "textColor": "#FFFFFF",
                    "allDay": True
                }])

    html_file = f'static/calendar_{month}.html'
    with open(html_file, 'w') as f:
        f.write(html_out)
    
    print(f'HTML generiert: {html_file}')

def fetch_calendar(calendar_url):
    try:
        response = requests.get(calendar_url)
        response.raise_for_status()
        return icalendar.Calendar.from_ical(response.text)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch iCalendar url: {str(e)}")

if __name__ == "__main__":
    render_calendar("Juli")