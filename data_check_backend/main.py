from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes in the app

out = {
    "EU" : {},
    "ASIA" : {},
    "USA" : {},
    "AU" : {},
    "CH" : {},
    "CN" : {}
}
# @app.route('/read_csv/<path:file_path>', methods=['GET'])

# @app.route('/', methods=['GET'])
# def read_csv():
    
#   # Read the CSV file using pandas

def get_data_for_region_mode(region_='USA', mode_='d1', check_function_='check_correlation_less_than_1'):
  
  
  # Read the CSV file using pandas
  file_path = '../csv_files/failed_data_check_d1_EU_20240123.csv'
  file_name_with_extension = os.path.basename(file_path)
  file_name = os.path.splitext(file_name_with_extension)[0]

  arr = file_name.split("_")
  region = arr[4]
  delay = arr[3]
  date = arr[5]

  df = pd.read_csv(file_path)

  for index, row in df.iterrows():
    varname, failed_checks = row['varname'], row['failed_checks']
    # out[region][delay][date][varname][failed_checks]=1
    out.setdefault(region, {}).setdefault(delay, {}).setdefault(failed_checks, {}).setdefault(varname, {})[date] = 1

  # Convert the DataFrame to a list of dictionaries
  # data = df.to_dict(orient='records')
  # print(out)
  # out = out[region_][mode_]
  out.setdefault(region_, {}).setdefault(mode_, {}).setdefault(check_function_, {})
  json_string = json.dumps(out[region_][mode_][check_function_])

  # Return the data as JSON
  return jsonify({"data": json_string})

@app.route('/check_data/', methods=['GET'])
def read_csv():

  region_ = request.args.get('region')
  delayMode = request.args.get('delayMode')
  checkFunction = request.args.get('checkFunction')


  print(region_, ", ", delayMode)

  output = get_data_for_region_mode(region_, delayMode, checkFunction)
  return output



# def read_csv(file_path):
# @app.route('/check_data/', methods=['GET'])
# def read_csv():
    
#   # Read the CSV file using pandas
#   file_path = '../csv_files/failed_data_check_d1_EU_20240123.csv'
#   file_name_with_extension = os.path.basename(file_path)
#   file_name = os.path.splitext(file_name_with_extension)[0]

#   arr = file_name.split("_")
#   region = arr[4]
#   delay = arr[3]
#   date = arr[5]

#   df = pd.read_csv(file_path)

#   for index, row in df.iterrows():
#     varname, failed_checks = row['varname'], row['failed_checks']
#     # out[region][delay][date][varname][failed_checks]=1
#     out.setdefault(region, {}).setdefault(delay, {}).setdefault(varname, {}).setdefault(date, {})[failed_checks] = 1



#   # Convert the DataFrame to a list of dictionaries
#   # data = df.to_dict(orient='records')
#   print(out)

#   json_string = json.dumps(out)

#   # Return the data as JSON
#   return jsonify({"data": json_string})


if __name__ == '__main__':
    app.run(debug=True)
