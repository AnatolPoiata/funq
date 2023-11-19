import streamlit as st
from streamlit_extras.app_logo import add_logo

from datetime import datetime, date, timedelta 
import pandas as pd

import requests
import json
import googlemaps

airports_city = pd.read_csv('./data/IATA_city.csv')
airports_city.dropna(subset=['Code'], inplace=True)
airports_city['city_long'] = airports_city['City'] + ', ' +airports_city['Country'] + ', '+airports_city['Code']

#server_url="http://89.32.236.109"
#itinerary_url="http://89.32.236.109:5000/"

flight_url="https://app-flight-3f9c6f645f67.herokuapp.com/"
itinerary_url = "https://app-itinerary-72ec0834c265.herokuapp.com/"

now_date = datetime.now()

#place_details = ['business_status',   'formatted_address', 'name', 'opening_hours', 'photos', 'place_id', 'price_level', 'rating',  'types', 'user_ratings_total']

df = pd.read_excel('./data/POIs.xlsx')
full_name = []
for i, row in df.iterrows():
	dest = ''
	if (len(str(row['city'])) > 0):
		dest = row['city']
	if ((len(str(row['region'])) > 0)&(row['city'] != row['region'])):
		dest = dest + ','+row['region']
	if ((len(str(row['country'])) > 0)&(row['city'] != row['country']) & (row['region'] != row['country'])):
		dest = dest + ','+row['country']
	full_name.append(dest)

df['Full'] = full_name
df.drop_duplicates(subset='Full', inplace=True)
df.sort_values(by='Full', ascending=True, inplace=True)
destinations = df['Full']


df1 = pd.read_csv('./data/worldcities.csv')

worldcities = df1[['city_ascii',	'lat', 'lng', 'country']].copy()

worldcities['city_long'] = worldcities['city_ascii'] + ', ' + worldcities['country']


st.set_page_config(layout="wide")




def trip_planner_section():

	day = 3
	st.empty()
	col1, col2, col3, col4 = st.columns([0.1, 0.1 ,0.7, 0.1], gap="small")

	with col1:
		st.image("./images/logo.png")
	
	with col3:
		st.header("Personal Trip Planner")

		destination = st.selectbox("Enter the place you want to visit", destinations, index=None)
		days = st.slider('Number of Days ', 1, 7, day) 
#		prefered_date = st.date_input('Prefered date to travel', value=None)
#		options = st.multiselect(
#			'What activities are you interested in ?',
#			['City walks', 'Local food', 'Wine', 'Shopping', 'Art&Culture', 'Wellness', 'Outdoors', 'History', 'Popular attractions', 'Hidden gems', 'Museums', 'Nightlife' ],
#			max_selections=5, help='Select up to 5')

		preferred_transport = st.multiselect(
			'Preferred transport',
			['Walking as much as I can', 'Public transport', 'Rental car', 'Taxi'],
			max_selections=1, help='Select one')

		add_info = st.text_area('Additional Information', height=200, value='I want to visit as many places as possible')

		if st.button("Send", key="button1"): 
			if destination:
#				user_input_prompt = 'Plan a trip to ' + user_input + ' for '+ str(days)+ ' days, strating from '+ prefered_date.strftime('%B %d, %Y')

				city = df[df['Full']==destination]['city'].to_list()[0]
				region = df[df['Full']==destination]['region'].to_list()[0]
				country = df[df['Full']==destination]['country'].to_list()[0]

				user_input =  {
						'destination': {
							"city": city,
							"region": region,
							"country": country,
							'days': days,
#						'prefered_date': prefered_date.strftime('%B %d, %Y'),
#						'options': options,
							'preferred_transport': preferred_transport
							},
						'add_info': add_info.strip(),
						}

				user_input = json.dumps(user_input)

				header = {'Content-Type': 'application/json', 'Accept': 'application/json'}

				candidates = requests.post(itinerary_url+"itinerary_candidates", json=user_input, headers= header)
				
				json_object = json.loads(candidates.content)
				st.write(json_object)

				json_object  = str(candidates.content).encode('utf-8').replace("'\': nan,", "'\': 0")
				
				st.write(json_object)

				st.write(json.loads(json_object))
				new_input = json.dumps(json.loads(json_object))

				route = requests.post(itinerary_url+"new_trip", json=new_input, headers= header)

				return route
			else:
				return 'NULL'


def show_itinerary(input_data):

#	if 'output' not in st.session_state:
#		st.session_state['output'] = '--'
	response = json.loads(input_data)

	print('response:',response)
	
	df = pd.DataFrame(response['data'])
	print('Overview',response['overview'])
