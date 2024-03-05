import urllib.request
import json
import os
import ssl

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# Request data goes here
# The example below assumes JSON formatting which may be updated
# depending on the format your endpoint expects.
# More information can be found here:
# https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
data =  {
  "Inputs": {
    "input1": [
      {
        "Issued_date": "2000-01-29 09:10:00",
        "Community_Name": "Austin",
        "Sector": "Other W Side",
        "Side": "West Side",
        "Hardship_Index": 73.0,
        "Per_capita_income": 73.0,
        "Percent_unemployed": 22.6,
        "Percent_without_diploma": 24.4,
        "Percent_households_below_poverty": 28.6,
        "Neighborhood": "A3",
        "Ward": 29,
        "Tract": 252101,
        "ZIP": 60644,
        "Police_District": 15,
        "Plate_Type": "PAS",
        "License_Plate_State": "IL",
        "Unit_ID": 15,
        "Violation_ID": 123,
        "PaymentIsOutstanding": 1
      },
      {
        "Issued_date": "2014-08-21 09:31:00",
        "Community_Name": "Chatham",
        "Sector": "Other S/SE/SW Side",
        "Side": "Far Southeast Side",
        "Hardship_Index": 73.0,
        "Per_capita_income": 73.0,
        "Percent_unemployed": 73.0,
        "Percent_without_diploma": 14.5,
        "Percent_households_below_poverty": 27.8,
        "Neighborhood": "C1",
        "Ward": 8,
        "Tract": 440102,
        "ZIP": 60619,
        "Police_District": 6,
        "Plate_Type": "PAS",
        "License_Plate_State": "IL",
        "Unit_ID": 498,
        "Violation_ID": 6,
        "PaymentIsOutstanding": 0
      },
      {
        "Issued_date": "2015-04-10 19:41:00",
        "Community_Name": "West Town",
        "Sector": "West Town",
        "Side": "West Side",
        "Hardship_Index": 73.0,
        "Per_capita_income": 73.0,
        "Percent_unemployed": 6.6,
        "Percent_without_diploma": 12.9,
        "Percent_households_below_poverty": 14.7,
        "Neighborhood": "WP3",
        "Ward": 1,
        "Tract": 241400,
        "ZIP": 60622,
        "Police_District": 14,
        "Plate_Type": "PAS",
        "License_Plate_State": "IL",
        "Unit_ID": 502,
        "Violation_ID": 44,
        "PaymentIsOutstanding": 0
      }
    ]
  },
  "GlobalParameters": {}
}

body = str.encode(json.dumps(data))

url = 'http://172.168.200.88:80/api/v1/service/parkdemoep/score'
# Replace this with the primary/secondary key or AMLToken for the endpoint
api_key = ''
if not api_key:
    raise Exception("A key should be provided to invoke the endpoint")


headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)

    result = response.read()
    print(result)
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(error.read().decode("utf8", 'ignore'))
