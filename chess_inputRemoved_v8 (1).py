import pandas as pd
import numpy as np
from json import *
from datetime import datetime

#Hard-coded data for output represents the account data 
#for banned accounts from chess.com

import requests
import sys
from csv import writer
chess = pd.read_csv('chess.csv')
chess=chess.replace(0,np.nan)
W=np.array(chess["Blitz Rating"])
r1=str(round(np.mean(W),0))
X=np.array(chess["Bullet Rating"])
r2=str(round(np.mean(X),0))
x=np.array(chess["Rapid Rating"])
r3=str(round(np.mean(x),0))
Y=np.array(chess["Accuracy"])
r4=str(round(np.mean(Y),0))
Z=np.array(chess["Account Age (Months)"])
r5=str(round(np.mean(Z),0))
y=np.array(chess["Bullet Win Rate"])
r6=str(round(np.mean(y),0))
z=np.array(chess["Blitz Win Rate"])
r7=str(round(np.mean(z),0))
Q=np.array(chess["Rapid Win Rate"])
r8=str(round(np.mean(Q),0))

try:
    username = sys.argv[1]
except:
    print("Usage: usage chessapi.py <username>")
    sys.exit(0)

req = 'https://api.chess.com/pub/player/' + username + '/stats'
req2 = 'https://api.chess.com/pub/player/' + username

resp = requests.get(req)
print(type(resp))
if resp.status_code != 200:
    # This means something went wrong.
    print("Oopsie")
else:
    print("User stats: ", resp.json())
    
resp2 = requests.get(req2)
if resp2.status_code != 200:
    # This means something went wrong.
    print("Oopsie 2")
else:
    print("Profile: ", resp2.json())

userStats = loads(dumps(resp.json()))
userProfile = loads(dumps(resp2.json()))

currentDate = datetime.utcnow()
joinDate = datetime.utcfromtimestamp(userProfile["joined"])
diff = joinDate - currentDate
accountage = diff.days/-30
print("Age of Account in Months: " + str(accountage))

if "chess_rapid" in userStats:
    rapidrating= userStats["chess_rapid"]["last"]["rating"]
    print("Rapid Rating: " + str(rapidrating))
    playaccuracy=input("Please enter the accuracy of their play. If you did not play this time control, enter '0'\n")
    #print(str(playaccuracy))
    winrate=userStats["chess_rapid"]["record"]["win"]/(userStats["chess_rapid"]["record"]["win"]+userStats["chess_rapid"]["record"]["loss"]+userStats["chess_rapid"]["record"]["draw"])
    print("Win Rate: " + str(winrate))
    if int(rapidrating)>float(r3) and float(accountage)<float(r5) and float(playaccuracy)>float(r4) or float(winrate)>float(r8):
        print('Sus!')
    elif int(rapidrating)>float(r3) and float(accountage)<float(r5) and float(winrate)>float(r8) or float(playaccuracy)>float(r4):
        print('Sus!')
    else:
        print('Never mind.')
else:
    rapidrating = 0
    winrate = 0
	
if "chess_blitz" in userStats:
    blitzrating=userStats["chess_blitz"]["last"]["rating"]
    print("Blitz Rating: " + str(blitzrating))
    blitzwinrate=userStats["chess_blitz"]["record"]["win"]/(userStats["chess_blitz"]["record"]["win"]+userStats["chess_blitz"]["record"]["loss"]+userStats["chess_blitz"]["record"]["draw"])
    print("Blitz Win Rate: " + str(winrate))
    if int(blitzrating)>float(r1) and float(accountage)<float(r5) and float(playaccuracy)>float(r4) or float(blitzwinrate)>float(r7):
        print('Sus!')
    elif int(blitzrating)>float(r1) and float(accountage)<float(r5) and float(blitzwinrate)>float(r7) or float(playaccuracy)>float(r4):
        print('Sus!')
    else:
        print('Never mind.')
else:
    blitzrating = 0
    blitzwinrate = 0

if "chess_bullet" in userStats:
    bulletrating=userStats["chess_bullet"]["last"]["rating"]
    print("Bullet Rating: " + str(bulletrating))
    bulletwinrate=userStats["chess_bullet"]["record"]["win"]/(userStats["chess_bullet"]["record"]["win"]+userStats["chess_bullet"]["record"]["loss"]+userStats["chess_bullet"]["record"]["draw"])
    print("Blitz Win Rate: " + str(winrate))
    if int(bulletrating)>float(r2) and float(accountage)<float(r5) and float(playaccuracy)>float(r4) or float(bulletwinrate)>float(r6):
        print('Sus!')
    elif int(bulletrating)>float(r2) and float(accountage)<float(r5) and float(bulletwinrate)>float(r6) or float(playaccuracy)>float(r4):
        print('Sus!')
    else:
        print('Never mind.')
else:
    bulletrating = 0
    bulletwinrate = 0

List=[username,blitzwinrate*100,bulletwinrate*100,winrate*100,blitzrating,bulletrating,rapidrating,accountage, playaccuracy]
print("List: " + str(List))
print('Do you wish to check for updates?')
answer=input("Enter yes or no:")

if answer=="yes":
	with open('suschess.csv', 'a',newline='') as f_object:
    		writer_object = writer(f_object)
    		writer_object.writerow(List)
    		f_object.close()
elif answer=="no":
	print('Goodbye')
#else:
	#print('Please answer yes or no')

print('Is the status on the account closed for fair play violations?')
answer=input("Enter yes or no:")
if answer=="yes":
	with open('suschess.csv', 'r') as f1, open('chess.csv', 'a+') as f2:
    		f2.write(str(List))
elif answer=="no":
		print('error')
		#f2.write(writer_object)
#else:
	#print('Please answer yes or no')