from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json

# Importar os clientes dos microsserviços
from microservices.service_a import microservice_a
from microservices.service_b import microservice_b

# Importações mantidas para compatibilidade
from .models import Car, Peca, Pedido, ItemPedido
from .serializers import CarSerializer, PecaSerializer, PedidoSerializer, PedidoListSerializer

# ========== GATEWAY VIEWS - CARROS (via Microsserviço A) ==========

@api_view(['GET'])
def car_list(request):
    """
    Lista todos os carros via Microsserviço A
    GET /api/cars/
    """
    try:
        result = microservice_a.get_cars()
        
        if result['status'] == 'success':
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Erro no gateway: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def car_detail(request, car_id):
    """
    Retorna detalhes de um carro específico via Microsserviço A
    GET /api/cars/{id}/
    """
    try:
        result = microservice_a.get_car_by_id(car_id)
        
        if result['status'] == 'success':
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_404_NOT_FOUND)
            
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Erro no gateway: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def car_pecas(request, car_id):
    """
    Lista todas as peças de um carro específico via Microsserviço A
    GET /api/cars/{id}/pecas/
    """
    try:
        result = microservice_a.get_car_parts(car_id)
        
        if result['status'] == 'success':
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_404_NOT_FOUND)
            
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Erro no gateway: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ========== GATEWAY VIEWS - PEÇAS (via Microsserviço A) ==========

@api_view(['GET'])
def peca_list(request):
    """
    Lista todas as peças via Microsserviço A
    GET /api/pecas/
    """
    try:
        # Extrair filtros dos query parameters
        filters = {
            'nome': request.GET.get('nome'),
            'car_id': request.GET.get('car_id'),
            'min_valor': request.GET.get('min_valor'),
            'max_valor': request.GET.get('max_valor'),
        }
        
        # Remover filtros vazios
        filters = {k: v for k, v in filters.items() if v is not None}
        
        result = microservice_a.get_parts(filters)
        
        if result['status'] == 'success':
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Erro no gateway: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def peca_detail(request, peca_id):
    """
    Retorna detalhes de uma peça específica via Microsserviço A
    GET /api/pecas/{id}/
    """
    try:
        result = microservice_a.get_part_by_id(peca_id)
        
        if result['status'] == 'success':
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_404_NOT_FOUND)
            
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Erro no gateway: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ========== GATEWAY VIEWS - CÁLCULOS E PEDIDOS (via Microsserviço B) ==========

@api_view(['POST'])
@csrf_exempt
def calculate_price(request):
    """
    Calcular preço total via Microsserviço B
    POST /api/calculate-price/
    Body: {
        "items": [
            {"peca_id": 1, "quantidade": 2},
            {"peca_id": 3, "quantidade": 1}
        ]
    }
    """
    try:
        data = json.loads(request.body) if request.body else {}
        items = data.get('items', [])
        
        if not items:
            return Response({
                'status': 'error',
                'message': 'Lista de itens é obrigatória'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        result = microservice_b.calculate_price(items)
        
        if result['status'] == 'success':
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
            
    except json.JSONDecodeError:
        return Response({
            'status': 'error',
            'message': 'JSON inválido'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Erro no gateway: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@csrf_exempt
def create_order(request):
    """
    Criar pedido via Microsserviço B
    POST /api/orders/
    Body: {
        "items": [
            {"peca_id": 1, "quantidade": 2},
            {"peca_id": 3, "quantidade": 1}
        ]
    }
    """
    try:
        data = json.loads(request.body) if request.body else {}
        
        # Validar dados
        validation = microservice_b.validate_order_data(data)
        if validation['status'] != 'success':
            return Response(validation, status=status.HTTP_400_BAD_REQUEST)
        
        # Criar pedido
        result = microservice_b.create_order(data)
        
        if result['status'] == 'success':
            return Response(result, status=status.HTTP_201_CREATED)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
            
    except json.JSONDecodeError:
        return Response({
            'status': 'error',
            'message': 'JSON inválido'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Erro no gateway: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def order_report(request, order_id):
    """
    Gerar relatório de pedido via Microsserviço B
    GET /api/orders/{order_id}/report/
    """
    try:
        result = microservice_b.get_order_report(order_id)
        
        if result['status'] == 'success':
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_404_NOT_FOUND)
            
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Erro no gateway: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@csrf_exempt
def generate_order_id(request):
    """
    Gerar ID único para pedido via Microsserviço B
    POST /api/generate-order-id/
    """
    try:
        result = microservice_b.generate_order_id()
        
        if result['status'] == 'success':
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Erro no gateway: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ========== GATEWAY VIEWS - UTILITÁRIAS ==========

@api_view(['GET'])
def health_check(request):
    """
    Health check do gateway e microsserviços
    GET /api/health/
    """
    try:
        # Testar Microsserviço A
        cars_result = microservice_a.get_cars()
        service_a_status = cars_result['status'] == 'success'
        
        # Testar Microsserviço B
        order_id_result = microservice_b.generate_order_id()
        service_b_status = order_id_result['status'] == 'success'
        
        overall_status = service_a_status and service_b_status
        
        return Response({
            'status': 'success' if overall_status else 'warning',
            'gateway': 'online',
            'microservices': {
                'service_a': 'online' if service_a_status else 'offline',
                'service_b': 'online' if service_b_status else 'offline'
            },
            'timestamp': str(timezone.now())
        }, status=status.HTTP_200_OK if overall_status else status.HTTP_503_SERVICE_UNAVAILABLE)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Erro no health check: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

