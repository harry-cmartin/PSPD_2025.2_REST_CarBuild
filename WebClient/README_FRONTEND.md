# Frontend WebClient - Sistema de Peças Automotivas

Este é o frontend React para o sistema de gestão de peças automotivas que consome a API Django.

## 🚀 Configuração

### 1. Instalar dependências
```bash
cd WebClient
npm install
```

### 2. Configurar variáveis de ambiente
Crie um arquivo `.env` na raiz do WebClient:

```env
# URL da API Django
REACT_APP_API_URL=http://localhost:8000/api

# Outras configurações opcionais
REACT_APP_ENABLE_LOGGING=true
```

### 3. Executar a aplicação
```bash
npm start
```

A aplicação estará disponível em: `http://localhost:3000`

## 📡 Integração com a API Django

O frontend está configurado para consumir as seguintes rotas da API:

### Carros
- `GET /api/cars/` - Lista todos os carros
- `GET /api/cars/{id}/pecas/` - Lista peças de um carro específico

### Peças
- `GET /api/pecas/` - Lista todas as peças
- `GET /api/pecas/?nome=filtro` - Busca peças por nome
- `GET /api/pecas/?car_id=1` - Filtra peças por carro
- `GET /api/pecas/?min_valor=50&max_valor=200` - Filtra por faixa de preço

## 🛠 Funcionalidades Implementadas

### ✅ Carregamento Dinâmico
- Carrega carros da API Django automaticamente
- Fallback para dados mock se a API estiver indisponível
- Estados de loading e erro

### ✅ Seleção de Carros e Peças
- Interface intuitiva para seleção de carros
- Busca automática de peças por carro
- Seleção de quantidades com validações

### ✅ Cálculo de Preços em Tempo Real
- Cálculo automático do subtotal
- Frete grátis acima de R$ 200
- Atualização instantânea ao alterar quantidades

### ✅ Sistema de Compras
- Finalização de pedidos (mock implementado)
- Confirmação de compra com detalhes
- Histórico de itens comprados

## 📁 Estrutura de Arquivos

```
WebClient/
├── public/
│   └── index.html
├── src/
│   ├── App.js          # Componente principal
│   ├── api.js          # Configuração da API
│   ├── config.js       # Configurações globais
│   ├── index.js        # Ponto de entrada
│   └── index.css       # Estilos globais
├── package.json
└── README.md
```

## 🔧 Configurações Importantes

### API Configuration (src/config.js)
```javascript
const config = {
  API_BASE_URL: 'http://localhost:8000/api',
  FRETE_GRATIS_VALOR: 200,
  VALOR_FRETE: 25,
  MAX_QUANTITY_DEFAULT: 4,
};
```

### API Services (src/api.js)
- `carService.getAll()` - Busca carros
- `carService.getPecas(carId)` - Busca peças do carro
- `pecaService.getAll(filters)` - Busca peças com filtros
- `apiUtils.calculatePrice(itens)` - Calcula preços

## 🔄 Fluxo de Funcionamento

1. **Inicialização**: Carrega carros da API
2. **Seleção de Carro**: Usuário escolhe um carro
3. **Busca de Peças**: Frontend busca peças do carro selecionado
4. **Seleção de Itens**: Usuário escolhe peças e quantidades
5. **Cálculo de Preços**: Cálculo automático em tempo real
6. **Finalização**: Criação do pedido (necessita implementação no backend)

## 🚨 Pendências para Implementação Completa

### No Backend Django:
1. **Criar views para pedidos**:
   ```python
   # views.py
   @api_view(['POST'])
   def create_pedido(request):
       # Implementar criação de pedidos
   ```

2. **Adicionar URLs de pedidos**:
   ```python
   # urls.py
   path('pedidos/', create_pedido, name='create_pedido'),
   ```

3. **Configurar CORS**:
   ```python
   # settings.py
   CORS_ALLOWED_ORIGINS = [
       "http://localhost:3000",
   ]
   ```

### No Frontend (se necessário):
1. Implementar autenticação de usuários
2. Adicionar persistência de carrinho
3. Melhorar tratamento de erros
4. Adicionar testes unitários

## 🐛 Debugging

### Verificar conexão com API:
1. Abra o console do navegador (F12)
2. Verifique os logs de requisições
3. Confirme se a API Django está rodando em `http://localhost:8000`

### Problemas comuns:
- **CORS Error**: Configurar django-cors-headers no backend
- **Connection Refused**: Verificar se a API está rodando
- **404 Not Found**: Verificar URLs da API

## 📝 Logs e Monitoramento

O frontend possui logs detalhados no console:
- 🚀 Requisições enviadas
- ✅ Respostas recebidas
- ❌ Erros de API
- 💰 Cálculos de preços

Para habilitar logs completos, defina no `.env`:
```
REACT_APP_ENABLE_LOGGING=true
```