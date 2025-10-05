"""
Microsserviço B - Cálculos e Pedidos
Responsável por: Cálculo de preços, geração de IDs únicos, relatórios de pedidos
"""

import requests
import uuid
from decimal import Decimal
from datetime import datetime
from django.conf import settings
from django.http import JsonResponse
from car.models import Pedido, ItemPedido, Peca
from car.serializers import PedidoSerializer, ItemPedidoSerializer
import json
import logging

logger = logging.getLogger(__name__)

class MicroserviceBClient:
    """Cliente para comunicação com Microsserviço B (Cálculos e Pedidos)"""
    
    def __init__(self):
        # Por enquanto, vamos simular que o microsserviço B está no mesmo processo
        # Em produção, seria uma URL externa como http://microservice-b:8002
        self.base_url = getattr(settings, 'MICROSERVICE_B_URL', 'internal')
        
        # Configurações de negócio
        self.frete_gratis_valor = getattr(settings, 'FRETE_GRATIS_VALOR', 200)
        self.valor_frete = getattr(settings, 'VALOR_FRETE', 25)
        
    def calculate_price(self, items_data):
        """
        Calcular preço total dos itens
        items_data: [{'peca_id': 1, 'quantidade': 2}, ...]
        """
        try:
            if self.base_url == 'internal':
                total_subtotal = Decimal('0.00')
                items_details = []
                
                for item in items_data:
                    try:
                        peca = Peca.objects.get(id=item['peca_id'])
                        quantidade = int(item['quantidade'])
                        subtotal = peca.valor * quantidade
                        total_subtotal += subtotal
                        
                        items_details.append({
                            'peca_id': peca.id,
                            'peca_nome': peca.nome,
                            'peca_valor': float(peca.valor),
                            'quantidade': quantidade,
                            'subtotal': float(subtotal)
                        })
                    except Peca.DoesNotExist:
                        return {
                            'status': 'error',
                            'message': f'Peça com ID {item["peca_id"]} não encontrada'
                        }
                
                # Calcular frete
                frete = Decimal('0.00') if total_subtotal >= self.frete_gratis_valor else Decimal(str(self.valor_frete))
                total_final = total_subtotal + frete
                
                return {
                    'status': 'success',
                    'data': {
                        'subtotal': float(total_subtotal),
                        'frete': float(frete),
                        'total': float(total_final),
                        'frete_gratis': total_subtotal >= self.frete_gratis_valor,
                        'items': items_details
                    }
                }
            else:
                # Chamada HTTP real para microsserviço externo
                response = requests.post(
                    f"{self.base_url}/calculate-price/",
                    json={'items': items_data},
                    timeout=10
                )
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"Erro ao calcular preço: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def generate_order_id(self):
        """Gerar ID único para pedido"""
        try:
            if self.base_url == 'internal':
                # Gerar UUID único
                order_id = str(uuid.uuid4())
                return {
                    'status': 'success',
                    'data': {
                        'order_id': order_id,
                        'generated_at': datetime.now().isoformat()
                    }
                }
            else:
                response = requests.post(f"{self.base_url}/generate-order-id/", timeout=10)
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"Erro ao gerar ID do pedido: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def create_order(self, order_data):
        """
        Criar pedido completo
        order_data: {
            'items': [{'peca_id': 1, 'quantidade': 2}],
            'valor_total': 150.00
        }
        """
        try:
            if self.base_url == 'internal':
                # Criar pedido
                pedido = Pedido.objects.create()
                
                # Adicionar itens
                for item_data in order_data['items']:
                    peca = Peca.objects.get(id=item_data['peca_id'])
                    ItemPedido.objects.create(
                        pedido=pedido,
                        peca=peca,
                        quantidade=item_data['quantidade']
                    )
                
                # Calcular total
                pedido.calcular_total()
                
                # Gerar relatório
                relatorio = pedido.gerar_relatorio()
                
                return {
                    'status': 'success',
                    'data': {
                        'pedido_id': str(pedido.id_unico),
                        'valor_total': float(pedido.valor_total),
                        'data_pedido': pedido.data_pedido.isoformat(),
                        'relatorio': relatorio
                    }
                }
            else:
                response = requests.post(
                    f"{self.base_url}/create-order/",
                    json=order_data,
                    timeout=10
                )
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"Erro ao criar pedido: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def get_order_report(self, order_id):
        """Gerar relatório de um pedido específico"""
        try:
            if self.base_url == 'internal':
                try:
                    pedido = Pedido.objects.get(id_unico=order_id)
                    relatorio = pedido.gerar_relatorio()
                    
                    return {
                        'status': 'success',
                        'data': relatorio
                    }
                except Pedido.DoesNotExist:
                    return {
                        'status': 'error',
                        'message': f'Pedido {order_id} não encontrado'
                    }
            else:
                response = requests.get(f"{self.base_url}/orders/{order_id}/report/", timeout=10)
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"Erro ao gerar relatório do pedido {order_id}: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def validate_order_data(self, order_data):
        """Validar dados do pedido antes de criar"""
        try:
            if not order_data.get('items'):
                return {
                    'status': 'error',
                    'message': 'Lista de itens é obrigatória'
                }
            
            if not isinstance(order_data['items'], list):
                return {
                    'status': 'error',
                    'message': 'Items deve ser uma lista'
                }
            
            for item in order_data['items']:
                if not item.get('peca_id') or not item.get('quantidade'):
                    return {
                        'status': 'error',
                        'message': 'Cada item deve ter peca_id e quantidade'
                    }
                
                if item['quantidade'] <= 0:
                    return {
                        'status': 'error',
                        'message': 'Quantidade deve ser maior que 0'
                    }
            
            return {
                'status': 'success',
                'message': 'Dados válidos'
            }
            
        except Exception as e:
            logger.error(f"Erro na validação: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }

# Instância global do cliente
microservice_b = MicroserviceBClient()