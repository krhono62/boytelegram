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
            print("asdhjashjdgghjasdgjhasd")
            return "💚 SIN REGISTRO MI TELMEX 💚"
        else:
            
            return "🟥 LINEA TELMEX CON REGISTRO 🟥"
        
    except requests.Timeout:
        print('La solicitud HTTP ha excedido el tiempo de espera de 7 segundos.')
        return "🟥 LINEA TELMEX CON REGISTRO 🟥"


def consultarExtras(telefono):
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

if __name__ == '__main__':
    app.run()
