import socket
import getopt
import sys

#UDP_IP="192.168.7.255"
destination_port = 2430
#scene_number="00"
  

try :
  optlist, args = getopt.getopt( sys.argv[1:], 'd:s:h')
  ipv6 = 0
  destination_ip = ""
except getopt.GetoptError:
  print "Errror in option input"
  sys.exit(2)
        
for opt, arg in optlist :
  if opt in "-d" :
    destination_ip = arg
  elif opt in "-s" :
    scene_number = arg #= hex( arg )
  elif opt in "-h" :
    help()
  if destination_ip == ""  :
    print "The -d DESTINATION_IP switch is required"
    sys.exit(2)

if __name__ == "__main__" :

  sceneint = int(scene_number)  
  scenehex = str(hex(sceneint)[2:].zfill(2))

  message="53697564695f37426d00".decode('hex') +  scenehex.decode('hex') + "000000010000000000".decode('hex')

  print "UDP target IP:", destination_ip
  print "hex scene: ", scenehex
  print "command:", message
  print "compare:", "53697564695f37426d0001000000010000000000".decode('hex')
  sock = socket.socket( socket.AF_INET6 if ipv6 else socket.AF_INET, socket.SOCK_DGRAM)
  sock.sendto( message, (destination_ip, destination_port) ) # destination IP address must be a string, not a packeted IP address


