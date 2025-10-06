import React, { useState } from "react";
import "./CartPage.css";
import "./App.js";
import axios from "axios";


function CartPage({ pricing, selectedParts, parts, onBack, purchaseResult, setPurchaseResult, getTotalItems, setPurchaseLoading, returnHome }) {
    const [showConfirmation, setShowConfirmation] = useState(false);
    //   const [purchaseResult, setPurchaseResult] = useState(initialPurchaseResult || null);

    // Debug logs
    console.log("🛒 CartPage - selectedParts:", selectedParts);
    console.log("🛒 CartPage - parts:", parts);
    console.log("🛒 CartPage - pricing:", pricing);
    console.log("🛒 CartPage - pricing.subtotal:", pricing?.subtotal, "pricing.frete:", pricing?.frete, "pricing.total:", pricing?.total);

    // Itens selecionados
    const itensSelecionados = Object.entries(selectedParts).map(([id, qtd]) => {
        // Buscar peça por ID - compatível com string e number
        const peca = parts.find((p) => String(p.id) === String(id));
        console.log(`🔍 Buscando peça - ID procurado: ${id} (${typeof id}), peças disponíveis:`, parts.map(p => `${p.id} (${typeof p.id}): ${p.nome}`));
        console.log(`🔍 Peça encontrada:`, peca);
        
        if (!peca) {
            console.warn(`⚠️ Peça não encontrada para ID: ${id}`);
            return { id, quantidade: qtd, nome: `Peça ID ${id} (não encontrada)`, valor: 0 };
        }
        
        return { ...peca, quantidade: qtd };
    });

    const total = (pricing?.subtotal || 0) + (pricing?.frete || 0);

    const Return = () => {
        returnHome();
        onBack();
    }

    // Componente de confirmação de compra
    const PurchaseConfirmation = ({ purchaseResult }) => {
        if (!purchaseResult) return null;

        // Os dados vêm do backend no formato:
        // { pedido_id, valor_total, data_pedido, relatorio: { id_pedido, data_pedido, itens, valor_total } }
        const relatorio = purchaseResult.relatorio || {};

        return (
            <div className="purchase-confirmation">
                <header className="header">
                    <h1>✅ Compra Realizada com Sucesso!</h1>
                </header>

                <div className="main-content">
                    <div className="purchase-details">
                        <div className="order-summary">
                            <h2>Pedido: {purchaseResult.pedido_id}</h2>
                            <div className="order-info">
                                <p><strong>Status:</strong> Confirmado</p>
                                <p><strong>Data:</strong> {relatorio.data_pedido || new Date(purchaseResult.data_pedido).toLocaleString('pt-BR')}</p>
                            </div>

                            <div className="pricing-breakdown">
                                <h3>💰 Resumo Financeiro</h3>
                                <div className="pricing-total">
                                    <span>Total Pago:</span>
                                    <span>R$ {(purchaseResult.valor_total || relatorio.valor_total || 0).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</span>
                                </div>
                            </div>

                            <div className="items-purchased">
                                <h3>📦 Itens Comprados</h3>
                                {(relatorio.itens || []).map((item, index) => (
                                    <div key={index} className="purchased-item">
                                        <span className="item-qty">{item.quantidade}x</span>
                                        <span className="item-name">{item.nome_peca}</span>
                                        <span className="item-price">R$ {(item.subtotal || 0).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</span>
                                    </div>
                                ))}
                            </div>

                            <div className="button-wrapper">
                                <button className="return-home" onClick={Return}>
                                    🏠 Página inicial
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    };

    const handleConfirmPurchase = async () => {
        if (!pricing || getTotalItems() === 0) return;

        setPurchaseLoading(true);

        try {
            // Monta os itens do pedido no formato esperado pelo Microsserviço B
            const items = Object.entries(selectedParts).map(([partId, quantidade]) => {
                const part = parts.find(p => String(p.id) === String(partId));
                if (!part) {
                    console.warn(`⚠️ Peça não encontrada para ID: ${partId} ao criar pedido`);
                    return null;
                }
                return {
                    peca_id: parseInt(partId), // Microsserviço B espera peca_id como int
                    quantidade: quantidade
                };
            }).filter(item => item !== null);

            console.log("🛒 Enviando pedido para API:", { items });

            // Chamada para o endpoint correto da API
            const response = await axios.post('http://localhost:8000/api/orders/', {
                items: items
            });

            console.log("✅ Resposta da API:", response.data);

            // Salva o resultado da compra
            setPurchaseResult(response.data.data); // A resposta vem em response.data.data

            // Mostra a tela de confirmação
            setShowConfirmation(true);

        } catch (error) {
            console.error('❌ Erro ao finalizar compra:', error);
            console.error('❌ Resposta do erro:', error.response?.data);
            
            const errorMessage = error.response?.data?.message || 
                               error.response?.data?.detail || 
                               error.message || 
                               'Erro desconhecido ao finalizar compra';
            
            alert(`Erro ao finalizar compra: ${errorMessage}`);
        } finally {
            setPurchaseLoading(false);
        }
    };

    // Renderiza carrinho ou confirmação
    if (showConfirmation && purchaseResult) {
        return <PurchaseConfirmation purchaseResult={purchaseResult} />;
    }

    return (
        <div className="cart-page">
            <header className="cart-header">
                <button onClick={onBack} className="back-button">⬅️</button>
                <h1>🛒 Meu Carrinho</h1>
            </header>

            <main className="cart-content">
                {itensSelecionados.length === 0 ? (
                    <p className="empty-cart">Seu carrinho está vazio.</p>
                ) : (
                    <div className="cart-details">
                        <h2>Itens Selecionados</h2>
                        <ul className="cart-items-list">
                            {itensSelecionados.map((item, index) => (
                                <li key={item.id || index} className="cart-item">
                                    <span>{item.quantidade}x {item.nome || 'Nome não encontrado'}</span>
                                    <strong>R$ {((item.valor || 0) * item.quantidade).toLocaleString("pt-BR", { minimumFractionDigits: 2 })}</strong>
                                </li>
                            ))}
                        </ul>

                        <div className="cart-summary">
                            <p>Subtotal: <strong>R$ {(pricing?.subtotal || 0).toLocaleString("pt-BR", { minimumFractionDigits: 2 })}</strong></p>
                            <p>Frete: <strong>R$ {(pricing?.frete || 0).toLocaleString("pt-BR", { minimumFractionDigits: 2 })}</strong></p>
                            <p className="cart-total">💰 Total: <strong>R$ {(pricing?.total || 0).toLocaleString("pt-BR", { minimumFractionDigits: 2 })}</strong></p>
                        </div>

                        <button className="finalize-button" onClick={handleConfirmPurchase}>
                            Confirmar Compra
                        </button>
                    </div>
                )}
            </main>
        </div>
    );
}

export default CartPage;
