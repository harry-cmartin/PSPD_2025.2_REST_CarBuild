# Arquitetura de Microsserviços - Sistema de Peças Automotivas

## 🏗️ Visão Geral da Arquitetura

```
┌─────────────────────┐    HTTP/REST    ┌─────────────────────┐
│   Frontend React   │◄──────────────►│   Django Gateway    │
│   (localhost:3000)  │                 │   (localhost:8000)  │
└─────────────────────┘                 └─────────────────────┘
                                                    │
                                                    ▼
                                        ┌─────────────────────┐
                                        │   Orquestração      │
                                        │                     │
                                        └─────────────────────┘
                                                    │
                                ┌───────────────────┼───────────────────┐
                                ▼                   ▼                   ▼
                    ┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
                    │  Microsserviço A    │ │  Microsserviço B    │ │   Base de Dados     │
                    │  (Banco de Dados)   │ │ (Cálculos/Pedidos)  │ │     SQLite          │
                    └─────────────────────┘ └─────────────────────┘ └─────────────────────┘
```

## 🎯 Responsabilidades dos Componentes

### 📱 **Frontend React** (`WebClient/`)
- Interface do usuário
- Exibição de carros e peças
- Carrinho de compras
- Finalização de pedidos
- **Comunicação**: Apenas com Django Gateway

### 🚪 **Django Gateway** (`Api/carBuild/`)
- **Função**: API Gateway / Backend for Frontend (BFF)
- **Responsabilidades**:
  - Receber requisições do frontend
  - Orquestrar chamadas para microsserviços
  - Agregar respostas
  - Autenticação e autorização
  - Logs e monitoramento

### 🗄️ **Microsserviço A** - Gerenciamento de Banco
- **Localização**: `microservices/service_a.py`
- **Responsabilidades**:
  - ✅ Listar carros
  - ✅ Buscar carros por ID
  - ✅ Listar peças de um carro
  - ✅ Buscar peças com filtros
  - ✅ Operações CRUD no banco de dados

### 🧮 **Microsserviço B** - Cálculos e Pedidos
- **Localização**: `microservices/service_b.py`
- **Responsabilidades**:
  - ✅ Calcular preços com frete
  - ✅ Gerar IDs únicos para pedidos
  - ✅ Criar pedidos completos
  - ✅ Gerar relatórios de pedidos
  - ✅ Validar dados de entrada

## 🔗 Endpoints da API Gateway

### 🚗 **Carros** (delegado para Microsserviço A)
```http
GET /api/cars/                    # Lista todos os carros
GET /api/cars/{id}/               # Detalhes de um carro
GET /api/cars/{id}/pecas/         # Peças de um carro específico
```

### 🔧 **Peças** (delegado para Microsserviço A)
```http
GET /api/pecas/                   # Lista peças (com filtros)
GET /api/pecas/{id}/              # Detalhes de uma peça
```

### 💰 **Cálculos** (delegado para Microsserviço B)
```http
POST /api/calculate-price/        # Calcular preço total
POST /api/generate-order-id/      # Gerar ID único
```

### 📋 **Pedidos** (delegado para Microsserviço B)
```http
POST /api/orders/                 # Criar pedido
GET /api/orders/{id}/report/      # Relatório do pedido
```

### 🏥 **Utilitários**
```http
GET /api/health/                  # Health check dos microsserviços
```

## 📊 Fluxo de Dados

### **1. Listar Carros**
```
Frontend → Gateway → Microsserviço A → Banco → Microsserviço A → Gateway → Frontend
```

### **2. Calcular Preços**
```
Frontend → Gateway → Microsserviço B → Cálculo → Gateway → Frontend
```

### **3. Criar Pedido**
```
Frontend → Gateway → Microsserviço B → Banco → Relatório → Gateway → Frontend
```

## 🛠️ Implementação Atual

### **Modo "Internal"** (Desenvolvimento)
- Ambos os microsserviços executam no mesmo processo Django
- Comunicação via chamadas diretas de função
- Configuração: `MICROSERVICE_A_URL = 'internal'`

### **Modo "External"** (Produção)
- Microsserviços como serviços separados
- Comunicação via HTTP/REST
- Configuração: `MICROSERVICE_A_URL = 'http://microservice-a:8001'`

