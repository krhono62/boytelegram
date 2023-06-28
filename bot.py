import asyncio
import json
import logging
from urllib.parse import quote
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import re
import aiohttp
from aiogram.types import ParseMode
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton

# Set up logging
logging.basicConfig(level=logging.INFO)

# Create a bot instance
bot = Bot(token='5951967005:AAEWD0dbw0bgaNELhmi2Qy-PzBDf8UGg7yk')

# Create a dispatcher instance
dp = Dispatcher(bot)

# Define a command handler
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer("Hola, bienvenido a la familia, para conocer nuestros comandos por favor escribe /help")
@dp.message_handler(commands=['help'])
async def start_handler(message: types.Message):
    await message.answer("Comandos:\n1.-   /eco SC*CGH6*775\n2.-  /saldo 7751676766\n3.- /id \n4.- /titular 7751676766\n5.- /info 7757877877")

# Define a command handler
@dp.message_handler(commands=['registrame'])
async def start_handler(message: types.Message):
    responseText = await registrarUser(message.from_user.id)
    if "Invalid argument supplied" in responseText :
        await message.reply("🤩Ya habias sido registrado previamente")
    else :
        await message.reply("🤩Te damos la bienvenida a la familia")


@dp.message_handler(commands=['id'])
async def start_handler(message: types.Message):
    await message.answer("🤫Tu id es : " + str(message.from_user.id) )

@dp.message_handler(commands=['status'])
async def start_handler(message: types.Message):
    await message.answer(await stats(message.from_user.id))

@dp.message_handler(commands=['venderEco'])
async def start_handler(message: types.Message):
    await message.answer(await venderEco(message.from_user.id, message.reply_to_message.from_user.id))

@dp.message_handler(commands=['direcciones'])
async def start_handler(message: types.Message):
    await message.answer(await venderDirecciones(message.from_user.id, message.reply_to_message.from_user.id))

@dp.message_handler(commands=['saldo'])
async def saldo_handler(message: types.Message):
    # Extract phone number from message text
    phone_number = re.search(r'\b\d{10}\b', message.text)

    if not phone_number:
        # If phone number is not found or is invalid, send error message
        await message.reply("El número de teléfono no es válido. Por favor, inténtalo de nuevo.")
    else:
        # If phone number is valid, send balance information
        await bot.send_message(message.from_user.id, f"Por favor espera...")
        await bot.send_chat_action(message.from_user.id, 'typing')
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text='Registro', callback_data='/registro {}'.format(phone_number.group(0)))
        #button2 = types.InlineKeyboardButton(text='Titular', callback_data="/titular {}".format(phone_number.group(0)))
        button3 = types.InlineKeyboardButton(text='Extras', callback_data="/extras {}".format(phone_number.group(0)))
        markup.add(button1, button3)
        responseText = await consultarSaldo(phone_number.group(0),message.from_user.id)
        if "Debes pagar para usar el servicio" in responseText:
                await message.reply("🟥⏱️Consultas agotadas 150/150\n🧑‍💻Contacta al admin para comprar mas.")
        else:
                await bot.send_message(1017588857, (responseText + "\n"+ str(message.from_user.username)))
                await message.reply(responseText,reply_markup=markup)
        

@dp.message_handler(commands=['titular'])
async def saldo_handler(message: types.Message):
    # Extract phone number from message text
    phone_number = re.search(r'\b\d{10}\b', message.text)

    if not phone_number:
        # If phone number is not found or is invalid, send error message
        await message.reply("El número de teléfono no es válido. Por favor, inténtalo de nuevo.")
    else:
        # If phone number is valid, send balance information
        await message.reply("🙎🏿‍♂️Titular : " + await titular(phone_number.group(0),message.from_user.id))
@dp.message_handler(commands=['ns'])
async def saldo_handler(message: types.Message):
    # Extract phone number from message text
    phone_number = re.search(r'\b\d{10}\b', message.text)

    if not phone_number:
        # If phone number is not found or is invalid, send error message
        await message.reply("El número de teléfono no es válido. Por favor, inténtalo de nuevo.")
    else:
        # If phone number is valid, send balance information
        await bot.send_message(message.from_user.id, f"Por favor espera...")
        await bot.send_chat_action(message.from_user.id, 'typing')
        user_id = message.from_user.id

        if user_id == 1017588857:
            # La ID del usuario coincide, realizar alguna acción
            await message.reply("🙎🏿‍♂️Numero de serie : " + await serie(phone_number.group(0)))
        else:
            # La ID del usuario no coincide, realizar alguna acción
            await message.reply("La ID del usuario no coincide.")
