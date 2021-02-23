import math  # Imports the math library in order to use the sqrt function
import sys  # Imports the system library in order to stop the programme if needed

def printL(list):  # A better way to display both the IP and the Mask of the network in their binary forms
  string = ""
  for i in range(4):
    for j in range(8):
      string += str(list[i][j])
    if i != 3:
      string+= "."
  return string


def ConvBinary(byte, bits):  # This function converts every part of the IP to the binary system
    byte = int(byte)
    binary = [0] * bits
    index = len(binary) - 1
    while True:
        quotient, remainder = divmod(byte, 2)
        byte = quotient
        binary[index] = remainder
        index -= 1
        if quotient == 0:
            break
    return binary

def ConvDecimal(byte,bits):  # Converts binary to decimal
  decimal = 0
  for i in range(bits,0,-1):
    decimal+= (2 **(bits - i)) * byte[i - 1]

  return decimal


def FindClass(FirstByte):  # Detects the IP's Class based on the first byte
    if FirstByte < 127:
        return 'A'
    elif FirstByte < 191:
        return 'B'
    elif FirstByte < 223:
        return 'C'


def IPMask(CIDR):  # returns the Mask of the IP provided by the user
    CIDRList = [[0 for i in range(8)] for j in range(4)]
    column = 0
    row = 0
    while CIDR > 0:
        CIDRList[row][column] = 1
        CIDR -= 1
        column += 1
        if column == len(CIDRList[0]):
            row += 1
            column = 0

    return CIDRList


def CalculateBitsNeeded(Subnets,CIDR):  # Calcuates the amount of bits the subnets will have to use at the last byte of the IP
  if Subnets == "C":
      response = int(input("How many computers would you like to have per subnet? "))
      i = 0
      power = 1
      while response >= power:
        power *= 2
        i += 1
      hostid = 32 - CIDR - i
      return hostid
      
  elif Subnets == "S":
        response = int(input("How many subnets would you like your network to have? "))
        i = 0
        power = 1
        while response >= power:
          power *= 2
          i += 1
        return i


def CalculateSubnets(Subnets):  # Prints all the subnets and the length of the IPs available
    for i in range(2 ** Subnets):
        gang = Subnets - len(format(i, 'b'))
        print gang * "0" + format(i, 'b') + " " + (8 - Subnets) * "0" + " | " + str(subnetsList[(8 - Subnets) - 1] * i)
        print gang * "0" + format(i, 'b') + " " + (8 - Subnets) * "1" + " | " + str(
            (subnetsList[(8 - Subnets) - 1] * (i + 1)) - 1)
        print "---------------"


subnetsList = [2, 4, 8, 16, 32, 64, 128, 256]  # from 2^1 to 2^8, these numbers are needed for the CalculateBitsNeeded function
IP = raw_input("Please type in the IP: ")  # User types in the IP of the network
IP = IP.split(".")  # Splits every part of the IP into a list
for byte in IP:  # Checks if any part of the ip is out of boundaries
    if int(byte) < 0 or int(byte) > 255:
        print "One or more parts of the IP were outside of the limit (0, 255), therefore the programme stopped!"
        sys.exit(0)

CIDR = int(input("Please type in the CIDR: "))  # User types in the CIDR for the Mask (amount of 1s the mask with have)
while CIDR < 0 or CIDR > 32:  # Checks if the CIDR is out of boundaries (there are only 32 digits in the IP, the mask cannot extend them)
    print "The CIDR you entered was not valid (0, 32)!"
    CIDR = int(input("Please type in the CIDR: "))

Subnets = raw_input("Would you like to split the network based on the amount of computers/subnet (C) "  # User selects how he wants to split the network, based on the amount of subnets
                    "or based on the amount of Subnets (S): ").upper()                                  # or based on computers per subnet
while Subnets not in ['C', 'S']:  # Checks if the option the user gave was valid
    print "Your option was invalid, please try again."
    Subnets = raw_input("Would you like to split the network based on the amount of computers/subnet (C) "
                        "or based on the amount of Subnets (S): ").upper()

Subnets = CalculateBitsNeeded(Subnets,CIDR)  # Calculates the amount of bits that will be needed in order to print out all the subnets

for i in range(len(IP)):  # Converts each byte of the IP from decimal to binary
    IP[i] = ConvBinary(IP[i], 8)
print "IP (Binary): " + printL(IP)  # Prints the IP with its binary form
print "Mask: " + printL(IPMask(CIDR))  # Prints the Mask of the network
print "Class: " + str(FindClass(ConvDecimal(IP[0],8)))  # Detects and prints the Class of the network based on IP's first byte
CalculateSubnets(Subnets)  # Prints all the subnets created based on user's options

# CREDITS
# https://github.com/ohmylawdy
# https://github.com/Nektarios