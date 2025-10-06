import React, { useState, useEffect } from "react";
import { carService, calculationService, pedidoService, apiUtils } from "./api";
import CartPage from "./CartPage";

function App() {
  const [cars, setCars] = useState([]);
  const [selectedCar, setSelectedCar] = useState(null);
  const [parts, setParts] = useState([]);
  const [selectedParts, setSelectedParts] = useState({}); // {partId: quantidade}
  const [pricing, setPricing] = useState(null);
  const [loading, setLoading] = useState(false);
  const [carsLoading, setCarsLoading] = useState(false);
  const [pricingLoading, setPricingLoading] = useState(false);
  const [error, setError] = useState(null);
  const [pricingError, setPricingError] = useState(null);
  const [purchaseResult, setPurchaseResult] = useState(null);
  const [showPurchasePage, setShowPurchasePage] = useState(false);
  const [purchaseLoading, setPurchaseLoading] = useState(false);
  const [showCartPage, setShowCartPage] = useState(false);

  // Carregar carros da API ao inicializar
  useEffect(() => {
    const loadCars = async () => {
      setCarsLoading(true);
      setError(null); // Limpar erro anterior
      try {
        console.log("🚗 Carregando carros da API...");
        const response = await carService.getAll();
        console.log("✅ Carros carregados:", response.data);
        setCars(response.data.data || []);
      } catch (err) {
        console.error("❌ Erro ao carregar carros:", err);
        setError(`Erro ao carregar carros: ${err.response?.data?.message || err.message}`);
        setCars([]); // Array vazio se não conseguir carregar da API
      } finally {
        setCarsLoading(false);
      }
    };

    loadCars();
  }, []);

  // Abrir carrinho
  const onOpenCart = () => {
    if (getTotalItems() > 0) {
      setShowCartPage(true);
    } else {
      alert("Seu carrinho está vazio! Adicione alguns itens primeiro.");
    }
  };

  const onBackFromCart = () => {
    setShowCartPage(false);
  };

  // Resetar app para nova compra
  const restartApp = () => {
    setSelectedCar(null);
    setSelectedParts({});
    setPricing(null);
    setPurchaseResult(null);
    setShowCartPage(false);
  };

  const handleCarSelect = async (car) => {
    setSelectedCar(car);
    setSelectedParts({});
    setPricing(null);
    setLoading(true);
    setError(null);

    try {
      console.log("🔧 Buscando peças para o carro:", car);

      const response = await carService.getPecas(car.id);

      console.log("✅ Peças encontradas:", response.data);
      setParts(response.data.data || []);

      if (!response.data.data || response.data.data.length === 0) {
        setError("Nenhuma peça encontrada para este carro");
      }
    } catch (err) {
      console.error("❌ Erro ao buscar peças:", err);
      setError(
        `Erro ao buscar peças: ${err.response?.data?.message || err.message}`
      );
      setParts([]);
    } finally {
      setLoading(false);
    }
  };

  const handlePartQuantityChange = (partId, quantity) => {
    // Garantir que partId seja sempre string para consistência
    const normalizedPartId = String(partId);
    const newSelectedParts = { ...selectedParts };

    if (quantity > 0) {
      newSelectedParts[normalizedPartId] = quantity;
    } else {
      delete newSelectedParts[normalizedPartId];
    }

    console.log("🔧 handlePartQuantityChange - partId:", partId, "normalizedPartId:", normalizedPartId, "quantity:", quantity);
    console.log("🔧 newSelectedParts:", newSelectedParts);

    setSelectedParts(newSelectedParts);
  };

  //cálculo de preços em tempo real via Microsserviço B
  useEffect(() => {
    const calculatePricing = async () => {
      const selectedPartsList = Object.entries(selectedParts);

      if (selectedPartsList.length === 0) {
        setPricing(null);
        setPricingError(null);
        return;
      }

      setPricingLoading(true);
      setPricingError(null);

      try {
        // Formatar itens para o Microsserviço B
        const items = apiUtils.formatItemsForCalculation(selectedParts, parts);

        console.log("💰 Enviando para Microsserviço B:", items);

        // Chamar Microsserviço B para cálculo
        const response = await calculationService.calculatePrice(items);

        console.log("✅ Preço calculado pelo Microsserviço B:", response.data);

        if (response.data.status === 'success') {
          setPricing(response.data.data);
        } else {
          setPricingError(response.data.message);
          setPricing(null);
        }
      } catch (err) {
        console.error("❌ Erro ao calcular preço via Microsserviço B:", err);
        setPricingError(err.response?.data?.message || err.message);
        setPricing(null);
      } finally {
        setPricingLoading(false);
      }
    };

    const timeoutId = setTimeout(calculatePricing, 500);

    return () => clearTimeout(timeoutId);
  }, [selectedParts, parts]);

  const getMaxQuantity = (part) => {
    // Regra: somente 1 chassi
    if (part.nome.toLowerCase().includes("chassi")) {
      return 1;
    }
    // Outras peças: máximo 5
    return 4;
  };

  const getTotalItems = () => {
    return Object.values(selectedParts).reduce((sum, qty) => sum + qty, 0);
  };

  const handlePurchase = async () => {
    if (!pricing || getTotalItems() === 0) return;

    setPurchaseLoading(true);

    try {
      // Formatar itens para o Microsserviço B
      const items = apiUtils.formatItemsForCalculation(selectedParts, parts);

      console.log('🛒 Enviando pedido para Microsserviço B:', { items });

      // Criar pedido via Microsserviço B
      const response = await pedidoService.create({ items });

      if (response.data.status === 'success') {
        console.log('✅ Pedido criado via Microsserviço B:', response.data);

        // Formatar resposta para o componente de confirmação
        const orderData = response.data.data;
        const mockResponse = {
          pedidoId: orderData.pedido_id,
          status: 'Confirmado',
          dataPedido: orderData.data_pedido,
          subtotal: pricing.subtotal,
          frete: pricing.frete,
          valorTotal: pricing.total,
          relatorio: orderData.relatorio,
          itensComprados: orderData.relatorio.itens.map(item => ({
            quantidade: item.quantidade,
            peca: {
              nome: item.nome_peca,
              valor: item.valor_unitario
            }
          }))
        };

        setPurchaseResult(mockResponse);
        setShowPurchasePage(true);
      } else {
        throw new Error(response.data.message || 'Erro ao criar pedido');
      }

    } catch (error) {
      console.error('❌ Erro ao finalizar compra via Microsserviço B:', error);
      alert(`Erro ao finalizar compra: ${error.response?.data?.message || error.message}`);
    } finally {
      setPurchaseLoading(false);
    }
  };

  if (showCartPage) {
    return (
      <CartPage
        pricing={pricing}
        selectedParts={selectedParts}
        parts={parts}
        onBack={onBackFromCart}
        purchaseResult={purchaseResult}
        setPurchaseResult={setPurchaseResult}
        getTotalItems={getTotalItems}
        setPurchaseLoading={() => { }}
        returnHome={restartApp}

      />
    );
  }

  return (
    <div className="app">
      {/* Header Verde */}
      <header className="header">
        <h1>🚗 Catálogo de Peças Automotivas</h1>
         <button className="cart" onClick={onOpenCart}>
          <span className="cart-icon">🛒</span>
          <span className="cart-count">{getTotalItems()}</span>
        </button>
        {getTotalItems() > 0 && (
          <div style={{ fontSize: "0.9rem", opacity: 0.9 }}>
            {getTotalItems()} item(s) selecionado(s)
          </div>
        )}
      </header>

      <div className="main-content">
        {/* Sidebar Verde Claro */}
        <aside className="sidebar">
          <h2>Selecione um Carro</h2>
          {carsLoading ? (
            <div className="loading">🔄 Carregando carros...</div>
          ) : error ? (
            <div className="error-message">
              <p>❌ {error}</p>
              <p style={{ fontSize: '0.9rem', marginTop: '10px' }}>
                Verifique se a API Django está rodando em localhost:8000
              </p>
            </div>
          ) : cars.length === 0 ? (
            <div className="empty-state">
              <p>📭 Nenhum carro encontrado</p>
              <p style={{ fontSize: '0.9rem', marginTop: '10px' }}>
                Cadastre carros no Django Admin primeiro
              </p>
            </div>
          ) : (
            <div className="car-list">
              {cars.map((car) => (
                <div
                  key={car.id}
                  className={`car-card ${selectedCar?.id === car.id ? "selected" : ""
                    }`}
                  onClick={() => handleCarSelect(car)}
                >
                  <h3>{car.modelo}</h3>
                  <p>Ano: {car.ano}</p>
                </div>
              ))}
            </div>
          )}

          {/* Resumo do Orçamento na Sidebar */}
          {pricing && (
            <div className="pricing-summary">
              <h3>💰 Orçamento</h3>
              <div className="pricing-details">
                <div className="pricing-line">
                  <span>Subtotal:</span>
                  <span>R$ {(pricing.subtotal || 0).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</span>
                </div>
                <div className="pricing-line">
                  <span>Frete:</span>
                  <span>R$ {(pricing.frete || 0).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</span>
                </div>
                <div className="pricing-total">
                  <span>Total:</span>
                  <span>R$ {(pricing.total || 0).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</span>
                </div>
              </div>

              {getTotalItems() > 0 && (
                <button
                  className="purchase-button"
                  onClick={onOpenCart}
                  disabled={purchaseLoading}
                  style={{
                    width: '100%',
                    padding: '12px',
                    marginTop: '15px',
                    backgroundColor: '#28a745',
                    color: 'white',
                    border: 'none',
                    borderRadius: '8px',
                    fontSize: '16px',
                    fontWeight: 'bold',
                    cursor: purchaseLoading ? 'not-allowed' : 'pointer',
                    opacity: purchaseLoading ? 0.7 : 1
                  }}
                >
                  {purchaseLoading ? '🔄 Processando...' : '🛒 Ver Carrinho'}
                </button>
              )}
            </div>
          )}

          {pricingLoading && (
            <div className="pricing-loading">
              <p>🔄 Calculando preço...</p>
            </div>
          )}

          {pricingError && (
            <div className="pricing-error">
              <p>❌ {pricingError}</p>
            </div>
          )}
        </aside>

        {/* Conteúdo Principal */}
        <main className="content">
          {!selectedCar && (
            <div
              style={{ textAlign: "center", padding: "3rem", color: "#666" }}
            >
              <h2>👈 Selecione um carro na barra lateral</h2>
              <p>Escolha um modelo para ver as peças disponíveis</p>
            </div>
          )}

          {selectedCar && (
            <div>
              <h1>
                Peças para {selectedCar.modelo.toUpperCase()} ({selectedCar.ano}
                )
              </h1>

              {loading && (
                <div className="loading">
                  <p>🔄 Carregando peças...</p>
                </div>
              )}

              {error && (
                <div className="error">
                  <p>{error}</p>
                  <small>
                    Verifique se o P-Api está rodando em http://127.0.0.1:8000
                  </small>
                </div>
              )}

              {!loading && !error && parts.length > 0 && (
                <div className="parts-list">
                  <h2>Peças Disponíveis ({parts.length})</h2>
                  <p style={{ color: "#666", marginBottom: "1rem" }}>
                    Selecione as peças e quantidades desejadas. O preço será
                    calculado em tempo real.
                  </p>

                  <div className="parts-grid">
                    {parts.map((part) => {
                      const maxQty = getMaxQuantity(part);
                      const currentQty = selectedParts[part.id] || 0;

                      return (
                        <div key={part.id} className="part-card interactive">
                          <h4>{part.nome}</h4>
                          <div className="price">
                            R${" "}
                            {part.valor.toLocaleString("pt-BR", {
                              minimumFractionDigits: 2,
                              maximumFractionDigits: 2,
                            })}
                          </div>
                          <div className="id">ID: {part.id}</div>

                          <div className="quantity-controls">
                            <label>Quantidade:</label>
                            <div className="quantity-input">
                              <button
                                onClick={() =>
                                  handlePartQuantityChange(
                                    part.id,
                                    Math.max(0, currentQty - 1)
                                  )
                                }
                                disabled={currentQty <= 0}
                                className="qty-btn"
                              >
                                -
                              </button>
                              <span className="qty-display">{currentQty}</span>
                              <button
                                onClick={() =>
                                  handlePartQuantityChange(
                                    part.id,
                                    Math.min(maxQty, currentQty + 1)
                                  )
                                }
                                disabled={currentQty >= maxQty}
                                className="qty-btn"
                              >
                                +
                              </button>
                            </div>
                            {maxQty === 1 && (
                              <small
                                style={{ color: "#999", fontSize: "0.8rem" }}
                              >
                                Máximo: 1 unidade
                              </small>
                            )}
                            {currentQty > 0 && (
                              <div className="item-total">
                                Subtotal: R${" "}
                                {(part.valor * currentQty).toLocaleString(
                                  "pt-BR",
                                  {
                                    minimumFractionDigits: 2,
                                  }
                                )}
                              </div>
                            )}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}

              {!loading && !error && parts.length === 0 && selectedCar && (
                <div
                  style={{
                    textAlign: "center",
                    padding: "2rem",
                    color: "#666",
                  }}
                >
                  <p>Nenhuma peça encontrada para este modelo.</p>
                </div>
              )}
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
