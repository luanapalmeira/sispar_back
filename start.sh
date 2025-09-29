#!/bin/bash

# ============================
# Script para rodar Flask no Git Bash
# ============================

# Carrega variáveis do .env (somente linhas VAR=VALOR válidas)
export $(grep -v '^#' .env | xargs)

# Define a aplicação Flask
export FLASK_APP=src.app   # <-- aqui você indica o arquivo principal
export FLASK_ENV=development  # opcional, para modo debug

# Mensagem para conferir
echo "Variáveis de ambiente carregadas:"
echo "URL_DATABASE_DEV=$URL_DATABASE_DEV"
echo "URL_DATABASE_PROD=$URL_DATABASE_PROD"
echo "FLASK_APP=$FLASK_APP"

# Roda o Flask
echo "Iniciando Flask..."
flask --debug run
