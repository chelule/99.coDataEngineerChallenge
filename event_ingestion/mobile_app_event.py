from faker import Faker
from datetime import datetime
from time import sleep
import requests

if __name__ == '__main__':
    faker = Faker()
    count = 0
    url = 'http://127.0.0.1:5000/events/'
    while True:
        data = {}
        data['Event_Type'] = 'ListingView'
        data['Event_Version'] = faker.bothify('V#')
        data['User_ID'] = faker.bothify('?#?#?#?##?')
        data['Listing_ID'] = faker.bothify('?#?#?#?##?')
        data['Server_Time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data['Device_Type'] = faker.bothify('iOS #.#')
        print(data)
        r = requests.post(url=url, data=data)
        sleep(5)
