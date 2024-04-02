from flask import Flask,jsonify, send_file
import csv
import requests
from bs4 import BeautifulSoup
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def export_csv():
    # Create a StringIO object to store CSV data in memory
    csv_data = BytesIO()


    try:
        url = 'https://en.wind-turbine-models.com/turbines/23-areva-m5000-116'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # get model
        turbine = soup.find('h1', class_='page-header').text.strip()
        # Find the <div> element with the specified classes
        datasheet = soup.find('div', id='datasheet')
        # List to store extracted data
        data_list = []
        if datasheet:
            sections = datasheet.find_all('div', class_='TabContent')
            for section in sections:
                section_name = section.find_previous_sibling('h3').text.strip()
                attributes = section.find_all('div', class_='row')
                section_data = {}
                for attribute in attributes:
                    key = attribute.find(class_='col-left').text.strip()
                    value = attribute.find(class_='col-right').text.strip()
                    section_data[key] = value
                data_list.append({section_name: section_data})
        # Initialize turbine data dictionary
        turbines = {
            'turbine_type': None,
            'id': None,
            'turbine_id': None,
            'manufacturer': None,
            'name': None,
            'nominal_power': None,
            'rotor_diameter': None,
            'rotor_area': None,
            'hub_height': None,
            'max_speed_drive': None,
            'wind_class_iec': None,
            'wind_zone_dibt': None,
            'power_density': None,
            'power_density_2': None,
            'calculated': None,
            'has_power_curve': None,
            'has_cp_curve': None,
            'has_ct_curve': None
        }
        # # Split the text by space
        parts = turbine.split()
        if len(parts) >= 2:
            manufacturer = parts[0]  # First part is the name
            model = " ".join(parts[1:])
            turbines["manufacturer"] = manufacturer
            turbines["name"] = model
        if datasheet:
            sections = datasheet.find_all('div', class_='TabContent')
            for section in sections:
                # Extract section name
                turbine_type = section.find_previous_sibling('h3').text.strip()
                turbines['turbine_type'] = turbine_type
                # Find all rows within the section
                rows = section.find_all('div', class_='row')
                for row in rows:
                    key = row.find(class_='col-left').text.strip()
                    value = row.find(class_='col-right').text.strip()
                    # Map attributes to columns
                    if key == 'ID:':
                        turbines['id'] = value
                    elif key == 'Rated power:':
                        turbines['nominal_power'] = value
                    elif key == 'Diameter:':
                        turbines['rotor_diameter'] = value
                    elif key == 'Swept area:':
                        turbines['rotor_area'] = value
                    elif key == 'Hub height:':
                        turbines['hub_height'] = value
                    elif key == 'Rotor speed, max:':
                        turbines['max_speed_drive'] = value
                    elif key == 'Wind class (IEC):':
                        turbines['wind_class_iec'] = value
                    elif key == 'Wind zone (DIBt):':
                        turbines['wind_zone_dibt'] = value
                    elif key == 'Power density 1:':
                        turbines['power_density'] = value
                    elif key == 'Power density 2:':
                        turbines['power_density_2'] = value
                    elif key == 'Calculated:':
                        turbines['calculated'] = value
                    elif key == 'Has power curve:':
                        turbines['has_power_curve'] = value
                    elif key == 'Has Cp curve:':
                        turbines['has_cp_curve'] = value
                    elif key == 'Has Ct curve:':
                        turbines['has_ct_curve'] = value
        title = soup.title.string
        # Convert the content of the container <div> to JSON
        output = {
            "title": title,
            "turbine": turbine,
            "turbines": turbines,
            "data": data_list,
        }

        data = [
            [
            'turbine_type',
            'id',
            'turbine_id',
            'manufacturer',
            'name',
            'nominal_power',
            'rotor_diameter',
            'rotor_area',
            'hub_height',
            'max_speed_drive',
            'wind_class_iec',
            'wind_zone_dibt',
            'power_density',
            'power_density_2',
            'calculated',
            'has_power_curve',
            'has_cp_curve',
            'has_ct_curve'
            ],
            [value for value in turbines.values()]
        ]



        # Encode data to bytes and write to CSV
        encoded_data = '\n'.join([','.join(map(str, row)) for row in data]).encode()
        csv_data.write(encoded_data)
        # Set StringIO object's file pointer to the beginning
        csv_data.seek(0)


        # Return the CSV file as a downloadable attachment with the specified filename
        return send_file(csv_data,
                        as_attachment=True,
                        download_name='output.csv',
                        mimetype='text/csv')

        return jsonify(output)

    except Exception as e:
        return e

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000, debug=True)