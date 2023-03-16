# this program finds all gliding 
# locations available per the British Gliding association website
from time import strftime
import requests, bs4
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
        
        output_data.append({
            "Club Name": club_name,
            "Address": club_physical_address,
            "Google Maps Location": google_maps_location,
            "Email": email,
            "Website": website
        })

df = pd.DataFrame(output_data)

fileName_obj = datetime.now()
filename = fileName_obj.strftime("%Y-%m-%d_%H-%M-%S") + ".xlsx"

df.to_excel(filename, index=False)