from bs4 import BeautifulSoup
import requests
import re

# similar to our API requests, but now we just want all the text
html = requests.get('https://www.usclimatedata.com/').text
# instead of converting to JSON, use BeautifulSoup and an html parser to read in the data
soup = BeautifulSoup(html, 'html.parser') # HTML parsing is basically: taking in HTML code and extracting relevant information 
                                        #like the title of the page, paragraphs in the page, headings in the page, links, bold text etc.
#print(soup.prettify()) # sanity check. Similar to json.dumps(json_object, indent=2)

weather_list = {}

month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

state_listing_parent = soup.find('div', class_='row states')
state_listing_divs = state_listing_parent.find_all('div', recursive=False)



for div in state_listing_divs:
    state_link_tag = div.find('a')
    state_details_path = state_link_tag['href']
    state_path = "https://www.usclimatedata.com" + state_details_path
    #print("https://www.usclimatedata.com" + course_details_path)
    #print(course_link_tag['title'])
    state_html = requests.get(state_path).text
    soup = BeautifulSoup(state_html, 'html.parser')
    weather_year_data = soup.find_all('td', class_='high text-right')
    state_weather = {}
    state_weather_temp = []
    for weather in weather_year_data:
        state_weather_temp.append(weather.text)
    for x in range(0,12):
        state_weather[month_list[x]] = state_weather_temp[x]
    weather_list[state_link_tag['title']] = state_weather
    


print(weather_list)

# instead of converting to JSON, use BeautifulSoup and an html parser to read in the data
#soup = BeautifulSoup(html, 'html.parser') # HTML parsing is basically: taking in HTML code and extracting relevant information 
                                        #like the title of the page, paragraphs in the page, headings in the page, links, bold text etc.
#print(soup.prettify()) # sanity check. Similar to json.dumps(json_object, indent=2)

#import re

#course_listing_parent = soup.find_all('td', class_='high text-right')

#print(course_listing_parent[0].text)

#course_listing_divs = course_listing_parent.find_all('div', recursive=False)