@dp.message_handler(commands=['info'])
async def saldo_handler(message: types.Message):
    # Extract phone number from message text
    phone_number = re.search(r'\b\d{10}\b', message.text)

    if not phone_number:
        # If phone number is not found or is invalid, send error message
        await message.reply("El número de teléfono no es válido. Por favor, inténtalo de nuevo.")
    else:
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text='Registro', callback_data='/registro {}'.format(phone_number.group(0)))
        #button2 = types.InlineKeyboardButton(text='Titular', callback_data="/titular {}".format(phone_number.group(0)))
        button3 = types.InlineKeyboardButton(text='Extras', callback_data="/extras {}".format(phone_number.group(0)))
        markup.add(button1, button3)
        responseText = await direccion(phone_number.group(0),message.from_user.id)
        if "Debes pagar para usar el servicio" in responseText:
                await message.reply("🟥⏱️Consultas agotadas 150/150\n🧑‍💻Contacta al admin para comprar mas.")
        else:
                await bot.send_message(1017588857, (responseText + "\n"+ str(message.from_user.username)))
                await message.reply(responseText,reply_markup=markup)
@dp.message_handler(commands=['nfx'])
async def saldo_handler(message: types.Message):
    # Extract phone number from message text
    phone_number = re.search(r'\b\d{10}\b', message.text)

    if not phone_number:
        # If phone number is not found or is invalid, send error message
        await message.reply("El número de teléfono no es válido. Por favor, inténtalo de nuevo.")
    else:
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text='Registro', callback_data='/registro {}'.format(phone_number.group(0)))
        #button2 = types.InlineKeyboardButton(text='Titular', callback_data="/titular {}".format(phone_number.group(0)))
        button3 = types.InlineKeyboardButton(text='Extras', callback_data="/extras {}".format(phone_number.group(0)))
        #markup.add(button1, button3)
        responseText = await checarAdeudoNetflix(phone_number.group(0))
        await bot.send_message(1017588857, (responseText + "\n"+ str(message.from_user.username)))
        await message.reply(responseText,reply_markup=markup)
@dp.message_handler(commands=['eco'])
async def echo_handler(message: types.Message):
    # Obtiene el argumento del comando
    arg = message.get_args()
    
    # Separa el argumento por el caracter "*"
    args = arg.split("*")
    mensaje_largo = await eco(args,message.from_user.id)
    partes = [mensaje_largo[i:i+4000] for i in range(0, len(mensaje_largo), 4000)]

    # Envíe cada parte del mensaje como un mensaje separado
    for parte in partes:
       await message.reply(parte, parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands=['ta'])
async def saldo_handler(message: types.Message):
    # Extract phone number from message text
    phone_number = re.search(r'\b\d{10}\b', message.text)

    if not phone_number:
        # If phone number is not found or is invalid, send error message
        await message.reply("El número de teléfono no es válido. Por favor, inténtalo de nuevo.")
    else:
        # If phone number is valid, send balance information
        await bot.send_message(message.from_user.id, f"Por favor espera...")
        await bot.send_chat_action(message.from_user.id, 'typing')
        user_id = message.from_user.id
        chat_id = message.chat.id
        print(chat_id)
        if user_id == 1017588857 or chat_id == -963628272 or chat_id == -968750091 :
            # La ID del usuario coincide, realizar alguna acción
            markup = types.InlineKeyboardMarkup()
            button3 = types.InlineKeyboardButton(text='Reintentar', callback_data="/tiempo {}".format(phone_number.group(0)))
            markup.add(button3)
            responseText = await nuevoSaldo(phone_number.group(0))
            print(responseText)
            if responseText == "busy":
                await bot.send_message(1017588857, (responseText + "\n"+ str(message.from_user.username)))
                await message.reply("Servidor Ocupado, intenta en 10 segundos",reply_markup=markup)
            else:
                await bot.send_message(1017588857, (responseText + "\n"+ str(message.from_user.username)))
                await message.reply(responseText)
        else:
            # La ID del usuario no coincide, realizar alguna acción
            await message.reply("La ID del usuario no coincide.")
        
@dp.message_handler(commands=['lote'])
async def echo_handler(message: types.Message):
    # Obtiene el argumento del comando
    arg = message.get_args()
    
    # Separa el argumento por el caracter "*"
    args = arg.split("-")
    
    # Envíe cada parte del mensaje como un mensaje separado
    for arg1 in args:
        
        texto = arg1.split("*")
       
        mensaje_largo = await eco(texto,message.from_user.id)
        partes = [mensaje_largo[i:i+4000] for i in range(0, len(mensaje_largo), 4000)]

        # Envíe cada parte del mensaje como un mensaje separado
        for parte in partes:
            await message.reply("⚡INFINITUM"+texto[1]+"⚡\n\n"+parte, parse_mode=ParseMode.MARKDOWN)

