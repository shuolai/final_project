from cache import *

url = "https://covid-19-statistics.p.rapidapi.com/reports"

CACHE_DICT = open_cache()

date_list = []

month = ["01","02","03","04","05","06","07","08","09","10","11","12"]
states = ["Alaska", "Alabama", "Arkansas", "Arizona", "California", "Colorado", "Connecticut", "District of Columbia", "Delaware", "Florida", "Georgia", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska"]

states_2 = ["New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]


for m in range(3,12):
    date_list.append("2020-" + month[m] + "-01")

for m in month:
    date_list.append("2021-" + m + "-01")

for m in range(0,4):
    date_list.append("2022-" + month[m] + "-01")

print(len(states))

#make_request_with_cache(url, "Michigan", "2020-04-01")
#make_request_with_cache(url, "Michigan", "2020-05-01")

for state in states:
    for date in date_list:
        make_request_with_cache(url, state, date)
