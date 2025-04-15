import requests
import os
import glob

def DeletSale(path):

    filestxt = glob.glob(os.path.join(path, '*.txt'))

    for file in filestxt:
        os.remove(file)

url = "http://mylsa.com.mx/pilot/DesktopRemote/Seals.php"
#url="http://localhost:8888/DesktopRemote/Seals.php"

response = requests.get(url)
path= os.getcwd()

DeletSale(path)

if response.status_code == 200:
    data = response.json()

    print(data)

    for info in data:
        info['ReferenciaPilot']
        print(path+"/"+str(info['ReferenciaPilot'])+".txt")
        if not os.path.exists(path+"/"+str(info['ReferenciaPilot'])+".txt"):
            with open(path+"/"+str(info['ReferenciaPilot'])+".txt","w") as file:
                for key,info in info.items():
                    file.write(key+" => " + str(info)+"\n")
                    
else:
    print('error de conexion')





    