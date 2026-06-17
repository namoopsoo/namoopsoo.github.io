---
title: "Quantifying Delays"
# slug: "2026-06-03--fun-delays"
date: 2026-06-03T23:12:20-04:00
draft: false

# optional thumbnail
#images:
#  - "THUMBNAIL_PLACEHOLDER"
#cover:
#  image: "THUMBNAIL_PLACEHOLDER"
---


I was worried I would lose the american airlines app notifications but luckily the email notifications persisted.

So here is some of my data, extracted from emails from aa.com 

 I wanted to use some data to tell the story of a recent trip I was taking from NY to Arizona. I left a very engaging group discussion at work because I planned a tight bike ride home to wrap up a quick exit to the airport in time to board my plane.

But then my flight was delayed several times through the end of the evening. Finally at around 11:40pm, the passengers, including a whole school trip full of high schoolers waiting in the airport, and myself, were told to come back at 5am for a 6am flight.

When I got home, preparing to sleep for barely 2 hours, I got an alert on my AA app that the flight would now be delayed another 2 hours. This actually brought me some slight relief, since I could add two more hours to my sleep. Or so I thought. When I woke up, I saw a new notification from AA saying that the flight was now back on track for a 6am departure. 

The flight was essentially boarding while I was brushing my teeth.

I was kind of over it, ready to just give up, but I had already planned a Lyft morning pickup, so I showered and got outside to take my scheduled ride. On the ride to the airport I was able to use the chat interface on my AA app to state my situation and given 4 options I was able to rebook to a new flight. Kind of cool actually. However I could not download a boarding pass. So at the airport, at the AA counter, I learned from a staff member helping me, that I was indeed rebooked, but my new flights were not completely getting cleaned up, updated. 

So this was my first experience using agentic AI to get my flight rebooked but haha the production data was buggy and required a human staff member to wrestle at the AA terminal for I would say about 15 minutes to straighten it out.





On the return trip, I also had a delay, and my ~55 minute layover turned into a ~35 minute layover and so I was trying to figure out whether I should attempt to rebook again or stay the course. Boarding would start while I would be leaving the plane for the first flight. And the flights are in two different terminals. I took the risk since AA didn't rebook me automatically. I had done my research about the Dallas Fortworth airport and how I needed to take the skytrain two stops between the two terminals I needed to go between during my layover. 

Yea I was one of the last people to board the plane, but I somehow made it!

In any case, the below is a bit of the data trail of what happened.

## Data trail


```python
#!/usr/bin/env python3

import csv
import re
import polars as pl
from pathlib import Path
from email import policy
from email.parser import BytesParser


def extract_text(msg):
    """Get HTML body if present, otherwise plain text."""
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            if ctype == "text/html":
                return part.get_content()
        for part in msg.walk():
            ctype = part.get_content_type()
            if ctype == "text/plain":
                return part.get_content()
    else:
        return msg.get_content()

    return ""


def extract_from_eml_file(eml_file):

    with open(eml_file, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)

    subject = msg.get("Subject", "")
    date = msg.get("Date", "")

    body = extract_text(msg)

    flight_match = re.search(
        r"Flight\s+(\d+)\s+to\s+([A-Z]{3})",
        body,
        re.IGNORECASE,
    )

    flight_number = flight_match.group(1) if flight_match else ""
    airport = flight_match.group(2) if flight_match else ""

    delay_match = re.search(
        r"Your flight from .*? is now scheduled to depart at (.*?) (as|after) (.*?)\.",
        body,
        re.IGNORECASE | re.DOTALL,
    )
    if delay_match:
        new_time = delay_match.group(1).strip()
        reason = delay_match.group(3).strip()
        delay_line = delay_match.group(0).strip()
        
    else:    
        delay_match = re.search(
            r"Your flight from .*? is delayed while (.*?)\..*?"
            r"The new departure time is (.*?)\.",
            body,
            re.IGNORECASE | re.DOTALL,
        )
    
        if delay_match:
            reason = delay_match.group(1).strip()
            new_time = delay_match.group(2).strip()
            delay_line = delay_match.group(0).strip()
        else:
            """<sp=
an>Your flight from Phoenix to Dallas Fort Worth is delayed after maintenan=
ce was required on a plane assigned to your flight. We're sorry for the dis=
ruption to your travel plans. The new departure time is 10:57 a.m.<br><br>G=
etting you to Dallas Fort Worth safely is our top priority.<br><br>You can =
check the American app for more information, and we'll keep you updated on =
any changes to your trip. We appreciate your patience as we get you on your=
 way.</span>"""
            delay_match = re.search(
                r"Your flight from .*? is delayed (.*?) We're sorry.*The new departure time is (\d\d:\d\d [ap].m.)",
                body,
                re.IGNORECASE | re.DOTALL,

            )
            if delay_match:
                reason = delay_match.group(1).strip()
                new_time = delay_match.group(2).strip()
                delay_line = delay_match.group(0).strip()
            else:
                reason = ""
                new_time = ""
                delay_line = ""
    

    return ({
        "file": eml_file.name,
        "date": date,
        "subject": subject,
        "flight_number": flight_number,
        "airport": airport,
        "new_departure_time": new_time,
        "reason": reason,
        "delay_line": delay_line,
    })

    
```


