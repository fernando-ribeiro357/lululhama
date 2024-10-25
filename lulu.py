import time
import os
import re
import asyncio
from ollama import AsyncClient, ResponseError

def prompt():
    ''' 
    Função para receber o prompt do usuário e fazer a 
    requisição assíncrona ao chat com o prompt fornecido 
    '''
    pergunta=input('😃 📣 ')
    if pergunta.lower() != 'sair':
        asyncio.run(chat(pergunta))
        prompt()

    print("\n.\n")
    time.sleep(2)


def retira_aster(text):
    ''' 
    Função para retirar o caracter '*' do texto fornecido  
    '''
    return re.sub('\*', '', text)


async def chat(pergunta):
    ''' 
    Função que implementa o cliente do Ollama  
    '''
    message = {'role': 'user', 'content': pergunta}
    try:
        print(""" 
   /)🎀(\\
  ( o __o)
  (  ( Y )
  (      )
                """)
        async for part in await AsyncClient().chat(model='lululhama', messages=[message], stream=True):
            saida = retira_aster(part['message']['content'])
            print(saida, end='', flush=True)
    except ResponseError as e:
        print('Error:', e.error)    
    print("\n")
    

def testeira():
    ''' Exibe o nome estilizado do programa na tela '''
    print(""" 
    ************************************************************
    *                                                     ▄    *
    *                                                     █▄   *
    *                                                     ██▀  *
    *   █░░ █░█ █░░ █░█  █░░ █░█ ▄▀█ █▀▄▀█ ▄▀█            ██   *
    *   █▄▄ █▄█ █▄▄ █▄█  █▄▄ █▀█ █▀█ █░▀░█ █▀█    ███❀❀❀❀███   *
    *                                            █ █████████   *
    *                                              ██     ██   *
    *                                              ██     ██   *
    *  (digite 'sair' para encerrar)                           *
    ************************************************************
    
   /)🎀(\\
  ( o __o)
  (  ( Y )
  (      )
                
Eu sou a Lulu Lhama! Pode conversar comigo.

          """)

def main():
    '''
    Função principal que inicia o programa 
    '''
    os.system('clear')
    testeira()
    prompt()


if __name__ == '__main__':
    main()

