# this program finds all gliding 
# locations available per the British Gliding association website
from time import strftime
import requests, bs4
from urllib.parse import urlparse, parse_qs
import pandas as pd
from datetime import datetime

output_data = []

print('starting...')
print('downloading the club finder page...')

res = requests.get('https://www.gliding.co.uk/club-finder/')

try:
    res.raise_for_status()
    print('done downloading the page.')

except Exception as exc:
    print('There was a problem downloading the page: %s' % (exc))

clubSoup = bs4.BeautifulSoup(res.text, 'html.parser')

glidingClubTags = clubSoup.select('.glidingclub')

for tag in glidingClubTags:
    nameOfClub = tag.find('h2')
    club_name = nameOfClub.text
    
    contact = tag.select('.gliding_contacts')
    for contactTag in contact:
        contactPage = contactTag.find('div',{'class': 'col-2 columnno-1 club-info'})
        clubPhysicalAddress = contactPage.find_all('p')
        club_physical_address = clubPhysicalAddress[0].text

        contactDetails = clubPhysicalAddress[1].find_all('a')
        google_maps_location = contactDetails[0]['href']
        email = contactDetails[1]['href']
        website = contactDetails[2]['href'] if len(contactDetails) == 3 else "none"
        
        parsed_url = urlparse(google_maps_location)

        # extract the coordinates from the google location url
        if parsed_url.query:  # URL has query string
            query_dict = parse_qs(parsed_url.query)

            if '//' in query_dict:
                start_loc = query_dict['//'][0].split("'")[1].split(',')
                end_loc = parsed_url.path.split('@')[1].split(',')[0:2]

            else:
                print("Invalid Google Maps link format!")
                exit()
        else:  # URL does not have query string
            start_loc = parsed_url.path.split("//")[1].split('/')[0].split(',')
            end_loc = parsed_url.path.split('@')[1].split(',')[0:2]

        start_lat, start_long = start_loc
        end_lat, end_long = end_loc

        output_data.append({
            "Club Name": club_name,
            "Address": club_physical_address,
            "Google Maps Location": google_maps_location,
            "Start latitude": start_lat[1:],
            "Start longitude": start_long[:-1],
            "End latitude": end_lat,
            "End longitude": end_long,
            "Email": email,
            "Website": website
        })

df = pd.DataFrame(output_data)

fileName_obj = datetime.now()
filename = fileName_obj.strftime("%Y-%m-%d_%H-%M-%S") + ".xlsx"

df.to_excel(filename, index=False)