```python
workdir = Path.home() / "Documents/2026-05-29-Scottsdale-Arizona/aa-emails"

# /2157515147\ -\ Your\ flight\ to\ Dallas_Fort\ Worth\ -\ Delayed.eml [I 2026-06-06 18:32:15.116 ServerApp] Saving file at /2026-06-04--aa-e
```


```python
for eml_file in  workdir.glob("*Delayed.eml"):
    break
eml_file.name
```




    '2157470468 - Your flight to Dallas_Fort Worth - Delayed.eml'




```python
extract_from_eml_file(eml_file)
```




    {'file': '2157470468 - Your flight to Dallas_Fort Worth - Delayed.eml',
     'date': 'Sat, 30 May 2026 02:28:12 +0000',
     'subject': 'Your flight to Dallas/Fort Worth - Delayed',
     'flight_number': '1571',
     'airport': 'DFW',
     'new_departure_time': 'May. 29, 11:15 p.m.',
     'reason': 'we continue to wait for your crew following an earlier delay',
     'delay_line': 'Your flight from New York to Dallas Fort Worth is now scheduled to depart at May. 29, 11:15 p.m. as we continue to wait for your crew following an earlier delay.'}




```python
data = extract_from_eml_file(workdir / '2159540012 - Your flight to Dallas_Fort Worth - Delayed.eml')
data["delay_line"], "reason", data["reason"]
data
```




    {'file': '2159540012 - Your flight to Dallas_Fort Worth - Delayed.eml',
     'date': 'Mon, 01 Jun 2026 16:25:39 +0000',
     'subject': 'Your flight to Dallas/Fort Worth - Delayed',
     'flight_number': '3284',
     'airport': 'DFW',
     'new_departure_time': '',
     'reason': '',
     'delay_line': ''}




```python
rows = []
for eml_file in  workdir.glob("*Delayed.eml"):
    rows.append(extract_from_eml_file(eml_file))
```


```python
df = pl.from_dicts(rows)
#df.filter(pl.col("new_departure_time").is_in([""]))[0]["file"][0]
df.to_dicts()
#df
[ [x["date"], x["new_departure_time"], x["reason"]] for x in rows]
```




    [['Sat, 30 May 2026 02:28:12 +0000',
      'May. 29, 11:15 p.m.',
      'we continue to wait for your crew following an earlier delay'],
     ['Sat, 30 May 2026 06:41:50 +0000',
      '9:45 a.m.',
      'your flight crew continues to prepare for takeoff'],
     ['Sat, 30 May 2026 01:42:00 +0000',
      'May. 29, 10:40 p.m.',
      'we wait for your crew following an earlier delay'],
     ['Fri, 29 May 2026 11:12:42 +0000',
      '7:02 p',
      'we prepare another plane to operate this flight'],
     ['Fri, 29 May 2026 20:58:33 +0000',
      '8:30 p.m.',
      'maintenance was required on a plane assigned to your flight'],
     ['Sat, 30 May 2026 03:07:57 +0000',
      '6:00 a.m.',
      'your flight crew needs more time to prepare for takeoff'],
     ['Fri, 29 May 2026 23:34:33 +0000',
      '9:45 p.m.',
      'your flight crew needs more time to prepare for takeoff'],
     ['Mon, 01 Jun 2026 16:25:39 +0000',
      '10:57 a.m.',
      'after maintenance was required on a plane assigned to your flight.'],
     ['Fri, 29 May 2026 20:17:21 +0000',
      '8:07 p.m.',
      'maintenance was required on a plane assigned to your flight'],
     ['Sat, 30 May 2026 01:34:01 +0000',
      'May. 29, 10:15 p.m.',
      'your flight crew continues to prepare for takeoff'],
     ['Sat, 30 May 2026 04:47:29 +0000',
      '8:00 a.m.',
      'your flight crew continues to prepare for takeoff']]




```python

```
