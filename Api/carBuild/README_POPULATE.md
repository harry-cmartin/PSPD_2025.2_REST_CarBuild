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

### Opção 3: Script Bash Automatizado
```bash
cd Api/carBuild

# Tornar executável (apenas primeira vez)
chmod +x setup_database.sh

# Executar script interativo
./setup_database.sh
```

## 📊 Dados Criados

### 🚗 **Carros (10 modelos)**
- Civic (2020)
- Corolla (2019)
- Fusca (1970)
- Gol (2018)
- Onix (2021)
- HB20 (2020)
- Polo (2019)
- Fiesta (2017)
- Uno (2016)
- Palio (2015)

### 🔧 **Peças (Mais de 150 peças)**

#### **Peças Genéricas** (para todos os carros):
- Filtros (ar, óleo, combustível)
- Sistema de freio (pastilhas, discos)
- Sistema elétrico (velas, bateria, alternador)
- Suspensão (amortecedores)
- Pneus (diferentes medidas)
- Fluidos (óleo motor, freio, radiador)
- Iluminação (lâmpadas H4, H7)

#### **Peças Especializadas**:
- **Fusca**: Carburador Weber, Cilindro Mestre, Gerador 6V
- **Civic**: Kit Embreagem VTEC, Sensor MAP Honda, ECU Original
- **Corolla**: Kit Embreagem Toyota, Sensor Oxigênio

#### **Peças Universais** (sem carro específico):
- Produtos de limpeza e manutenção
- Acessórios gerais
- Fluidos universais

### 📋 **Pedidos (5-10 pedidos aleatórios)**
- Cada pedido tem 1-6 itens diferentes
- Quantidades realistas (pneus em pares, peças caras unitárias)
- Valores calculados automaticamente
- UUIDs únicos para identificação

## ⚙️ Regras de Negócio Implementadas

### **Quantidades Inteligentes**:
- **Chassi**: Máximo 1 unidade
- **Pneus**: Sempre em pares (2 ou 4)
- **Peças caras** (>R$ 500): Geralmente 1 unidade
- **Outras peças**: 1-4 unidades

### **Preços Realistas**:
- Faixas de preço por tipo de peça
- Variação aleatória dentro da faixa
- Peças especializadas mais caras
- Peças universais com preços médios

### **Relacionamentos Corretos**:
- Peças específicas vinculadas a carros
- Peças universais sem vinculação
- Pedidos com múltiplos itens
- Cálculo automático de totais

## 🔍 Verificar Dados Criados

### Via Django Admin:
```bash
python3 manage.py runserver
# Acesse: http://localhost:8000/admin/
```

### Via API:
```bash
# Listar carros
curl http://localhost:8000/api/cars/

# Listar peças
curl http://localhost:8000/api/pecas/

# Peças de um carro específico
curl http://localhost:8000/api/cars/1/pecas/
```

### Via Python Shell:
```bash
python3 manage.py shell

# No shell Python:
from car.models import Car, Peca, Pedido, ItemPedido

print(f"Carros: {Car.objects.count()}")
print(f"Peças: {Peca.objects.count()}")
print(f"Pedidos: {Pedido.objects.count()}")
print(f"Itens: {ItemPedido.objects.count()}")

# Ver carros com suas peças
for car in Car.objects.all():
    print(f"{car.modelo}: {car.pecas.count()} peças")
```

## 🛠 Solução de Problemas

### **Erro de Migração**:
```bash
python3 manage.py makemigrations car
python3 manage.py migrate
```

### **Erro de ImportError**:
```bash
# Verificar se está no diretório correto
ls -la  # Deve mostrar manage.py

# Verificar se Django está instalado
python3 -c "import django; print(django.VERSION)"
```

### **Erro de Permissão (Linux/Mac)**:
```bash
chmod +x setup_database.sh
```

### **Limpar Tudo e Recomeçar**:
```bash
# Apagar banco SQLite
rm db.sqlite3

# Recriar migrações
python3 manage.py makemigrations car
python3 manage.py migrate

# Popular novamente
python3 manage.py populate_db --clear
```

## 📈 Exemplo de Saída

```
🚀 Iniciando população do banco de dados...

🚗 Criando carros...
  ✓ Civic (2020)
  ✓ Corolla (2019)
  ✓ Fusca (1970)
  ...
🚗 Criados 10 carros

🔧 Criando peças...
  ✓ Filtro de Ar para Civic - R$ 45.67
  ✓ Pastilha de Freio Dianteira para Civic - R$ 156.89
  ✓ Kit Embreagem VTEC (especial) para Civic - R$ 987.45
  ...
🔧 Criadas 156 peças

📋 Criando pedidos...
  ✓ Pedido a1b2c3d4... - 3 itens - R$ 245.67
  ✓ Pedido e5f6g7h8... - 5 itens - R$ 1234.56
  ...
📋 Criados 7 pedidos

🎉 Banco de dados populado com sucesso!

📊 Resumo:
   🚗 Carros: 10
   🔧 Peças: 156
   📋 Pedidos: 7
   📦 Itens: 23
```

## 🎯 Próximos Passos

1. **Criar superusuário**:
   ```bash
   python3 manage.py createsuperuser
   ```

2. **Iniciar servidor**:
   ```bash
   python3 manage.py runserver
   ```

3. **Testar no frontend**:
   ```bash
   cd ../../WebClient
   npm start
   ```

Agora seu banco está populado e pronto para testar a integração completa entre Django API e React Frontend! 🎉