## ⚙️ Configurações

### **`settings.py`**
```python
# URLs dos Microsserviços
MICROSERVICE_A_URL = 'internal'  # ou URL externa
MICROSERVICE_B_URL = 'internal'  # ou URL externa

# Configurações de Negócio
FRETE_GRATIS_VALOR = 200.00
VALOR_FRETE = 25.00

# Timeouts
MICROSERVICE_TIMEOUT = 10
```

### **`microservices/config.py`**
```python
# Configurações específicas dos microsserviços
CIRCUIT_BREAKER_FAILURE_THRESHOLD = 5
MICROSERVICE_RETRY_ATTEMPTS = 3
```

## 🔄 Exemplos de Requisições

### **1. Calcular Preço via Microsserviço B**
```javascript
// Frontend
const items = [
  { peca_id: 1, quantidade: 2 },
  { peca_id: 3, quantidade: 1 }
];

const response = await calculationService.calculatePrice(items);
```

```http
POST /api/calculate-price/
Content-Type: application/json

{
  "items": [
    {"peca_id": 1, "quantidade": 2},
    {"peca_id": 3, "quantidade": 1}
  ]
}
```

**Resposta:**
```json
{
  "status": "success",
  "data": {
    "subtotal": 150.00,
    "frete": 25.00,
    "total": 175.00,
    "frete_gratis": false,
    "items": [...]
  }
}
```

### **2. Criar Pedido via Microsserviço B**
```http
POST /api/orders/
Content-Type: application/json

{
  "items": [
    {"peca_id": 1, "quantidade": 2},
    {"peca_id": 3, "quantidade": 1}
  ]
}
```

**Resposta:**
```json
{
  "status": "success",
  "data": {
    "pedido_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "valor_total": 175.00,
    "data_pedido": "2025-10-05T14:30:00Z",
    "relatorio": {...}
  }
}
```

## 🧪 Como Testar

### **1. Health Check**
```bash
curl http://localhost:8000/api/health/
```

### **2. Listar Carros (Microsserviço A)**
```bash
curl http://localhost:8000/api/cars/
```

### **3. Calcular Preço (Microsserviço B)**
```bash
curl -X POST http://localhost:8000/api/calculate-price/ \
  -H "Content-Type: application/json" \
  -d '{"items":[{"peca_id":1,"quantidade":2}]}'
```

### **4. Criar Pedido (Microsserviço B)**
```bash
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{"items":[{"peca_id":1,"quantidade":2}]}'
```

## 🚀 Vantagens desta Arquitetura

### **1. Separação de Responsabilidades**
- **Microsserviço A**: Foca apenas em dados
- **Microsserviço B**: Foca apenas em lógica de negócio
- **Gateway**: Orquestra tudo

### **2. Escalabilidade**
- Cada microsserviço pode ser escalado independentemente
- Possibilidade de usar tecnologias diferentes por serviço

### **3. Manutenibilidade**
- Código organizado por domínio
- Easier debugging e testing
- Deploy independente (quando externos)

### **4. Flexibilidade**
- Modo interno para desenvolvimento
- Modo externo para produção
- Fácil migração entre modos

## 🔮 Roadmap Futuro

### **Implementações Pendentes:**
1. **Circuit Breaker** para resiliência
2. **Retry Logic** com backoff exponencial
3. **Load Balancing** para múltiplas instâncias
4. **Service Discovery** para ambiente distribuído
5. **Distributed Tracing** para monitoramento
6. **Authentication/Authorization** entre serviços

### **Migração para Produção:**
1. Dockerizar cada microsserviço
2. Configurar Kubernetes/Docker Compose
3. Implementar service mesh (Istio)
4. Adicionar API versioning
5. Implementar CQRS pattern

## 📈 Monitoramento

### **Logs Estruturados:**
```python
logger.info("Microsserviço A: Buscando carros", extra={
    "service": "microservice_a",
    "operation": "get_cars",
    "timestamp": datetime.now()
})
```

### **Métricas:**
- Latência de resposta por microsserviço
- Taxa de erro por endpoint
- Throughput de requisições
- Health check status

Agora o sistema está completamente reestruturado com arquitetura de microsserviços! 🎉