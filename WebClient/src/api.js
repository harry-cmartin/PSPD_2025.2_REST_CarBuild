import axios from 'axios';
import config from './config';

// Instância do axios com configurações padrão
const api = axios.create({
  baseURL: config.API_BASE_URL,
  timeout: config.API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para logs (opcional)
api.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('❌ API Response Error:', error.response || error);
    return Promise.reject(error);
  }
);

// Funções da API para carros
export const carService = {
  // Listar todos os carros
  getAll: () => api.get('/cars/'),
  
  // Obter peças de um carro específico
  getPecas: (carId) => api.get(`/cars/${carId}/pecas/`),
};

// Funções da API para peças
export const pecaService = {
  // Listar todas as peças (com filtros opcionais)
  getAll: (filters = {}) => {
    const params = new URLSearchParams();
    
    if (filters.nome) params.append('nome', filters.nome);
    if (filters.car_id) params.append('car_id', filters.car_id);
    if (filters.min_valor) params.append('min_valor', filters.min_valor);
    if (filters.max_valor) params.append('max_valor', filters.max_valor);
    
    const query = params.toString();
    return api.get(`/pecas/${query ? '?' + query : ''}`);
  },
  
  // Buscar peças por termo
  search: (query) => api.get(`/search/pecas/?q=${encodeURIComponent(query)}`),
};

// Funções da API para cálculos e pedidos (Microsserviço B)
export const calculationService = {
  // Calcular preço de itens
  calculatePrice: (items) => api.post('/calculate-price/', { items }),
  
  // Gerar ID único para pedido
  generateOrderId: () => api.post('/generate-order-id/'),
};

// Funções da API para pedidos (Microsserviço B)
export const pedidoService = {
  // Criar pedido
  create: (orderData) => api.post('/orders/', orderData),
  
  // Obter relatório de um pedido
  getReport: (orderId) => api.get(`/orders/${orderId}/report/`),
};

// Funções utilitárias
export const apiUtils = {
  // Health check dos microsserviços
  healthCheck: () => api.get('/health/'),
  
  // Calcular preço total de itens (local)
  calculatePriceLocal: (itens) => {
    return itens.reduce((total, item) => {
      return total + (item.peca.valor * item.quantidade);
    }, 0);
  },
  
  // Formatar itens para o microsserviço B
  formatItemsForCalculation: (selectedParts, parts) => {
    return Object.entries(selectedParts).map(([partId, quantidade]) => ({
      peca_id: parseInt(partId),
      quantidade: quantidade
    }));
  },
  
  // Formatar moeda brasileira
  formatCurrency: (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  },
};

export default api;