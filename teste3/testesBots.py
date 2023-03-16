import telebot
from telebot import types
from shapely.geometry import Point, Polygon
from funcoesUteis import *

CHAVE_API = '5637032623:AAHd6hqrZKi0vJK7AyDluwGJGdRh-sENtsk'

#vetor para as chaves adiquiridas com a resolução dos enigmas (fotos)
chaves_desafios = []

#chaves conseguidas por cada usuário
chaves_usuario = dict()

#progresso do usuario no bot
progresso_usuario = dict()

bot = telebot.TeleBot(CHAVE_API)

#Menu ----------------------------------------------------------
#mostrar menu
def menu(mensagem):
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    botao_mapa = types.KeyboardButton("Mapa 🗺")  
    botao_chaves = types.KeyboardButton("Chaves Adquiridas 🗝")
    botao_enigma = types.KeyboardButton("Enigma 📜")
    menu.add(botao_mapa, botao_chaves, botao_enigma)

    bot.send_message(mensagem.chat.id, "Você poderá interagir com o menu abaixo.", reply_markup=menu)

#mostrar mapa
@bot.message_handler(func=verificar_mapa)
def mapa(mensagem):
    bot.send_message(mensagem.chat.id, "Aqui está o mapa: ")

    photo = open("mapa.png", 'rb')
    bot.send_photo(mensagem.chat.id, photo=photo)

#mostrar chaves adquiridas
@bot.message_handler(func=verificar_chaves)
def chaves_adquiridas(mensagem):

    print(f"Quantidade de Chaves ({mensagem.from_user.first_name}): {chaves_usuario[mensagem.from_user.id]}")
    if chaves_usuario[mensagem.from_user.id] == 0:
        bot.send_message(mensagem.chat.id, "Você ainda não possui nenhuma chave. Resolva os enigmas para obtê-las.")
    else:
        bot.send_message(mensagem.chat.id, "Aqui estão as chaves que você adquiriu até o momento: ")

        #fazer um for para imprimir 3 imagens
        chaves = open_photo()
        for i in range(chaves_usuario[mensagem.from_user.id]): 
            bot.send_photo(mensagem.chat.id, photo=chaves[i])

    #bot.send_message(mensagem.chat.id, "Ocorreu um erro inesperado.")
    

#mostrar enigma atual
@bot.message_handler(func=verificar_enigma_atual)
def enigma(mensagem):
    try:
        print(f"Enigma atual ({mensagem.from_user.first_name}): {progresso_usuario[mensagem.from_user.id]}")
        if progresso_usuario[mensagem.from_user.id] == 1:
            enigma1(mensagem)
        elif progresso_usuario[mensagem.from_user.id] == 2:
            enigma2(mensagem)
        elif progresso_usuario[mensagem.from_user.id] == 3:
            enigma3(mensagem)
        elif progresso_usuario[mensagem.from_user.id] == 4:
            enigma4(mensagem)
        elif progresso_usuario[mensagem.from_user.id] == 5:
            bot.send_message(mensagem.chat.id, "Você, não tem mais enigmas para resolver. Vá para a sala do PET para finalizar a dinâmica.")
        else:
            pass
    except:
        bot.send_message(mensagem.chat.id, "Ocorreu um erro inesperado. Repita sua ação.")
#------------------------------------------------------------------

#Chamadas para conferir respostas ---------------------------------
@bot.message_handler(content_types=['location'])
def respostas_localizacao(mensagem):
    try:
        if progresso_usuario[mensagem.from_user.id] == 2:
            loc_enigma2(mensagem)
        elif progresso_usuario[mensagem.from_user.id] == 3:
            loc_enigma3(mensagem)
        elif progresso_usuario[mensagem.from_user.id] == 4:
            loc_enigma4(mensagem)
        else:
            pass
    except:
        bot.send_message(mensagem.chat.id, "Ocorreu um erro inesperado. Repita sua ação.")

@bot.message_handler(commands=["resposta"])
def respostas_escritas(mensagem):
    try:
        progresso_atual = progresso_usuario[mensagem.from_user.id]
        if progresso_atual == 0:
            resposta_inicio(mensagem)
        elif progresso_atual == 1:
            resposta_biblioteca(mensagem)
        elif progresso_atual == 2:
            resposta_programacao(mensagem)
        else:
            pass
    except:
        bot.send_message(mensagem.chat.id, "Ocoreu um erro inesperado.")
#------------------------------------------------------------------

