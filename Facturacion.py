from flask import Flask, request, jsonify
import os
from flask_cors import CORS
import xml.etree.ElementTree as ET

# -*- coding: utf-8 -*-
app = Flask(__name__)
CORS(app, origins="*")

@app.route('/process', methods=['POST'])
def process_data():
    try:
        # Recibiendo y validando la data
        data = request.get_json()
        ReceptorData = data.get("Receptor", {})
        EmisorData = data.get("Emisor", {})
        ConceptoData = data.get("Concepto", {})
        ImpuestosData = data.get("Impuestos", {})
        rfc = ReceptorData.get("RFC")

        if not rfc:
            return jsonify({"error": "RFC not found in the data"}), 400

        formatted_data = """
        ### Comprobante ###
        Version        : 4.0
        Serie          : NF
        Folio          : 8392
        Fecha          : 2025-01-07T15:34:49
        Forma Pago     : PAGO EN UNA SOLA EXHIBICION
        Total          : 636460.34
        Moneda         : MXN
        Tipo Cambio    : 1
        Subtotal       : 738293.99
        Tipo Comprobante: I
        Exportacion    : 01
        Lugar Emision  : PUE
        CP Emisor      : 07700

        ### Emisor ###
        RFC           : %(RFCEmisor)s
        Nombre        : %(NombreEmisor)s
        Reg Fiscal    : %(RegimenFiscalEmisor)s

        ### Receptor ###
        RFC           : %(RFCReceptor)s
        Nombre        : %(NombreReceptor)s
        CP            : %(CPReceptor)s
        Reg Fiscal    : %(RegimenFiscalReceptor)s
        Uso CFDI      : %(UsoCFDIReceptor)s

        ### Concepto ###
        Clave ProdServ: %(ClaveProd)s
        No. Identidad : %(NoIdentidad)s
        Cantidad      : %(Cantidad)s
        Unidad        : %(Unidad)s
        Descripcion   : %(Descripcion)s
        Valor Unitario: %(ValorUnitario)s
        Importe       : %(Importe)s

        ### Impuestos Trasladados ###
        Base          : %(Base)s
        Impuesto      : %(Impuesto)s
        Tipo Factor   : %(TipoFactor)s
        Tasa          : %(Tasa)s
        Importe       : %(Importe)s

        ### Mensaje PDF ###
        MONEDA: MXN, VEHICULO NO CAUSA ISAN, EN VIRTUD DE TRATARSE DE UNA VENTA ENTRE CONCESIONARIOS EL IMPUESTO CORRESPONDIENTE SE PAGARA EN EL MOMENTO DE LA PRIMERA ENAJENACION AL PUBLICO, LA TRANSMISION DE LA PROPIEDAD DEL BIEN AL QUE SE REFIERE LA PRESENTE FACTURA SE FORMALIZA A TRAVES DEL CONTRATO DE ADHESION CORRESPONDIENTE, CONFORME A LAS DISPOSICIONES DE LA NORMA OFICIAL MEXICANA 160-SCFI-2003.
        """ % {
            'RFCEmisor': EmisorData.get('RFC', ''),
            'NombreEmisor': EmisorData.get('Nombre', ''),
            'RegimenFiscalEmisor': EmisorData.get('RegimenFiscal', ''),

            'RFCReceptor': ReceptorData.get('RFC', ''),
            'NombreReceptor': ReceptorData.get('Nombre', ''),
            'CPReceptor': ReceptorData.get('CP', ''),
            'RegimenFiscalReceptor': ReceptorData.get('RegimenFiscal', ''),
            'UsoCFDIReceptor': ReceptorData.get('UsoCFDI', ''),

            'ClaveProd': ConceptoData.get('ClaveProd', ''),
            'NoIdentidad': ConceptoData.get('NoIdentidad', ''),
            'Cantidad': ConceptoData.get('Cantidad', ''),
            'Unidad': ConceptoData.get('Unidad', ''),
            'Descripcion': ConceptoData.get('Descripcion', ''),
            'ValorUnitario': ConceptoData.get('ValorUnitario', ''),
            'Importe': ConceptoData.get('Importe', ''),

            'Base': ImpuestosData.get('Base', ''),
            'Impuesto': ImpuestosData.get('Impuesto', ''),
            'TipoFactor': ImpuestosData.get('TipoFactor', ''),
            'Tasa': ImpuestosData.get('Tasa', ''),
            'Importe': ImpuestosData.get('Importe', '')
        }

        # Guardar en archivo
        pathorigin = os.getcwd()
        filenameTxt = "{}.txt".format(rfc)
        filepathTxt = os.path.join(pathorigin + "/Aplicacion", filenameTxt)
        filenameXml = "{}.txt".format(rfc)
        filepathXml = os.path.join(pathorigin + "/Aplicacion", filenameXml)

        with open(filepathTxt, "w") as archivo:
            archivo.write(formatted_data)

        tree = ET.parse(filepathXml)
        root = tree.getroot()

        namespaces = {
            "cfdi": "http://www.sat.gob.mx/cfd/4",
            "xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "ventavehiculos": "http://www.sat.gob.mx/ventavehiculos",
        }

        comprobante = {
            "Version": root.attrib.get("Version"),
            "Serie": root.attrib.get("Serie"),
            "Folio": root.attrib.get("Folio"),
            "Fecha": root.attrib.get("Fecha"),
            "FormaPago": root.attrib.get("FormaPago"),
            "SubTotal": root.attrib.get("SubTotal"),
            "Total": root.attrib.get("Total"),
        }

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8086)