#	print('Buget', response['estimated_buget'])
#	print('Add_info', response['add_info_response'])

	details = []

	for i, row in df.iterrows():
		print('i=', i)
		day = row['day']
		itin = row['itinerary']

		for it in itin:

			try:
				stop = it['stop']
			except:
				stop = None
			try:	
				name = it['name']
			except:
				name = None
			try:		
				place =it['place']
			except:
				place = None
			try:	
				gmap_id = it['gmap_id']
			except:
				gmap_id = None
			try: 
				price_per_ticket = it['price_per_ticket']
			except:
				price_per_ticket = None
			try:
				duration_hours = it['duration_hours']
			except:
				duration_hours = None
			try:
				category = it['category']
			except:
				category = None
			try:
				rating = it['rating']
			except:
				rating = None
			try:
				description_long = it['description_long']
			except:
				description_long = None
			try:
				description_short = it['description_short']
			except:
				description_short = None
			try:
				reason = it['reason']
			except:
				reason = None
			try:
				transportation = it['transportation']
			except:
				transportatio= None
			try:
				lat = it['lat']
			except:
				lat = None
			try:
				lon = it['lon']
			except:
				lon = None
			try:
				opening_hours = it['opening_hours']
			except:
				opening_hours = None
			try:
				time_to_visit = it['time to visit']
			except:
				time_to_visit = None


			detail = {
				"day": day,
				"stop": stop,
				"name": name,
				"place": place,
				"gmap_id": gmap_id, 
				"price_per_ticket": price_per_ticket,
				"duration_hours": duration_hours,
				"category": category,
				"rating": rating,
				"description_long": description_long,
				"description_short": description_short,
				"reason": reason,
				"transportation": transportation,
				"lat": lat,
				"lon": lon,
				"opening_hours": opening_hours,
				"time_to_visit": time_to_visit
				 }
			print(detail)

			details.append(detail)

	df = pd.DataFrame(details)


	df['lat'] = df['lat'].astype(float)
	df['lon'] = df['lon'].astype(float)

	st.empty()
	st.title('Itinerary')

	header = st.columns(2)
	header[0].subheader('Itinerary details')
	header[1].subheader('Itieneray map')

	row1 = st.columns(2)

	row1[0].write(response)
	row1[1].map(df[['day', 'stop', 'lat', 'lon']], latitude='lat', longitude='lon')

	return



def get_response(system_message, user_input):
	messages = [
		Message(role="system", content=system_message, ),
		Message(role="user", content=user_input)
	]

	options = Options(messages=messages)
	output = service.chat(options)
	return output

def flight_submit():	

	origin = st.session_state.origin
	origin = origin.split(', ')[-1]

	destination = st.session_state.destination
	destination = destination.split(', ')[-1]

	departure_date = st.session_state.departure_date
	departure_date = departure_date.strftime("%Y-%m-%d")

	return_date = st.session_state.departure_date
	return_date = return_date.strftime("%Y-%m-%d")

	pax = str(st.session_state.passengers)
	cabin = st.session_state.cabin.upper()
#	cabin = cabin.upper()

	request_data = {
					"currencyCode": "USD",
					"originDestinations": [
											{
											"id": "1",
											"originLocationCode": origin,
											"destinationLocationCode": destination,
											"departureDateTimeRange": {
												"date": departure_date,
												}
											},
											{
											"id": "2",
											"originLocationCode": origin,
											"destinationLocationCode": destination,
											"departureDateTimeRange": {
												"date": return_date,
												}
											},

										],

					"travelers": [
									{
										"id": pax,
										"travelerType": "ADULT"
									}
								],
					"sources": [
								"GDS"
								],
					"searchCriteria": {
							"maxFlightOffers": 3,
							"flightFilters": {
								"cabinRestrictions": [
												{
												"cabin": cabin,
												"coverage": "MOST_SEGMENTS",
												"originDestinationIds": [
													"1"
													]
												}
											]
										}
								}
					}


	header = {'Content-Type': 'application/json', 'Accept': 'application/json'}
	
#	print(request_data)

	user_input = json.dumps(request_data)

	response = requests.post(flight_url+"flight_search", data=user_input, headers= header)

	resp = response.content
	st.write(json.loads(resp))

	st.session_state.json_data = response

	return response
	
#	response = requests.post("http://localhost:2222/flight_search", json=user_input)

	data = response.content

#	print('response:', data)

#	response = json.loads(data)['data']
	response = json.loads(data)

	st.write(response)

	result = response
	st.session_state.json_data = result

#	return response


def flight_search_section():

	if 'json_data' not in st.session_state:
		st.session_state.json_data = ''

	if 'output' not in st.session_state:
		st.session_state['output'] = '--'

	st.title("Flight Search")
	st.subheader('Let us plan your trip!')

	with st.form(key='flight_form'):
		c1, c2, c3, c4, c5, c6 = st.columns([3,3,2,2,1,2])

		with c1:
			st.selectbox("From", airports_city['city_long'], key='origin', index=None, placeholder='Origin')

		with c2:
			st.selectbox("To", airports_city['city_long'], key='destination', index=None, placeholder='Destination')

		with c3:
			st.date_input('Departure Date', value=now_date + timedelta(days=1), key='departure_date')

		with c4:
			st.date_input('Return Date', value=now_date + timedelta(days=1), key='return_date')

		with c5:
			st.number_input('number', key='passengers', min_value=1, max_value=9, value="min", step=1, format='%d')

		with c6:
			st.selectbox("To", ('Economy', 'Business', 'First'), key='cabin')

