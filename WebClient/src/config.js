// Configurações da aplicação
const config = {
  // URL base da API Django
  API_BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
  
  // Configurações de timeout
  API_TIMEOUT: 10000,
  
  // Configurações de frete
  FRETE_GRATIS_VALOR: 200,
  VALOR_FRETE: 25,
  
  // Configurações de quantidade máxima
  MAX_QUANTITY_DEFAULT: 4,
  MAX_QUANTITY_CHASSI: 1,
  
  // Configurações de debounce
  PRICE_CALCULATION_DELAY: 500,
};

export default config;