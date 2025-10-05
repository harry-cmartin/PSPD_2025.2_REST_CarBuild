"""
Microsserviço A - Gerenciamento de Banco de Dados
Responsável por: Carros, Peças, operações CRUD no banco
"""

import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from car.models import Car, Peca
from car.serializers import CarSerializer, PecaSerializer
import json
import logging

logger = logging.getLogger(__name__)

class MicroserviceAClient:
    """Cliente para comunicação com Microsserviço A (Banco de Dados)"""
    
    def __init__(self):
        # Por enquanto, vamos simular que o microsserviço A está no mesmo processo
        # Em produção, seria uma URL externa como http://microservice-a:8001
        self.base_url = getattr(settings, 'MICROSERVICE_A_URL', 'internal')
        
    def get_cars(self):
        """Buscar todos os carros"""
        try:
            if self.base_url == 'internal':
                # Simulando chamada interna
                cars = Car.objects.all()
                serializer = CarSerializer(cars, many=True)
                return {
                    'status': 'success',
                    'data': serializer.data,
                    'count': len(serializer.data)
                }
            else:
                # Chamada HTTP real para microsserviço externo
                response = requests.get(f"{self.base_url}/cars/", timeout=10)
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"Erro ao buscar carros: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'data': []
            }
    
    def get_car_by_id(self, car_id):
        """Buscar carro por ID"""
        try:
            if self.base_url == 'internal':
                car = get_object_or_404(Car, id=car_id)
                serializer = CarSerializer(car)
                return {
                    'status': 'success',
                    'data': serializer.data
                }
            else:
                response = requests.get(f"{self.base_url}/cars/{car_id}/", timeout=10)
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"Erro ao buscar carro {car_id}: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def get_car_parts(self, car_id):
        """Buscar peças de um carro específico"""
        try:
            if self.base_url == 'internal':
                car = get_object_or_404(Car, id=car_id)
                parts = car.pecas.all()
                serializer = PecaSerializer(parts, many=True)
                return {
                    'status': 'success',
                    'data': serializer.data,
                    'car': CarSerializer(car).data,
                    'count': len(serializer.data)
                }
            else:
                response = requests.get(f"{self.base_url}/cars/{car_id}/parts/", timeout=10)
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"Erro ao buscar peças do carro {car_id}: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'data': []
            }
    
    def get_parts(self, filters=None):
        """Buscar peças com filtros opcionais"""
        try:
            if self.base_url == 'internal':
                queryset = Peca.objects.all()
                
                if filters:
                    if filters.get('nome'):
                        queryset = queryset.filter(nome__icontains=filters['nome'])
                    if filters.get('car_id'):
                        queryset = queryset.filter(owner_id=filters['car_id'])
                    if filters.get('min_valor'):
                        queryset = queryset.filter(valor__gte=filters['min_valor'])
                    if filters.get('max_valor'):
                        queryset = queryset.filter(valor__lte=filters['max_valor'])
                
                serializer = PecaSerializer(queryset, many=True)
                return {
                    'status': 'success',
                    'data': serializer.data,
                    'count': len(serializer.data),
                    'filters_applied': filters or {}
                }
            else:
                params = filters or {}
                response = requests.get(f"{self.base_url}/parts/", params=params, timeout=10)
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"Erro ao buscar peças: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'data': []
            }
    
    def get_part_by_id(self, part_id):
        """Buscar peça por ID"""
        try:
            if self.base_url == 'internal':
                part = get_object_or_404(Peca, id=part_id)
                serializer = PecaSerializer(part)
                return {
                    'status': 'success',
                    'data': serializer.data
                }
            else:
                response = requests.get(f"{self.base_url}/parts/{part_id}/", timeout=10)
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"Erro ao buscar peça {part_id}: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }

# Instância global do cliente
microservice_a = MicroserviceAClient()