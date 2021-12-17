import requests
import urllib.parse

KEY     = "DMCJYJVvkr0qvlVTpvWsZGxuALk9U7HR"
API     = "https://www.mapquestapi.com/directions/v2/route?"

while True:
    orig = input('Origin location: ')
    if orig == 'q' or orig == 'quit':
        break
    dest = input('Destination: ')
    if orig == 'q' or orig == 'quit':
        break
    
    url     = API + urllib.parse.urlencode({'key':KEY, "from":orig, "to": dest})
    json_data = requests.get(url).json()

    print(f"url: {url}")
    # print(json_data)
    json_status = json_data['info']['statuscode']

    if json_status == 0:
        print(f"API Status: {json_status} = A succefully route call. \n")
        print("=============================================")
        print(f"Directions from {orig} to {dest}")
        print(f"Trip duration   {json_data['route']['formattedTime']}")
        print("Kilometers:    "  + str("{:.2f}".format((json_data["route"]["distance"])*1.61)))
        print(f"Fuel Used (Ltr):  " + str("{:.2f}".format(json_data['route']['fuelUsed']*3.78)))
        print("=============================================\n")
        
        
        


