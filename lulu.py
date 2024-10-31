import os, re, json
from datetime import datetime
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from rich.console import Console
from rich.markdown import Markdown

load_dotenv()

def header():
    ''' Exibe o user estilizado do programa na tela '''
    print(""" 
    ╔══════════════════════════════════════════════════════════╗
    ║  🎀 🎀 🎀 🎀 🎀 🎀 🎀 🎀 🎀 🎀 🎀 🎀 🎀             ▄    ║
    ║                                                     █▄   ║
    ║ *****************************************           ██▀  ║
    ║ * █░░ █░█ █░░ █░█  █░░ █░█ ▄▀█ █▀▄▀█ ▄▀█*           ██   ║
    ║ * █▄▄ █▄█ █▄▄ █▄█  █▄▄ █▀█ █▀█ █░▀░█ █▀█*   ███❀❀❀❀███   ║
    ║ *****************************************  █ █████████   ║
    ║                                              ██     ██   ║
    ║  🌸 🌸 🌸 🌸 🌸 🌸 🌸 🌸 🌸 🌸 🌸 🌸 🌸      ██     ██   ║
    ╚══════════════════════════════════════════════════════════╝
    
   /)🎀(\\
  ( o __o)
  (  ( Y )
  (      )
                
! Pode conversar comigo.
          """)


def prompt():
    ''' 
    Função para receber o prompt do usuário e fazer a 
    requisição ao chat com o prompt fornecido
    '''
    try:
        mensagens = []
        pergunta0 = 'Olá. Eu sou a Lulu Lhama. Qual é o seu nome?'
        mensagens.append(('assistant', pergunta0))
        user = input(f'{pergunta0}\n >>> ')        
        mensagens.append(('user', user))
        pergunta1 = f'Olá {user}. Vamos conversar.'
        mensagens.append(('assistant', pergunta1))
        print(f'{pergunta1} \n')
        while True:
            pergunta = input(f'["x": sair]\n{user} >>> ')

            if pergunta.lower() == 'x':
                print('\nSaindo do programa...\n')            
                break
            
            mensagem = ('user', pergunta)
            history(mensagem);
            mensagens.append(mensagem)
            # resposta = retira_aster(resposta_bot(mensagens))
            resposta = resposta_bot(mensagens)
            mensagem = ('assistant', resposta)
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
            print('\n')
        print('Obrigado por me consultar, estarei sempre aqui para te ajudar.\n')
        # history(mensagens)
    except KeyboardInterrupt:
        print("Sinal de interrupção recebido. Encerrando...")

def resposta_bot(mensagens):
    # Para utilizar o ChatGroq, é necessário configurar GROQ_API_KEY no .env
    # chat = ChatGroq(model='llama-3.1-70b-versatile')
    # Utilizar as mensagens modelo para passar mensagens do sistema
    # mensagens_modelo = [('system', 'Seu user é Lulu e você é uma atendente lhama amigável, que fica feliz em ajudar.')]
    # mensagens_modelo += mensagens
    chat = ChatOllama(base_url='http://192.168.1.40:11434',model='lululhama')
    template = ChatPromptTemplate.from_messages(mensagens)
    chain = template | chat
    return chain.invoke({}).content


def retira_aster(text):
    ''' 
    Função para retirar o caracter '*' do texto fornecido  
    '''
    return re.sub('\*', '', text)


def history(tupla):    
    try:
        now = datetime.now()
        data_hora = now.strftime('%Y-%m-%d %H:%M:%S')
        data = now.strftime('%Y-%m-%d')
        caminho_do_arquivo = f'./history/{data}.txt'
        # Abre o arquivo no modo 'w' (write), que sobrescreve o arquivo se já existir
        with open(caminho_do_arquivo, 'a') as arquivo:
            # Escreve a variável no arquivo
            arquivo.write(data_hora + ' : ' + str(tupla) + '\n')
    except Exception as e:
        print(f"Ocorreu um erro ao escrever o arquivo: {e}")


def main():
    '''
    Função principal que inicia o programa 
    '''
    os.system('clear')
    header()
    prompt()


if __name__ == '__main__':
    main()
