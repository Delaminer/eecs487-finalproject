import requests

# SOME EXAMPLEs
# Duplicate: 28205 -> original post 17339
# Duplicate: 33553 -> original post 17243
id = "28205"

# api-endpoint
# URL = "https://api.stackexchange.com/2.3/questions/1/linked?order=desc&sort=activity&site=stackoverflow"
# URL = "https://api.stackexchange.com/2.3/questions/" + id + "/related?order=desc&sort=activity&site=stackoverflow"
URL =  "https://api.stackexchange.com/2.3/questions/" + id + "?order=desc&sort=activity&site=linguistics&filter=!6Wfm_gTNExWJv"
# location given here
r = requests.get(url = URL)
  
# extracting data in json format
data = r.json()
  
print("This question is a duplicate:", data["items"][0]["closed_reason"] == "Duplicate")
print("This question is a duplicate:", data["items"][0]["closed_details"]["reason"] == "Duplicate")
print(data["items"][0]["closed_details"]["original_questions"])

  
# # extracting latitude, longitude and formatted address 
# # of the first matching location
# latitude = data['results'][0]['geometry']['location']['lat']
# longitude = data['results'][0]['geometry']['location']['lng']
# formatted_address = data['results'][0]['formatted_address']
  
# # printing the output
# print("Latitude:%s\nLongitude:%s\nFormatted Address:%s"
#       %(latitude, longitude,formatted_address))