#Desafio 1 --------------------------------------------------------
@bot.message_handler(commands=["start"])
def mensagem_inicio(mensagem):
    chaves_usuario[mensagem.from_user.id] = 0
    progresso_usuario[mensagem.from_user.id] = 0
    bot.send_message(mensagem.chat.id, "Seja bem-vindo, aventureiro(a)! Estou empolgado em ver você embarcando em uma jornada para resolver desafios e enigmas. Você é uma pessoa corajosa e habilidosa, e estou certo de que será capaz de superar todos os obstáculos que surgirem em seu caminho.")

    bot.send_message(mensagem.chat.id, "Como já foi explicado no auditório, no seu primeiro desafio você e sua equipe precisarão utilizar a criatividade para montar uma frase com palavras aleatórias que estão escritas nas paredes do ICA. ")
    bot.send_message(mensagem.chat.id, "Tirem uma foto de cada palavra da frase que vocês montaram e, no final, mostrem para o membro do PET que se encontra na entrada. Com isso, ele irá informar a senha para o primeiro Enigma.")


def resposta_inicio(mensagem):
    resposta = mensagem.text[10:]
    if resposta.lower() != "python":
        bot.send_message(mensagem.chat.id, "Senha errada! Verifique se escreveu corretamente e tente novamente.")
    else:
        bot.send_message(mensagem.chat.id, "Parabéns, você passou para a próxima etapa!")
        progresso_usuario[mensagem.from_user.id] = 1

        menu(mensagem)

        bot.send_message(mensagem.chat.id, "Quando estiver preparado, clique em 'Enigma 📜' para aceitar esse desafio.")
#---------------------------------------------------------------

#Enigma 1 ------------------------------------------------------
def enigma1(mensagem):

    photo = open("enigma1.png", 'rb')
    bot.send_photo(mensagem.chat.id, photo=photo)

    bot.send_message(mensagem.chat.id, "Para responder o enigma você deve achar a senha escondida pelo campus. Ao encontrá-la, digite /resposta [resposta aqui] para confirmar se a senha está correta.")

def resposta_biblioteca(mensagem):
    resposta = mensagem.text[10:]
    livro_correto = ["algoritmos","algoritmos teoria e prática","algoritmos: teoria e prática"] 
    if resposta.lower() not in livro_correto:
        bot.reply_to(mensagem, "Resposta errada ❌")
    else:
        bot.send_message(mensagem.chat.id, "Parabéns, você desvendou o primeiro enigma!")
        
        #adiciona ponto (chave adquirida)
        chaves_usuario[mensagem.from_user.id] = 1
        progresso_usuario[mensagem.from_user.id] = 2
        
        bot.send_message(mensagem.chat.id, "Você obteve uma chave. Para ver todas as chaves que você adquiriu até agora clique em 'Chaves Adquiridas 🗝'.")
        bot.send_message(mensagem.chat.id, "Para receber o próximo enigma, clique em 'Enigma 📜'.")
#----------------------------------------------------------------

#Enigma 2 -------------------------------------------------------
def enigma2(mensagem):
    photo = open("enigma2.png", 'rb')
    bot.send_photo(mensagem.chat.id, photo=photo)
    bot.send_message(mensagem.chat.id, "Neste enigma você deve achar o local descrito pelo enigma. Ao chegar no lugar, você envia sua *Localização Atual* (como indicado na foto abaixo) para verificar se está no local correto.")
    photo = open("instrucao.png", 'rb')
    bot.send_photo(mensagem.chat.id, photo=photo)

def loc_enigma2(mensagem):
    print(f"latitude: {mensagem.location.latitude} \nlongitude: {mensagem.location.longitude}")
    #print(mensagem)
    bloco_910 = Polygon([(-3.745898438499496, -38.5744853446593), (-3.745708408491267, -38.573944879578114), (-3.746262439526792, -38.57430965998031), (-3.7461098802911312, -38.57383893232895)])
    #print("chega aqui 1")
    loc_user = Point(mensagem.location.latitude, mensagem.location.longitude)
    #loc_user = Point(-3.745949295397726, -38.57425736501989)
    #print("chega aqui 2")
    if bloco_910.contains(loc_user):
        #print("chega aqui 3")
        bot.send_message(mensagem.chat.id, "Párabens, você encontrou o local correto. Agora, dirija-se ao LEC para um petiano lhe guiar no próximo desafio.")
        #print("chega aqui 4")
        print(f"Usuário: {mensagem.from_user.first_name}: localização correta")
    else:
        bot.send_message(mensagem.chat.id, "Localização errada ❌. Tente novamente em um local próximo ou continue procurando pelo lugar certo!")
        print(f"Usuário: {mensagem.from_user.first_name}: localização errada.")
#----------------------------------------------------------------

