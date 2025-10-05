from django.urls import path
from .views import (
    # Views de carros (Microsserviço A)
    car_list,
    car_detail,
    car_pecas,
    
    # Views de peças (Microsserviço A)
    peca_list,
    peca_detail,
    
    # Views de cálculos e pedidos (Microsserviço B)
    calculate_price,
    create_order,
    order_report,
    generate_order_id,
    
    # Views utilitárias
    health_check,
)

urlpatterns = [
    # ========== ENDPOINTS - CARROS (Microsserviço A) ==========
    path('cars/', car_list, name='car_list'),
    path('cars/<int:car_id>/', car_detail, name='car_detail'),
    path('cars/<int:car_id>/pecas/', car_pecas, name='car_pecas'),
    
    # ========== ENDPOINTS - PEÇAS (Microsserviço A) ==========
    path('pecas/', peca_list, name='peca_list'),
    path('pecas/<int:peca_id>/', peca_detail, name='peca_detail'),
    
    # ========== ENDPOINTS - CÁLCULOS E PEDIDOS (Microsserviço B) ==========
    path('calculate-price/', calculate_price, name='calculate_price'),
    path('orders/', create_order, name='create_order'),
    path('orders/<str:order_id>/report/', order_report, name='order_report'),
    path('generate-order-id/', generate_order_id, name='generate_order_id'),
    
    # ========== ENDPOINTS - UTILITÁRIOS ==========
    path('health/', health_check, name='health_check'),
]