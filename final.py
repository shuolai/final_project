from cache import *
import json
from bs4 import BeautifulSoup
from flask import Flask, render_template
import requests
import re
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def extract_covid_data():
    url = "https://covid-19-statistics.p.rapidapi.com/reports"

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

    if os.path.exists('covid_data.json'):
        pass
    else:
        # load monthly covid data for state in list states
        cache_dict = open_cache("covid_data.json")
        for state in states:
            for date in date_list:
                make_request_with_cache(url, state, date, cache_dict, "covid_data.json")

    if os.path.exists('covid_data_2.json'):
        pass
    else:
        # load monthly covid data for state in list states_2
        cache_dict_2 = open_cache("covid_data_2.json")
        for state in states_2:
            for date in date_list:
                make_request_with_cache(url, state, date, cache_dict_2, "covid_data_2.json")
    
    monthly_confirmed = {}
    total_confirmed  ={}

    file = open('covid_data.json')
    data = json.load(file)

    for state in states:
        state_monthly_confirmed_list = []
        for year_month in date_list[:-1]:
            month_key = state + "_" + year_month
            next_month_key = state + "_" + date_list[date_list.index(year_month)+1]
            confirmed_in_month = data[next_month_key]["data"][0]['confirmed'] - data[month_key]["data"][0]['confirmed']
            state_monthly_confirmed_list.append(confirmed_in_month)
        monthly_confirmed[state] = state_monthly_confirmed_list

        month_key = state + "_" + date_list[-1]
        total_confirmed[state] = data[month_key]["data"][0]['confirmed']

    file = open('covid_data_2.json')
    data = json.load(file)

    for state in states_2:
        state_monthly_confirmed_list = []
        for year_month in date_list[:-1]:
            month_key = state + "_" + year_month
            next_month_key = state + "_" + date_list[date_list.index(year_month)+1]
            confirmed_in_month = data[next_month_key]["data"][0]['confirmed'] - data[month_key]["data"][0]['confirmed']
            state_monthly_confirmed_list.append(confirmed_in_month)
        monthly_confirmed[state] = state_monthly_confirmed_list

        month_key = state + "_" + date_list[-1]
        total_confirmed[state] = data[month_key]["data"][0]['confirmed']

    # return list of sample date, number of monthly confirmed people and the number of total confirmed people for each state
    return date_list, monthly_confirmed, total_confirmed


def extract_weather_high_data():
    if os.path.exists('weather_high.json'):
        pass
    else:
        # similar to our API requests, but now we just want all the text
        html = requests.get('https://www.usclimatedata.com/').text
        # instead of converting to JSON, use BeautifulSoup and an html parser to read in the data
        soup = BeautifulSoup(html, 'html.parser') # HTML parsing is basically: taking in HTML code and extracting relevant information 
                                                #like the title of the page, paragraphs in the page, headings in the page, links, bold text etc.
        #print(soup.prettify()) # sanity check. Similar to json.dumps(json_object, indent=2)

        weather_dict = {}

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
            state_weather = []
            for weather in weather_year_data:
                state_weather.append(int(weather.text))
            state_weather = state_weather[3:12] + state_weather + state_weather[0:3]
            #for x in range(0,12):
            #    state_weather[month_list[x]] = state_weather_temp[x]
            weather_dict[state_link_tag['title']] = state_weather
            print("finish " + state_link_tag['title'])
            
        dumped_json_cache = json.dumps(weather_dict)
        fw = open("weather_high.json","w")
        fw.write(dumped_json_cache)
        fw.close() 

def extract_weather_low_data():
    if os.path.exists('weather_low.json'):
        pass
    else:
        # similar to our API requests, but now we just want all the text
        html = requests.get('https://www.usclimatedata.com/').text
        # instead of converting to JSON, use BeautifulSoup and an html parser to read in the data
        soup = BeautifulSoup(html, 'html.parser') # HTML parsing is basically: taking in HTML code and extracting relevant information 
                                                #like the title of the page, paragraphs in the page, headings in the page, links, bold text etc.
        #print(soup.prettify()) # sanity check. Similar to json.dumps(json_object, indent=2)

        weather_dict = {}

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
            weather_year_data = soup.find_all('td', class_='low text-right')
            state_weather = []
            for weather in weather_year_data:
                state_weather.append(int(weather.text))
            state_weather = state_weather[3:12] + state_weather + state_weather[0:3]
            #for x in range(0,12):
            #    state_weather[month_list[x]] = state_weather_temp[x]
            weather_dict[state_link_tag['title']] = state_weather
            print("finish " + state_link_tag['title'])
            
        dumped_json_cache = json.dumps(weather_dict)
        fw = open("weather_low.json","w")
        fw.write(dumped_json_cache)
        fw.close() 

