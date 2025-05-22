from textblob import TextBlob
import re
import nltk
nltk.download('punkt')

DAYS = {
    "monday": "Monday",
    "tuesday": "Tuesday",
    "wednesday": "Wednesday",
    "thursday": "Thursday",
    "friday": "Friday",
    "saturday": "Saturday",
    "sunday": "Sunday",
    "weekends": ["Saturday", "Sunday"],
    "weekdays": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
}

def parse_availability(text):
    text = text.lower()
    blob = TextBlob(text)
    results = []

    for sentence in blob.sentences:
        for day_key, day_val in DAYS.items():
            if day_key in sentence.raw:
                start, end = "10:00", "16:00"
                phrase = sentence.raw

                if "morning" in phrase:
                    start, end = "08:00", "12:00"
                elif "afternoon" in phrase:
                    start, end = "13:00", "17:00"
                elif "evening" in phrase:
                    start, end = "17:00", "20:00"
                elif "all day" in phrase:
                    start, end = "08:00", "18:00"
                elif "after" in phrase:
                    match = re.search(r"after (\d{1,2})(am|pm)?", phrase)
                    if match:
                        hour = int(match.group(1))
                        if match.group(2) == "pm" and hour != 12:
                            hour += 12
                        start = f"{hour:02d}:00"
                        end = "20:00"

                if isinstance(day_val, list):
                    for d in day_val:
                        results.append((d, start, end))
                else:
                    results.append((day_val, start, end))

    return results
