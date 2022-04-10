import time, json, requests
from requests.sessions import HTTPAdapter

# 2. Complete la declaración if para solicitar al usuario el token de acceso de Webex Teams.
choice = input ("¿Desea usar el token de Webex codificado? (y/n) ")

if choice == "N" or choice == "n":
    accessToken = "Bearer " + input("Ingrese su token de acceso ")
else:
	accessToken = "Bearer YWVkZGNkNzAtMmVhOC00MDEyLTllMTUtNzg4ZTEzMWRhZDkwYzY4ZjU5OGQtYTJh_P0A1_a2846766-4793-4366-afe1-303099abecc2"

# 3. Proporcione la URL de la API de sala de Webex.
r = requests.get ("https://webexapis.com/v1/rooms",
                    headers = {"Authorization": accessToken}
                )

#####################################################################################
# NO EDITAR NINGÚN BLOCK CON r.status_code
if not r.status_code == 200:
    raise Exception ("Respuesta incorrecta de la API de Webex Teams. Status code: {} Text: {}" .format (r.status_code, r.text))
######################################################################################

# 4. Cree un bucle para imprimir el tipo y el título de cada sala.
print ("Lista de salas:")
rooms = r.json () ["items"]
for room in rooms:
    print(room["type"], room["title"])

#######################################################################################
# BUSCAR SALA DE EQUIPOS DE WEBEX PARA MONITOREAR
# - Busca el nombre de sala proporcionado por el usuario.
# - Si se encuentra, imprima el mensaje "found", de lo contrario imprime el error.
# - Almacena valores para su uso posterior por bot.
# NO EDITAR CÓDIGO EN ESTE BLOQUE
#######################################################################################

while True:
    roomNameToSearch = input ("¿Qué sala debe ser monitoreada para mensajes /location? ")
    roomIDToGetMessages = None
    
    for room in rooms:
        if(room["title"].find(roomNameToSearch) != -1):
            print ("Found rooms with the word " + roomNameToSearch)
            print (room ["title"])
            roomIDToGetMessages = room ["id"]
            roomTitleTogetMessages = room ["title"]
            print ("sala encontrada:" + roomTitleTogetMessages)
            break

    if (roomIDToGetMessages == None):
        print ("Lo siento, no encontré ninguna sala con" + roomNameToSearch +".")
        print ("Inténtelo de nuevo...")
    else:
        break

######################################################################################
# CÓDIGO BOT DE WEBEX TEAMS
# Inicia el bot de Webex para escuchar y responder a los mensajes /location.
######################################################################################

while True:
    time.sleep (1)
    getParameters = {
                            "roomId": roomIDToGetMessages,
                            "max": 1
                    }
# 5. Proporcione la URL de la API de mensajes de Webex.
    r = requests.get ("https://webexapis.com/v1/messages", 
                         params = getParameters, 
                         headers = {"Authorization": accessToken}
                    )

    if not r.status_code == 200:
        raise Exception ("Respuesta incorrecta de la API de Webex Teams. Status code: {} Texto: {}" .format (r.status_code, r.text))
    
    json_data = r.json ()
    if len (json_data ["items"]) == 0:
        raise Exception ("No hay mensajes en la sala.")
    
    messages = json_data ["items"]
    message = messages [0] ["text"]
    print("Received message: " + message)
    
    if message.find ("/") == 0:
        location = message [1:]
# 6. Proporcione la clave de consumidor de la API de MapQuest.
        MapsaPigetParameters = { 
                                "location": location, 
                                "key": "DMCJYJVvkr0qvlVTpvWsZGxuALk9U7HR"
                               }
# 7. Proporcione la URL de la API de direcciones de MapQuest.
        r = requests.get("https://www.mapquestapi.com/geocoding/v1/address", 
                             params = MapsaPigetParameters
                        )
        json_data = r.json()

        if not json_data ["info"] ["statuscode"] == 0:
            raise Exception ("Respuesta incorrecta de MapQuest API. Status code: {}" .format (r.statuscode))

        locationResults = json_data ["results"] [0] ["providedLocation"] ["location"]
        print ("Ubicación: " + locationResults)
# 8. Proporcione los valores clave de MapQuest para obtener la latitud y la longitud.
        locationLat = json_data ["results"] [0] ["locations"] [0] ["latLng"] ["lat"]
        locationLng = json_data ["results"] [0] ["locations"] [0] ["latLng"] ["lng"]
        print ("Localización coordenadas GPS:" + str (locationLat) + "," + str (locationLng))
        
        IssaPigetParameters = { 
                                "lat": locationLat, 
                                "lon": locationLng
                              }
# 9. Proporcione la URL de la API de tiempos de paso de ISS.
        r = requests.get("http://api.open-notify.org/iss-pass.json", 
                             params = IssaPigetParameters
                        )

        json_data = r.json()

        if not "response" in json_data:
            raise Exception ("Respuesta incorrecta de la API open-notify.org. Status code: {} Texto: {}" .format (r.status_code, r.text))
# 10. Proporcione los valores clave ISS del tiempo de espera y duración.
        risetimeinEpochSeconds = json_data ["response"] [0] ["risetime"]
        durationInSeconds = json_data ["response"] [0] ["duration"]
# 11. Convierta el valor de risetime epoch en una fecha y hora legible para humanos.
        risetimeInFormattedString = time.strftime( "%Y-%m-%d %H:%M:%S", time.gmtime(risetimeinEpochSeconds))
# 12. Complete el código para formatear el mensaje de respuesta.
# Ejemplo de resultado de un mensaje de respuesta: En Austin, Texas, la ISS sobrevolará el jue Jun 18 18:42:36 2020 durante 242 segundos.
        responseMessage = "In {} the ISS will fly over on {} for {} seconds.".format(location, risetimeInFormattedString, durationInSeconds)

        print ("Envío a Webex: " +responseMessage)
# 13. Complete el código para publicar el mensaje en la sala de Webex. 
        HttpHeaders = { 
                             "Authorization": accessToken,
                             "Content-Type": "application/json"
                           }
        PostData = {
                            "roomId": roomIDToGetMessages,
                            "text": responseMessage
                        }

        r = requests.post ("https://webexapis.com/v1/messages", 
                              data = json.dumps (PostData), 
                              headers= HttpHeaders
                         )
        if not r.status_code == 200:
            raise Exception ("Respuesta incorrecta de la API de Webex. Status code: {} Text: {}" .format (r.status_code, r.text))
