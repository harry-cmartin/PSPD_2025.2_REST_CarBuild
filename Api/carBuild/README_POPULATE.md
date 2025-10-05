# Scripts de População do Banco de Dados

Este diretório contém scripts para popular o banco de dados com dados de exemplo baseados nos modelos Django.

## 📁 Arquivos Criados

### 1. **Comando Django** (`car/management/commands/populate_db.py`)
Comando personalizado do Django para popular o banco.

### 2. **Script Python Standalone** (`populate_database.py`)
Script Python que pode ser executado diretamente.

### 3. **Script Bash** (`setup_database.sh`)
Script bash que automatiza todo o processo (migrações + população).

## 🚀 Como Usar

### Opção 1: Comando Django (Recomendado)
```bash
cd Api/carBuild

# Popular com dados completos
python3 manage.py populate_db

# Limpar dados antes de popular
python3 manage.py populate_db --clear

# Criar apenas carros e peças (sem pedidos)
python3 manage.py populate_db --cars-only

# Ver ajuda
python3 manage.py populate_db --help
```

### Opção 2: Script Python Direto
```bash
cd Api/carBuild

# Popular com dados completos
python3 populate_database.py

# Limpar dados antes de popular
python3 populate_database.py --clear

# Criar apenas carros e peças
python3 populate_database.py --cars-only
```

