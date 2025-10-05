# Configurações dos Microsserviços

# URLs dos Microsserviços (em produção seriam URLs externas)
MICROSERVICE_A_URL = 'internal'  # ou 'http://microservice-a:8001'
MICROSERVICE_B_URL = 'internal'  # ou 'http://microservice-b:8002'

# Configurações de Negócio para Microsserviço B
FRETE_GRATIS_VALOR = 200.00  # Valor mínimo para frete grátis
VALOR_FRETE = 25.00          # Valor do frete padrão

# Configurações de Timeout
MICROSERVICE_TIMEOUT = 10    # Timeout em segundos para chamadas HTTP

# Configurações de Retry
MICROSERVICE_RETRY_ATTEMPTS = 3
MICROSERVICE_RETRY_DELAY = 1  # Delay em segundos entre tentativas

# Configurações de Circuit Breaker (para implementação futura)
CIRCUIT_BREAKER_FAILURE_THRESHOLD = 5
CIRCUIT_BREAKER_TIMEOUT = 60