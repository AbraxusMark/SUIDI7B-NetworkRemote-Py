import requests, json
from requests.auth import HTTPBasicAuth
import socket
import getopt
import sys
import datetime


pollkey = 'IU68fUaUjy58yWS'

url='http://api.polleverywhere.com/multiple_choice_polls/' + pollkey  + '.json'
resurl='http://api.polleverywhere.com/multiple_choice_polls/' + pollkey + '/results.json'
usr='support@abraxuslighting.co.uk'
pas='chopin'

destination_port = 2430

print ("Run at:", datetime.datetime.now())

try :
  optlist, args = getopt.getopt( sys.argv[1:], 'd:h')
  destination_ip = ""
except getopt.GetoptError:
  print ("Errror in option input")
  sys.exit(2)
        
for opt, arg in optlist :
  if opt in "-d" :
    destination_ip = arg
  elif opt in "-h" :
    help()
  if destination_ip == ""  :
    print ("The -d DESTINATION_IP switch is required")
    sys.exit(2)

if __name__ == "__main__" :


  try:
    response = requests.get(url, auth=HTTPBasicAuth(usr, pas), headers = {'accept': 'application/json', 'Content-Type': 'application/json' })

    data = response.json()
    
  except requests.exceptions.ConnectionError as e:
    print ("Connection Error")
    sys.exit(2)
    #exit!
  if response.history:
      print ("Request was redirected")
  else:
      print( "Request was not redirected")
      
  #now we should have the json
  dataoptions =  data['options']  #narrow the reply.
  resultsorder = 0
  resulthistory = 0
  resultwinner = 0
	

  #find the winner
  for option in dataoptions:
    resultsorder+=1
    resultvote = option['results_count']
    print(resultvote, option['value'], resulthistory)
    
    if int(resultvote) > int(resulthistory):
      optionname = option['value']
      resulthistory=resultvote
      resultwinner=resultsorder
    
  #check for a winner  
  if resultwinner == 0:
    print('NO WINNER!!! (No votes?) Exiting without scene change')
    sys.exit(2)

  print ('Winner is', resultwinner, optionname)
      
  #command SUIDI7B via a udp packet
  sceneint = int(resultwinner)  
  scenehex = str(hex(sceneint)[2:].zfill(2))

  message="53697564695f37426d00".decode('hex') +  scenehex.decode('hex') + "000000010000000000".decode('hex')

  print ("UDP target IP:", destination_ip)
  print ("hex scene: ", scenehex)
  print ("command:", message)
  print ("compare:", "53697564695f37426d0001000000010000000000".decode('hex'))
  sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
  sock.sendto( message, (destination_ip, destination_port) ) # destination IP address must be a string, not a packeted IP address
    
  #clear the poll
  response = requests.delete(resurl, auth=HTTPBasicAuth(usr, pas), headers = {'accept': 'application/json', 'Content-Type': 'application/json' })