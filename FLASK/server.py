import numpy as np
from flask import Flask, render_template, jsonify, request, send_from_directory
import requests
import os


app = Flask(__name__)

@app.route('/')
'''def index():
  return render_template('home.html')'''

# Rota que recupera arquivos da pasta "assets"
@app.route('/assets/<path:path>')
def send_assets(path):
  return send_from_directory('assets', path)


# ROTA PRINCIPAL que mostra a página "resultado.html"
@app.route('/analise', methods=['POST'])
def analisar(videoInput):
  '''
  Pega video de input, executa método e retorna resultado como requisicao HTTP
  '''
  pass

  
@app.route('/demo', methods=['POST'])
def demo_func():
  '''
  Pega video de demonstracao do servidor, finge processamento e retorna resultados
  '''
  pass

if __name__ == '__main__':
  # para poder adicionar um sheduler de tasks de background,
  # adicionar use_reloader=False
    app.run(debug=True)