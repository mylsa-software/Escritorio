import os
import pdfplumber
import json


Json = {}

path=os.path.dirname(os.path.abspath(__file__))

print(path)
for file in os.listdir(path):
    if file.endswith('.pdf'):
        print(file)

        data=[]

        with pdfplumber.open(os.path.join(path,file)) as filepdf:
            for i, pages in enumerate(filepdf.pages):
                tables = pages.extract_tables()
                for table in tables:
                    for row in table:
                        if row[0] != "CAT CLAVE DESCRIPCION\nVEHICULAR":
                            
                            for row1 in row:
                                
                                if row1:
                                    lineas = row1.splitlines()
                                    for line in lineas:
                                        if line != "EQUIPOOPCIONAL":
                                            data.append(line)
        
        info=[]

        for data1 in data:
            componentes = data1.split()

            if len(componentes) == 7 or len(componentes) == 5:
                row={"Cat":componentes[0],"Vehicular":componentes[1],"Modelo":componentes[2],"Precio":componentes[4].replace(',','')}
                info.append(row)

            if len(componentes) == 6:
                row={"Cat":componentes[0],"Vehicular":componentes[1],"Modelo":componentes[2],"Precio":componentes[len(componentes)-2].replace(',','')}
                info.append(row)
        
        Json[os.path.splitext(file)[0]]=info

with open(os.path.join(path,"Cat.json"),"w",encoding='utf-8') as data:
    json.dump(Json,data,indent=4,ensure_ascii=False)