def extract_population_data():
    population_dict = {}

    # similar to our API requests, but now we just want all the text
    html = requests.get('https://en.wikipedia.org/wiki/List_of_U.S._states_and_territories_by_population').text
    # instead of converting to JSON, use BeautifulSoup and an html parser to read in the data
    soup = BeautifulSoup(html, 'html.parser') # HTML parsing is basically: taking in HTML code and extracting relevant information 
                                            #like the title of the page, paragraphs in the page, headings in the page, links, bold text etc.
    #print(soup.prettify()) # sanity check. Similar to json.dumps(json_object, indent=2)

    population_table = soup.find('table').findAll('tr')

    for x in range(2,58):
        population_dict[population_table[x].find('a')['title']] = int(population_table[x].findAll('td')[2].text.replace(',', ''))

    #print(population_table[2].find('a')['title'])

    #print(int(population_table[55].findAll('td')[2].text.replace(',', '')))

    population_dict["District of Columbia"] = population_dict.pop("Washington, D.C.")
    population_dict["Georgia"] = population_dict.pop("Georgia (U.S. state)")
    population_dict["New York"] = population_dict.pop("New York (state)")
    population_dict["Washington"] = population_dict.pop("Washington (state)")

    return population_dict

def extract_population_data_2():
    if os.path.exists("population.json"):
        pass
    else:
        population_dict = {}

        # similar to our API requests, but now we just want all the text
        html = requests.get('https://www.infoplease.com/us/states/state-population-by-rank').text
        # instead of converting to JSON, use BeautifulSoup and an html parser to read in the data
        soup = BeautifulSoup(html, 'html.parser') # HTML parsing is basically: taking in HTML code and extracting relevant information 
                                                #like the title of the page, paragraphs in the page, headings in the page, links, bold text etc.
        #print(soup.prettify()) # sanity check. Similar to json.dumps(json_object, indent=2)

        population_table = soup.find('table').findAll('tr')

        for x in range(1,52):
            population_dict[population_table[x].find('a').text] = int(population_table[x].findAll('td')[2].text.replace(',', ''))

        #print(population_table[2].find('a').text)

        #print(population_table[2].findAll('td')[2].text.replace(',', ''))

        population_dict["District of Columbia"] = population_dict.pop("DC")

        #print(population_dict)

        dumped_json_cache = json.dumps(population_dict)
        fw = open("population.json","w")
        fw.write(dumped_json_cache)
        fw.close() 