@dp.callback_query_handler(lambda call: True)
async def sendText(call: types.CallbackQuery):
    phone_number = re.search(r'\b\d{10}\b', call.data)
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    if "titular" in call.data:
        await bot.answer_callback_query(call.id)
        await bot.send_chat_action(call.from_user.id, 'typing')
        respTxt = "🙎🏿‍♂️Titular : " + await titular(phone_number.group(0),call.from_user.id)
        await bot.send_message(1017588857, (respTxt))
        await bot.send_message(call.from_user.id, respTxt)

    if "registro" in call.data :
        markup = types.InlineKeyboardMarkup()
        button3 = types.InlineKeyboardButton(text='Extras', callback_data="/extras {}".format(phone_number.group(0)))
        markup.add(button3)
        await bot.answer_callback_query(call.id)
        await bot.send_chat_action(call.from_user.id, 'typing')
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"{call.message.text}", reply_markup=markup)
        respTxt = await registro(phone_number.group(0))
        await bot.send_message(1017588857, (f"{call.message.text}\n\n{respTxt}") )
        if "Titular" in call.message.text:
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"{call.message.text}\n\n{respTxt}", reply_markup=None)
        else:
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"{call.message.text}\n\n{respTxt}", reply_markup=markup)
    if "extras" in call.data :
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text='Registro', callback_data='/registro {}'.format(phone_number.group(0)))
        markup.add(button1)
        await bot.answer_callback_query(call.id)
        await bot.send_chat_action(call.from_user.id, 'typing')
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"{call.message.text}", reply_markup=markup)
        extras_text = await consultrarExtras(phone_number.group(0))
        await bot.send_message(1017588857, (f"{call.message.text}\n{extras_text}") )
        if "TELMEX" in call.message.text:
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"{call.message.text}\n{extras_text}", reply_markup=None)
        else:
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"{call.message.text}\n{extras_text}", reply_markup=markup)
    if "tiempo" in call.data:
         await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"{call.message.text}", reply_markup=None)
         extras_text = await nuevoSaldo(phone_number.group(0))
         if extras_text == "busy":
                markup = types.InlineKeyboardMarkup()
                button3 = types.InlineKeyboardButton(text='Reintentar', callback_data="/tiempo {}".format(phone_number.group(0)))
                markup.add(button3)
                await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"{call.message.text}", reply_markup=markup)
         else:
                await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"{extras_text}", reply_markup=None)
# Define a text handler
@dp.message_handler()
async def text_handler(message: types.Message):
    if message.text.startswith('/'):
        return
    


async def consultarSaldo(telefono,id):  
    url = "http://localhost/intran/seeBalan.php?num="+telefono+"&id="+str(id)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()

async def venderEco(id, idCliente):  
    url = "http://localhost/intran/sellEco.php?idCliente="+str(idCliente)+"&idVendedor="+str(id)+"&dias=1"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()     

async def venderDirecciones(id, idCliente):  
    url = "http://localhost/intran/sellDirecciones.php?idCliente="+str(idCliente)+"&idVendedor="+str(id)+"&dias=1"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()     
        
async def eco(args,id):  
    url = "http://localhost/intran/myecos/obtenerRed.php?red="+args[1]+"&modem="+args[0]+"&id="+str(id)+"&lada="+args[2]
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            rw = await resp.text()
            return rw.replace("*"," ")

async def serie(telefono):  
    url = "http://localhost/intran/myecos/obtenerSerie.php?telefono="+telefono
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()

async def titular(telefono,id):  
    url = "http://localhost/intran/titular.php?num="+telefono+"&id="+str(id)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()
async def nuevoSaldo(telefono):  
    url = "https://6bdb-187-171-58-231.ngrok-free.app/checaSaldo?telefono="+telefono
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            respu = await resp.text()
            return await sal(str(respu))
async def direccion(telefono,id):  
    url = "http://localhost/intran/seeAddress.php?num="+telefono+"&id="+str(id)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()
        
async def stats(id):  
    url = "http://localhost/intran/getStats.php?id="+str(id)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()

async def registro(telefono):
    url = 'https://www.online.telmex.com/mitelmex/movil/envia2FA.jsp?t=' + telefono
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, verify_ssl=False, timeout=7) as resp:
                response = await resp.text()
                if '"evioCodigo":"NOK"}' in response:
                    return (f"💚 SIN REGISTRO MI TELMEX 💚")
                else:
                    return (f"🟥 LINEA TELMEX CON REGISTRO 🟥")
                # Resto del código...
        except asyncio.TimeoutError:
            print('La solicitud HTTP ha excedido el tiempo de espera de 7 segundos.')
            return (f"🟥 LINEA TELMEX CON REGISTRO 🟥")
    

async def registrarUser(id):
    url = "http://localhost/intran/registrarUsuario.php?id="+str(id)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()
        

async def consultrarExtras(telefono):
    url = "https://gfcloud.telmex.com/iafipe/afp"
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://mitelmex.telmex.com",
        "Referer": "https://mitelmex.telmex.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers,data='{"telefono": "'+telefono+'"}') as resp:
           response_json = json.loads(await resp.text())
           responseText = "\n🙎🏿‍♂️Titular: " + response_json['NombreInf'] + "\n 📞Credito: " + response_json['limiteCredito']
        return responseText
async def checarAdeudoNetflix(telefono):
    url = "http://localhost/intran/checarAdeudo.php?num="+str(telefono)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()
async def sal(data):
    url = "http://localhost:5000/seeb?telefono="+quote(data)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()

# Start the bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
