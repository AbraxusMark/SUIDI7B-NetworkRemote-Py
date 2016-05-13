import requests, json
from requests.auth import HTTPBasicAuth
import socket
import getopt
import sys
import datetime
import time
import subprocess
import random

#user poll id & account
pollkey = 'IU68fUaUjy58yWS'
usr="support@abraxuslighting.co.uk"
pas="chopin"

url='https://www.polleverywhere.com/multiple_choice_polls/' + pollkey  + '.json'
resurl='https://www.polleverywhere.com/multiple_choice_polls/' + pollkey + '/results'

#port for UDP packet to SUIDI 7B / ue7
destination_port = 2430

#mark in log the time
print ("**********  Run at:", datetime.datetime.now())

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
    print ("Connection Error, exiting")
#reboot for resiliance?
    #subprocesscall(['shutdown', '-r', 'now'])
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
#    print(resultvote, option['value'], resulthistory)
    
    if int(resultvote) > int(resulthistory):
      optionname = option['value']
      resulthistory=resultvote
      resultwinner=resultsorder
    
  #check for a winner  
  if resultwinner == 0:
    print 'NO WINNER!!! (No votes?) choosing random'
    resultwinner=random.randint(1,5)
    print ('Winner is', resultwinner, 'chosen at random')
  else:
    print ('Winner is', resultwinner, optionname)
      
  #command SUIDI7B via a udp packet
  sceneint = int(resultwinner)  
  scenehex = str(hex(sceneint)[2:].zfill(2))

  message="53697564695f37426d00".decode('hex') +  scenehex.decode('hex') + "000000010000000000".decode('hex')

#  print ("UDP target IP:", destination_ip)
  print ("hex scene: ", scenehex)
#  print ("command:", message)
#  print ("compare:", "53697564695f37426d0001000000010000000000".decode('hex'))
  sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
  sock.sendto( message, (destination_ip, destination_port) ) # destination IP address must be a string, not a packeted IP address

  #play a the song#
  subprocess.call(['mpc', 'play', scenehex])

  #clear the poll
  
  response = requests.delete(resurl, auth=requests.auth.HTTPBasicAuth(usr, pas), headers = {'Accept': 'application/json', 'Content-Type': 'application/json' })

  if response.history:
    print "Delete request was redirected"
    for resp in response.history:
        print resp.status_code, resp.url
    print "Final destination:"
    print response.status_code, response.url
  else:
    print "Request was not redirected"

    