#Desafio 2 -------------------------------------------------------
def resposta_programacao(mensagem):
    resposta = mensagem.text[10:]
    if resposta.lower() != "prog127":
        bot.send_message(mensagem.chat.id, "Senha errada! Verifique se escreveu corretamente e tente novamente.")
    else:
        progresso_usuario[mensagem.from_user.id] = 3
        #colocar marcador depois para conseguir que nao acessem esse desafio antes de conseguir essa senha.

        bot.send_message(mensagem.chat.id, "Parabéns,você passou pelo desafio de programação. Quando estiver preparado, clique em 'Enigma 📜' para acessar o próximo enigma")
#------------------------------------------------------------------

#Enigma 3 ---------------------------------------------------------
def enigma3(mensagem):
    photo = open("enigma3.png", 'rb')
    bot.send_photo(mensagem.chat.id, photo=photo)
    bot.send_message(mensagem.chat.id, "Neste enigma você deve achar o local descrito pelo enigma. Ao chegar no lugar, você envia sua *Localização Atual* para verificar se está no local correto.")

def loc_enigma3(mensagem):
    print(f"latitude: {mensagem.location.latitude} \nlongitude: {mensagem.location.longitude}")
    
    ru = Polygon([(-3.744389860527157, -38.5728667273693), (-3.7448784344658783, -38.572386677242974), (-3.7454030557739775, -38.57283362543783), (-3.7448882800346324, -38.573321053709016)])
    
    loc_user = Point(mensagem.location.latitude, mensagem.location.longitude)

    if ru.contains(loc_user):
        chaves_usuario[mensagem.from_user.id] = 2
        progresso_usuario[mensagem.from_user.id] = 4
        bot.send_message(mensagem.chat.id, "Párabens, você encontrou o local correto.")
        bot.send_message(mensagem.chat.id, "Você obteve uma chave. Para ver todas as chaves que você adquiriu até agora, vá ao menu e clique em 'Chaves Adquiridas'.")

        bot.send_message(mensagem.chat.id, "Quando estiver preparado, clique em 'Enigma 📜' para acessar o próximo enigma")
        print(f"Usuário: {mensagem.from_user.first_name}: localização correta")
    else:
        bot.send_message(mensagem.chat.id, "Localização errada ❌. Tente novamente em um local próximo ou continue procurando pelo lugar certo!")
        print(f"Usuário: {mensagem.from_user.first_name}: localização errada.")
#-------------------------------------------------------------------

#Enigma 4 ----------------------------------------------------------
def enigma4(mensagem):
    photo = open("enigma4.png", 'rb')
    bot.send_photo(mensagem.chat.id, photo=photo)
    bot.send_message(mensagem.chat.id, "Neste enigma você deve achar o local descrito pelo enigma. Ao chegar no lugar, você envia sua *Localização Atual* para verificar se está no local correto.")


def loc_enigma4(mensagem):
    print(f"latitude: {mensagem.location.latitude} \nlongitude: {mensagem.location.longitude}")
    
    mangueiras = Polygon([(-3.7456977063762764, -38.57530208540856), (-3.745590647197231, -38.57481124119089), (-3.746338722936829, -38.57508080317928), (-3.746155384219029, -38.574552408037874)])

    loc_user = Point(mensagem.location.latitude, mensagem.location.longitude)

    if mangueiras.contains(loc_user):
        chaves_usuario[mensagem.from_user.id] = 3
        progresso_usuario[mensagem.from_user.id] = 5
        bot.send_message(mensagem.chat.id, "Párabens, você encontrou o local correto.")
        bot.send_message(mensagem.chat.id, "Você obteve uma chave. Para ver todas as chaves que você adquiriu até agora, vá ao menu e clique em 'Chaves Adquiridas'.")

        bot.send_message(mensagem.chat.id, "Você resolveu todos os enigmas. Para finalizar a atividade, dirija-se a sala do pet e dê sua resposta final de acordo com as chaves que você adquiriu.")
        print(f"Usuário: {mensagem.from_user.first_name}: localização correta")
    else:
        bot.send_message(mensagem.chat.id, "Localização errada ❌. Tente novamente em um local próximo ou continue procurando pelo lugar certo!")
        print(f"Usuário: {mensagem.from_user.first_name}: localização errada.")
#-----------------------------------------------------------------------

bot.infinity_polling(none_stop=True)

#Coisas pra fazer ainda ------------------------------------------
# - Ver como vou colocar o bot em um servidor junto com as fotos.
# - Pesquisar como subir fotos no servidor do telegram.
# - Procurar uma forma de fazer a função verificar se tornar só uma.
# - Olhar como remover a mensagem de "aqui está o menu".
#-----------------------------------------------------------------