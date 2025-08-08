import time
import pandas as pd
import json
import os
from docling.document_converter import DocumentConverter

path=os.path.dirname(os.path.abspath(__file__))
final = {}

for file in os.listdir(path):
    if file.endswith('.pdf'):
        print(file)

        doc_converter = DocumentConverter()
        conv_res = doc_converter.convert(os.path.join(path,file))

        Json = []
        with open(file.replace('pdf',"txt"), "w", encoding="utf-8") as txt_file:
            for table_ix, table in enumerate(conv_res.document.tables):
                table_df: pd.DataFrame = table.export_to_dataframe()
                #filtramos solo cat validos y quitamos los rows con EQUIPO OPCIONAL
                if len(table_df.columns)>=5:
                    if len(table_df.columns)==7:
                        table_df.columns=['CAT','CLAVE VEHICULAR','DESCRIPCION','PRECIO LISTA','PRECIO CLIENTE','FORD CREDIT ','CONTADO']
                    elif len(table_df.columns)==5:
                        table_df.columns=['CAT','CLAVE VEHICULAR','DESCRIPCION','PRECIO LISTA','PRECIO CLIENTE']

                    table_df = table_df[~table_df["CAT"].str.match(r"^\d", na=False)]
                    table_df = table_df[~table_df["CAT"].isin(["EQUIPO OPCIONAL", "EQUIPO", "OPCIONAL","NV / NP"])]

                    for index,row in table_df.iterrows():
                        Json.append({
                            "Cat": row['CAT'],
                            "Vehicular": row['CLAVE VEHICULAR'],
                            "Modelo": row['DESCRIPCION'],
                            "Precio": row['PRECIO LISTA'].replace(',','')
                        })

                    txt_file.write(table_df.to_string(index=False))
                    txt_file.write('\n')
        
        final[os.path.splitext(file)[0]]=Json
        
with open("Cat.json", "w", encoding="utf-8") as txt_file:
    json.dump(final, txt_file , ensure_ascii=False, indent=4)