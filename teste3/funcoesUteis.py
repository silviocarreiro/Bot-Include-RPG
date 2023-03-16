#Funcoes uteis -------------------------------------------------
def verificar_mapa(mensagem):
    comandos = ['Mapa 🗺']
    if mensagem.text in comandos:
        return True
    
def verificar_chaves(mensagem):
    comandos = ['Chaves Adquiridas 🗝']
    if mensagem.text in comandos:
        return True

def verificar_enigma_atual(mensagem):
    comandos = ['Enigma 📜']
    if mensagem.text in comandos:
        return True
    
def open_photo():
    chave1 = open("chave1.png", 'rb')
    chave2 = open("chave2.png", 'rb')
    chave3 = open("chave3.png", 'rb')
    chaves_desafios = [chave1, chave2, chave3]
    return chaves_desafios
#---------------------------------------------------------------