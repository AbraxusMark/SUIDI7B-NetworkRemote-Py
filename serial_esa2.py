
import socket
import getopt
import sys
import datetime
import serial

#port for all SUIDIs
destination_port = 2430 

#mark in log the time
print ("*******  Run at:", str(datetime.datetime.now()))

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
    #open serial
    
    ser = serial.Serial(
    port='/dev/ttyACM0',\
    baudrate=115200,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=10)
    
  except:
    print ("Serial Connection Error")
    sys.exit(2)
    #exit!
    
  stepvalue = 0
    
  while True:
    
    line=ser.readline()
    if len(line)>1:      
      if line[:1] == "2":
        stepvalue = int(line[3:])
    #else:
      #print "timeout"
      
    if stepvalue > 50:
      sceneint = 1
      if stepvalue > 250:
        sceneint = 2
      if stepvalue > 320:
        sceneint = 3
      if stepvalue > 400:
        sceneint = 4
      
      print stepvalue
      print sceneint
      #command SUIDI7B via a udp packet
      
      scenehex = str(hex(sceneint)[2:].zfill(2)) #create byte value to insert in message

      message="53697564695f37426d00".decode('hex') +  scenehex.decode('hex') + "000000010000000000".decode('hex')

      #print ("UDP target IP:", destination_ip)
      #print ("hex scene: ", scenehex)
      #print ("command:", message)
      #print ("compare:", "53697564695f37426d0001000000010000000000".decode('hex'))
      sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM)
      sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
      sock.sendto( message, (destination_ip, destination_port) ) # destination IP address must be a string, not a packeted IP address
    
    stepvalue=0
    