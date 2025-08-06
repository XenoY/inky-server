from render.renderer import Renderer
from datetime import datetime
import requests
import icalendar
import recurring_ical_events
from datetime import datetime, timedelta
from PIL import Image, ImageColor, ImageDraw, ImageFont
import os
import json

from config import config

calendars = config.get("calendar", {}).get("entries", [])
print(calendars)
class Calendar(Renderer):
    handle = "calendar"

    @property
    def template_properties(self):
        properties = super().template_properties
        
        current_dt = datetime.now()
        start, end = self.get_view_range(current_dt)
        parsed_events = []

        for entry in calendars:
            calendar = self.fetch_calendar(entry['url'])

            events = recurring_ical_events.of(calendar).between(start, end)
                # contrast_color = self.get_contrast_color(color)
            for event in events:
                start_str, end_end, all_day = self.parse_data_points(event)
                parsed_event = {
                    "title": str(event.get("summary")),
                    "start": start_str,
                    "backgroundColor": entry['color'],
                    "textColor": self.get_contrast_color(entry['color']),
                    "allDay": all_day
                }
                if end_end:
                    parsed_event['end'] = end_end

                parsed_events.append(parsed_event)
        properties.update(events=parsed_events)
        properties.update(weather=self.fetch_weather())
        print(type(properties['weather']))
        return properties

    def fetch_weather(self):
        try:
            response = requests.get("https://aareguru.existenz.ch/v2018/current?city=bern")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise RuntimeError(f"Failed to fetch weather. {e}")


    def fetch_calendar(self, calendar_url):
        try:
            response = requests.get(calendar_url)
            response.raise_for_status()
            return icalendar.Calendar.from_ical(response.text)
        except Exception as e:
            raise RuntimeError(f"Failed to fetch iCalendar url: {str(e)}")

    def get_view_range(self, current_dt):
        start = datetime(current_dt.year, current_dt.month, current_dt.day)

        start = start - timedelta(days=start.weekday())
        end = start + timedelta(weeks=4)
        print(end)
        return start, end

    def parse_data_points(self, event):
        all_day = False
        dtstart = event.decoded("dtstart")
        if isinstance(dtstart, datetime):
            start = dtstart.isoformat()
        else:
            start = dtstart.isoformat()
            all_day = True

        end = None
        if "dtend" in event:
            dtend = event.decoded("dtend")
            if isinstance(dtend, datetime):
                end = dtend.isoformat()
            else:
                end = dtend.isoformat()
        elif "duration" in event:
            duration = event.decoded("duration")
            end = (dtstart + duration).isoformat()
        return start, end, all_day

    def get_contrast_color(self, color):
        """
        Returns '#000000' (black) or '#ffffff' (white) depending on the contrast
        against the given color.
        """
        r, g, b = ImageColor.getrgb(color)
        # YIQ formula to estimate brightness
        yiq = (r * 299 + g * 587 + b * 114) / 1000

        return '#000000' if yiq >= 150 else '#ffffff'