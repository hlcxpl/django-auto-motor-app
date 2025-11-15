#!/bin/bash
# Script para instalar dependencias de Python en Ubuntu/Debian
echo "Instalando dependencias para compilar Python..."
apt update
apt install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
libffi-dev liblzma-dev
echo "Dependencias instaladas correctamente."