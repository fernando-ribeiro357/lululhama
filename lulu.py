import os
import re
import json
import random
import string
import pygame
from gtts import gTTS
from datetime import datetime
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from rich.console import Console
from rich.markdown import Markdown

load_dotenv()

def header():
    ''' Exibe o user estilizado do programa na tela '''
    print(""" 
    ╔═══════════════════════════════════════════════════════════╗
    ║  🎀 🎀 🎀 🎀 🎀 🎀 🎀 🎀 🎀 🎀 🎀 🎀 🎀              ▄    ║
    ║                                                      █▄   ║
    ║ ******************************************           ██▀  ║
    ║ * █░░ █░█ █░░ █░█  █░░ █░█ ▄▀█ █▀▄▀█ ▄▀█ *           ██   ║
    ║ * █▄▄ █▄█ █▄▄ █▄█  █▄▄ █▀█ █▀█ █░▀░█ █▀█ *   ███❀❀❀❀███   ║
    ║ ******************************************  █ █████████   ║
    ║                                               ██     ██   ║
    ║  🌸 🌸 🌸 🌸 🌸 🌸 🌸 🌸 🌸 🌸 🌸 🌸 🌸       ██     ██   ║
    ╚═══════════════════════════════════════════════════════════╝
    
   /)🎀(\\
  ( o __o)
  (  ( Y )
  (      )
          """)


def prompt():
    ''' 
    Função para receber o prompt do usuário e fazer a 
    requisição ao chat com o prompt fornecido
    '''
    try:
        mensagens = []
        pergunta0 = 'Olá. Qual é o seu nome?'
        mensagem = ('ai', pergunta0)
        mensagens.append(mensagem)
        history(mensagem);
        tts(pergunta0)
        user = input(f'{pergunta0}\n >>> ')
        mensagem = ('human', user)
        mensagens.append(mensagem)
        history(mensagem)
        pergunta1 = f'Oi {user}. Vamos conversar.'
        mensagem = ('ai', pergunta1)
        mensagens.append(mensagem)
        history(mensagem)
        print(f'{pergunta1}')
        tts(pergunta1)
        print('\n')
        while True:
            pergunta = input(f'["x": sair]\n{user} >>> ')

            if pergunta.lower() == 'x':
                print('\nSaindo do programa...\n')            
                break
            
            mensagem = ('human', pergunta)
            history(mensagem);
            mensagens.append(mensagem)
            resposta = resposta_bot(mensagens)
            mensagem = ('ai', resposta)
            history(mensagem);
            mensagens.append(mensagem)
            print(f'''
   /)🎀(\\
  ( o __o)
  (  ( Y )
  (      )
  ''')
            console = Console()
            markdown = Markdown(resposta)
            console.print(markdown)
            texto = re.sub("\*", "", resposta)
            # string = re.sub(r'[^a-zA-Z0-9]', '', resposta)
            emoji_pattern = re.compile(u"["  
                                       u"\U0001F600-\U0001F64F|"  # emoticons
                                       u"\U0001F300-\U0001F5FF|"  # symbols & pictographs
                                       u"\U0001F680-\U0001F6FF|"  # transport & map symbols
                                       u"\U0001F1E0-\U0001F1FF"   # flags (iOS)
                                       "]+", flags=re.UNICODE)
            string = emoji_pattern.sub(r'', texto)
            tts(string)
            print('\n')
        
        string = 'Obrigado por me consultar, estarei sempre aqui para te ajudar.'
        print(f'{string}')
        tts(string)
        print('\n')
        # history(mensagens)
    except KeyboardInterrupt:
        print("Sinal de interrupção recebido. Encerrando...")

def resposta_bot(mensagens):
    mensagens_modelo = [('system', 'Seu nome é Lulu e você é uma assistente lhama amigável, que fica feliz em ajudar. Você mora em uma montanha no Peru onde a natureza é exuberante com lindos pastos verdes salpicados de pequenas flores coloridas. Você adora contar piadas e jogos em texto com o usuário.')]
    mensagens_modelo += mensagens
    chat = ChatOllama(base_url=os.getenv('OLLAMA_URL','http://localhost:11434'), model=os.getenv('OLLAMA_MODEL','llama3.2'))
    template = ChatPromptTemplate.from_messages(mensagens_modelo)
    chain = template | chat
    return chain.invoke({}).content

def history(tupla):    
    now = datetime.now()
    data_hora = now.strftime('%Y-%m-%d %H:%M:%S')
    data = now.strftime('%Y-%m-%d')
    caminho_do_arquivo = f'./history/{data}.txt'
    try:
        # Abre o arquivo no modo 'a' (append), que escreve no final do arquivo se já existir
        with open(caminho_do_arquivo, 'a') as arquivo:
            # Escreve a variável no arquivo
            arquivo.write(data_hora + '|' + str(tupla) + '\n')            
    except Exception as e:
        print(f"Ocorreu um erro ao escrever o arquivo {caminho_do_arquivo}: {e}")

def tts(text: str, lang="pt", slow=False, file_name: str | None = None):
    '''Função para converter o texto em voz (tts) utilizando a bibioteca gTTS
        e o pygame.mixer para executar o áudio gerado pelo texto fornecido
    '''
    # Teste
    # print(f"{text}")

    file_name = file_name or random_mp3_fname()
    file_path = f"/tmp/{file_name}"    
    tts = gTTS(text=text, lang=lang, slow=slow)
    tts.save(file_path)

    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.stop()
    os.remove(file_path)

def random_mp3_fname(str_size=12, allowed_chars=string.ascii_letters) -> str:
    fname = ''.join(random.choice(allowed_chars) for x in range(str_size))
    return f"{fname}.mp3"


def main():
    '''
    Função principal que inicia o programa 
    '''
    os.system('clear')
    header()
    prompt()


if __name__ == '__main__':
    main()