#		with c7:
		st.form_submit_button('Submit', on_click=flight_submit)

	if isinstance(str(st.session_state.json_data), str):
		return st.session_state.json_data
	else:
		return None

#	st.text_area('Additional Information', height=200, value='I want to visit as many places as possible! (respect time)', key='additional_information')

#	user_input = st.text_input("Enter the Place You Want to Visit", key="input2")
#	if st.button("Send", key="button2"): 
#		if user_input:
#			return get_response(TOUR_GUIDE_SYSTEM, user_input)
#		else:
#			return "NULL"

def hotel_submit():

	destination = st.session_state.destination_hotel
	destination_lat = worldcities.loc[worldcities['city_long'] == destination]['lat'][0]
	destination_lon = worldcities[worldcities['city_long'] == destination]['lng'][0]

	print(destination_lat, destination_lon)

	request_data = {'lat': destination_lat, 'lon': destination_lon}

	user_input = json.dumps(request_data)
	response = requests.post("http://localhost:3333/hotel_list", json=user_input)

	data = response.content
	print(data)


def hotel_search_section():

	st.title("Hotel Search")
	if 'json_data' not in st.session_state:
		st.session_state.json_data = ''

	if 'output' not in st.session_state:
		st.session_state['output'] = '--'

	st.subheader('Find the place to stay!')

	with st.form(key='hotel_form'):
		c1, c2, c3, c4 = st.columns(4)

		with c1:
			st.selectbox("Destination", worldcities['city_long'], key='destination_hotel', index=None, placeholder='Where are you going')

		with c2:
			st.date_input('Check-In Date', value=now_date + timedelta(days=1), key='check_in_date')

		with c3:
			st.date_input('Check-Out Date', value=now_date + timedelta(days=2), key='check_out_date')

		with c4:
			st.number_input('Adults', key='adults', min_value=1, max_value=4, value="min", step=1, format='%d')

#		with c7:
		st.form_submit_button('Submit', on_click=hotel_submit)

	if isinstance(str(st.session_state.json_data), str):
		st.write(str(st.session_state.json_data))

def visa_info_section():
	st.title("Visa Info")
	user_input = st.text_input("Enter the Place You Want to Visit", key="input4")
	if st.button("Send", key="button4"): 
		if user_input:
			return get_response(TOUR_GUIDE_SYSTEM, user_input)
		else:
			return "NULL"

def tour_guide_section():
	st.title("Tour Guide Assistant")
	user_input = st.text_input("Enter the Place You Want to Visit", key="input5")
	if st.button("Send", key="button5"): 
		if user_input:
			return get_response(TOUR_GUIDE_SYSTEM, user_input)
		else:
			return "NULL"


def contact_section():
	st.title("Contact Us")
	user_input = st.text_input("Enter the Place You Want to Visit", key="input6")
	if st.button("Send", key="button6"): 
		if user_input:
			return get_response(TOUR_GUIDE_SYSTEM, user_input)
		else:
			return "NULL"

def about_section():
	st.title("About")
	user_input = st.text_input("Enter the Place You Want to Visit", key="input7")
	if st.button("Send", key="button7"): 
		if user_input:
			return get_response(TOUR_GUIDE_SYSTEM, user_input)
		else:
			return "NULL"


def show(output):
	if output: 
		st.markdown(output.content)
	elif output=="NULL":
		st.markdown("Please Enter Some Text")


def main():

	tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Travel Planner", "Flight", 'Hotel', 'Visa', 'Tour Guide', 'Contact', 'About'])

	with tab1:
		output = trip_planner_section()
		if output:
			out_res = output.content
#			st.write(out_res)

			st.write(json.loads(out_res))
			
#			st.write(json.loads(output))
#			itinerary = ta.itinerary_days(output)
			try:
				show_itinerary(output)
			except:
				pass
#			return output
#			show(itinerary)
		else:
			st.write('')

#		itinerary = ta.itinerary_days(output)
#		return output
#		show(output)

	with tab2:
		output = flight_search_section()
		if output:
			st.write(output)
#			itinerary = ta.itinerary_days(output)
#			return output
#			show(itinerary)
		else:
			st.write('')

#		st.subheader('Trip Schedule')
#		st.write(st.session_state.output)
#		show(output)

	with tab3:
		output = hotel_search_section()
		show(output)

	with tab4:
		output = visa_info_section()
		show(output)

	with tab5:
		output = tour_guide_section()
		show(output)

	with tab6:
		output = contact_section()
		show(output)

	with tab7:
		output = about_section()
		show(output)


#	output = new_trip_form()
#	if output:
#		st.write(output.content)
#		itinerary = ta.itinerary_days(output)
#		return output
#	else:
#		st.write('')



if __name__ == "__main__":
	main()