def weather_and_covid(state_item, date_list, monthly_confirmed):
    #state_item = "California"
    file = open('weather_high.json')
    weather_high = json.load(file)
    file.close()
    file = open('weather_low.json')
    weather_low = json.load(file)
    file.close()

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Bar(x=date_list, y=monthly_confirmed[state_item], name="monthly_confirmed"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=date_list, y=weather_high["Climate " + state_item], name="monthly_high_temperature", line=dict(shape='spline')),
        secondary_y=True,
    )

    fig.add_trace(
        go.Scatter(x=date_list, y=weather_low["Climate " + state_item], name="monthly_low_temperature",line=dict(shape='spline')),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text = state_item + " weather and covid confirmed number."
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Date")

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Confirmed Number</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Temperature in °F</b>", secondary_y=True)
    fig.update_yaxes(range=[0,120], secondary_y=True)

    fig.show()

def show_risk_level(json_dict, state_item):
    country_number = 23.73

    xval = [state_item , "U.S."]
    yval = [json_dict[state_item]['risk_number'], country_number]

    bar_data = go.Bar(x=xval, y=yval)
    fig = go.Figure(data = bar_data)
    fig.update_layout(width=800,height=600)
    
    # Add figure title
    if json_dict[state_item]['risk_level'] == "Low":
        fig.update_layout(
            title_text = state_item + "\'s travel risk level is: " + json_dict[state_item]['risk_level'],
            title_font_color="green"
        )
    elif json_dict[state_item]['risk_level'] == "Medium":
        fig.update_layout(
            title_text = state_item + "\'s travel risk level is: " + json_dict[state_item]['risk_level'],
            title_font_color="orange"
        )
    else:
        fig.update_layout(
            title_text = state_item + "\'s travel risk level is: " + json_dict[state_item]['risk_level'],
            title_font_color="red"
        )

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Confirmed Number in 100 people.</b>")

    fig.show()

def travel_recommendation(json_dict):
    print("Available locations are: Northeast/Southeast/Midwest/Southwest/West")
    state_location = input("Please enter the location you would like to check: ")
    state_selected = []
    for state_key in json_dict.keys():
        if json_dict[state_key]['location'] == state_location:
            state_selected.append(state_key)

    state_selected = [x for x in state_selected if json_dict[x]['risk_level'] == "Low"]

    if state_selected:
        temp_list = []
        month = int(input("Please enter the month you would like to travel (1 - 12): "))
        for state in state_selected:
            state_average = (json_dict[state]['weather_low'][month-1] + json_dict[state]['weather_high'][month-1])/2 
            temp_list.append(abs(state_average - 71.6))
        print("The recommended travel destination is " + state_selected[temp_list.index(min(temp_list))] + "!")
    else:
        print("There is no low-risk state in the location you choose. We do not recommend you to travel at this time.")

def travel_html():
    app = Flask(__name__)
    @app.route('/')
    def index():     
        return render_template('recommendation.html')
    app.run()

def create_json_file(total_confirmed):
    if os.path.exists("data.json"):
        file = open('data.json')
        json_dict = json.load(file)
        file.close()
        return json_dict
    else:
        json_dict = {}

        location_dict = {
        "Northeast" : ["Maine", "Massachusetts", "Rhode Island", "Connecticut", "New Hampshire", "Vermont", "New York", "Pennsylvania", "New Jersey", "Delaware", "Maryland", "District of Columbia"],
        "Southeast" : ["West Virginia", "Virginia", "Kentucky", "Tennessee", "North Carolina", "South Carolina", "Georgia", "Alabama", "Mississippi", "Arkansas", "Louisiana", "Florida"],
        "Midwest" : ["Ohio", "Indiana", "Michigan", "Illinois", "Missouri", "Wisconsin", "Minnesota", "Iowa", "Kansas", "Nebraska", "South Dakota", "North Dakota"],
        "Southwest" : ["Texas", "Oklahoma", "New Mexico", "Arizona"],
        "West" : ["Colorado", "Wyoming", "Montana", "Idaho", "Washington", "Oregon", "Utah", "Nevada", "California", "Alaska", "Hawaii"]
        }

        file = open('weather_high.json')
        weather_high = json.load(file)
        file.close()
        file = open('weather_low.json')
        weather_low = json.load(file)
        file.close()
        file = open('population.json')
        population_dict = json.load(file)
        file.close()

        for state in total_confirmed.keys():

            state_dict  ={}
            state_number = total_confirmed[state] * 100 / population_dict[state]
            state_dict["risk_number"] = state_number

            if state_number < 22:
                state_dict["risk_level"] = "Low"
            elif state_number < 24:
                state_dict["risk_level"] = "Medium"
            else:
                state_dict["risk_level"] = "High"

            for key in location_dict.keys():
                if state in location_dict[key]:
                    state_dict["location"] = key
                    break

            state_dict["weather_high"] = weather_high["Climate " + state][9:21]
            state_dict["weather_low"] = weather_low["Climate " + state][9:21]

            json_dict[state] = state_dict

        dumped_json_cache = json.dumps(json_dict)
        fw = open("data.json","w")
        fw.write(dumped_json_cache)
        fw.close() 

        return json_dict

def main():
    date_list, monthly_confirmed, total_confirmed = extract_covid_data()
    extract_population_data_2()
    extract_weather_high_data()
    extract_weather_low_data()
    json_dict = create_json_file(total_confirmed)

    running = True
    print("Welcome to the covid and weather system.")
    while running:
        print("1. Check weather and covid data for a state.")
        print("2. Check the risk level for a state.")
        print("3. Find a recommended travel destination.")
        print("4. Check all recommended travel destinaitons.")
        number = input("Please enter the number for your search option: ")
        if number == "1":
            state_item = input("Please enter the state you would like to check: ")
            weather_and_covid(state_item, date_list, monthly_confirmed)
            running_flag = input("Would you like to continue searching other information? (yes or no) ")
            if running_flag == "no":
                running = False
        elif number == "2":
            state_item = input("Please enter the state you would like to check: ")
            show_risk_level(json_dict, state_item)
            running_flag = input("Would you like to continue searching other information? (yes or no) ")
            if running_flag == "no":
                running = False
        elif number == "3":
            travel_recommendation(json_dict)
            running_flag = input("Would you like to continue searching other information? (yes or no) ")
            if running_flag == "no":
                running = False
        elif number == "4":
            travel_html()
            running_flag = input("Would you like to continue searching other information? (yes or no) ")
            if running_flag == "no":
                running = False
        else:
            print("### Please enter a valid number! (1 - 3) ###")

    print("Thank you for using the covid and weather system! Bye!")

 
#
# The following two-line "magic sequence" must be the last thing in
# your file.  After you write the main() function, this line it will
# cause the program to automatically start when you run it.
#
if __name__ == '__main__':
    main()
