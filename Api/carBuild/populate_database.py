#!/usr/bin/env python
"""
Script para popular o banco de dados com dados de exemplo.

Uso:
1. Via comando Django: python manage.py populate_db
2. Via script direto: python populate_database.py

Opções:
- --clear: Limpa dados existentes antes de popular
- --cars-only: Popula apenas carros e peças (sem pedidos)
"""

import os
import sys
import django
from decimal import Decimal
import random

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carBuild.settings')
django.setup()

# Importar modelos após configurar Django
from car.models import Car, Peca, Pedido, ItemPedido
from django.db import transaction

def limpar_dados():
    """Limpa todos os dados do banco"""
    print('🗑️  Limpando dados existentes...')
    ItemPedido.objects.all().delete()
    Pedido.objects.all().delete()
    Peca.objects.all().delete()
    Car.objects.all().delete()
    print('✅ Dados limpos com sucesso!')

def criar_carros():
    """Cria carros de exemplo"""
    print('🚗 Criando carros...')
    
    cars_data = [
        {'modelo': 'Civic', 'ano': 2020},
        {'modelo': 'Corolla', 'ano': 2019},
        {'modelo': 'Fusca', 'ano': 1970},
        {'modelo': 'Gol', 'ano': 2018},
        {'modelo': 'Onix', 'ano': 2021},
        {'modelo': 'HB20', 'ano': 2020},
        {'modelo': 'Polo', 'ano': 2019},
        {'modelo': 'Fiesta', 'ano': 2017},
        {'modelo': 'Uno', 'ano': 2016},
        {'modelo': 'Palio', 'ano': 2015},
    ]

    cars = []
    for car_data in cars_data:
        car, created = Car.objects.get_or_create(
            modelo=car_data['modelo'],
            ano=car_data['ano']
        )
        if created:
            cars.append(car)
            print(f'  ✓ {car.modelo} ({car.ano})')

    print(f'🚗 Criados {len(cars)} carros')
    return Car.objects.all()

def criar_pecas(cars):
    """Cria peças de exemplo para os carros"""
    print('🔧 Criando peças...')
    
    pecas_genericas = [
        {'nome': 'Filtro de Ar', 'valor_min': 25.00, 'valor_max': 60.00},
        {'nome': 'Filtro de Óleo', 'valor_min': 15.00, 'valor_max': 40.00},
        {'nome': 'Filtro de Combustível', 'valor_min': 30.00, 'valor_max': 80.00},
        {'nome': 'Pastilha de Freio Dianteira', 'valor_min': 80.00, 'valor_max': 200.00},
        {'nome': 'Pastilha de Freio Traseira', 'valor_min': 60.00, 'valor_max': 150.00},
        {'nome': 'Disco de Freio Dianteiro', 'valor_min': 120.00, 'valor_max': 300.00},
        {'nome': 'Disco de Freio Traseiro', 'valor_min': 100.00, 'valor_max': 250.00},
        {'nome': 'Vela de Ignição', 'valor_min': 20.00, 'valor_max': 50.00},
        {'nome': 'Correia Dentada', 'valor_min': 40.00, 'valor_max': 120.00},
        {'nome': 'Bomba de Combustível', 'valor_min': 200.00, 'valor_max': 500.00},
        {'nome': 'Radiador', 'valor_min': 300.00, 'valor_max': 800.00},
        {'nome': 'Alternador', 'valor_min': 250.00, 'valor_max': 600.00},
        {'nome': 'Motor de Arranque', 'valor_min': 200.00, 'valor_max': 500.00},
        {'nome': 'Amortecedor Dianteiro', 'valor_min': 150.00, 'valor_max': 400.00},
        {'nome': 'Amortecedor Traseiro', 'valor_min': 120.00, 'valor_max': 350.00},
        {'nome': 'Pneu 175/70 R13', 'valor_min': 200.00, 'valor_max': 400.00},
        {'nome': 'Pneu 185/60 R15', 'valor_min': 300.00, 'valor_max': 600.00},
        {'nome': 'Bateria 60Ah', 'valor_min': 180.00, 'valor_max': 300.00},
        {'nome': 'Bateria 70Ah', 'valor_min': 220.00, 'valor_max': 400.00},
        {'nome': 'Óleo Motor 5W30 (1L)', 'valor_min': 35.00, 'valor_max': 60.00},
        {'nome': 'Óleo Motor 10W40 (1L)', 'valor_min': 30.00, 'valor_max': 50.00},
        {'nome': 'Fluido de Freio DOT4', 'valor_min': 15.00, 'valor_max': 35.00},
        {'nome': 'Aditivo Radiador', 'valor_min': 12.00, 'valor_max': 30.00},
        {'nome': 'Lâmpada H4', 'valor_min': 25.00, 'valor_max': 80.00},
        {'nome': 'Lâmpada H7', 'valor_min': 30.00, 'valor_max': 90.00},
    ]

    pecas_especiais = {
        'Fusca': [
            {'nome': 'Carburador Weber 40', 'valor_min': 400.00, 'valor_max': 800.00},
            {'nome': 'Cilindro Mestre Duplo', 'valor_min': 150.00, 'valor_max': 300.00},
            {'nome': 'Caixa de Fusível 6V', 'valor_min': 80.00, 'valor_max': 200.00},
            {'nome': 'Gerador 6V', 'valor_min': 200.00, 'valor_max': 450.00},
        ],
        'Civic': [
            {'nome': 'Kit Embreagem VTEC', 'valor_min': 600.00, 'valor_max': 1200.00},
            {'nome': 'Sensor MAP Honda', 'valor_min': 120.00, 'valor_max': 250.00},
            {'nome': 'Bobina de Ignição VTEC', 'valor_min': 180.00, 'valor_max': 350.00},
            {'nome': 'ECU Honda Original', 'valor_min': 800.00, 'valor_max': 1500.00},
        ],
        'Corolla': [
            {'nome': 'Kit Embreagem Toyota', 'valor_min': 500.00, 'valor_max': 900.00},
            {'nome': 'Sensor Oxigênio Toyota', 'valor_min': 150.00, 'valor_max': 300.00},
            {'nome': 'Filtro Cabine Toyota', 'valor_min': 40.00, 'valor_max': 80.00},
        ]
    }

    pecas_criadas = []
    
    # Criar peças genéricas para cada carro
    for car in cars:
        # Escolher aleatoriamente 6-10 peças genéricas por carro
        num_pecas = random.randint(6, 10)
        pecas_selecionadas = random.sample(pecas_genericas, min(num_pecas, len(pecas_genericas)))
        
        for peca_data in pecas_selecionadas:
            valor = Decimal(str(round(random.uniform(
                peca_data['valor_min'], 
                peca_data['valor_max']
            ), 2)))
            
            peca, created = Peca.objects.get_or_create(
                nome=peca_data['nome'],
                owner=car,
                defaults={'valor': valor}
            )
            
            if created:
                pecas_criadas.append(peca)
                print(f'  ✓ {peca.nome} para {car.modelo} - R$ {peca.valor}')

        # Adicionar peças especiais se existirem para o modelo
        if car.modelo in pecas_especiais:
            for peca_data in pecas_especiais[car.modelo]:
                valor = Decimal(str(round(random.uniform(
                    peca_data['valor_min'], 
                    peca_data['valor_max']
                ), 2)))
                
                peca, created = Peca.objects.get_or_create(
                    nome=peca_data['nome'],
                    owner=car,
                    defaults={'valor': valor}
                )
                
                if created:
                    pecas_criadas.append(peca)
                    print(f'  ✓ {peca.nome} (especial) para {car.modelo} - R$ {peca.valor}')

    # Criar algumas peças universais (sem owner)
    pecas_universais = [
        {'nome': 'Óleo Motor Universal 20W50 (4L)', 'valor': 45.00},
        {'nome': 'Fluido de Freio Universal DOT4', 'valor': 25.00},
        {'nome': 'Aditivo Combustível Universal', 'valor': 18.00},
        {'nome': 'Cera Automotiva Premium', 'valor': 35.00},
        {'nome': 'Shampoo Automotivo', 'valor': 22.00},
        {'nome': 'Pano de Microfibra', 'valor': 15.00},
        {'nome': 'Aromatizante Vanilla', 'valor': 8.00},
        {'nome': 'Limpa Vidros', 'valor': 12.00},
    ]

    for peca_data in pecas_universais:
        peca, created = Peca.objects.get_or_create(
            nome=peca_data['nome'],
            owner=None,
            defaults={'valor': Decimal(str(peca_data['valor']))}
        )
        
        if created:
            pecas_criadas.append(peca)
            print(f'  ✓ {peca.nome} (universal) - R$ {peca.valor}')

    print(f'🔧 Criadas {len(pecas_criadas)} peças')
    return Peca.objects.all()

def criar_pedidos(pecas):
    """Cria pedidos de exemplo"""
    print('📋 Criando pedidos...')
    
    pedidos_criados = []
    
    # Criar 5-10 pedidos aleatórios
    num_pedidos = random.randint(5, 10)
    
    for i in range(num_pedidos):
        pedido = Pedido.objects.create()
        
        # Adicionar 1-6 itens aleatórios por pedido
        num_itens = random.randint(1, 6)
        pecas_disponiveis = list(pecas)
        pecas_pedido = random.sample(pecas_disponiveis, min(num_itens, len(pecas_disponiveis)))
        
        itens_criados = []
        for peca in pecas_pedido:
            quantidade = random.randint(1, 4)
            
            # Algumas regras de negócio
            if 'chassi' in peca.nome.lower():
                quantidade = 1
            elif 'pneu' in peca.nome.lower():
                quantidade = random.choice([2, 4])  # Pneus geralmente em pares
            elif peca.valor > 500:  # Peças caras
                quantidade = 1
            
            item = ItemPedido.objects.create(
                pedido=pedido,
                peca=peca,
                quantidade=quantidade
            )
            itens_criados.append(item)
        
        # Calcular total do pedido
        pedido.calcular_total()
        pedidos_criados.append(pedido)
        
        print(f'  ✓ Pedido {str(pedido.id_unico)[:8]}... - {len(itens_criados)} itens - R$ {pedido.valor_total}')

    print(f'📋 Criados {len(pedidos_criados)} pedidos')
    return pedidos_criados

def main():
    """Função principal"""
    print('🚀 Iniciando população do banco de dados...\n')
    
    # Verificar argumentos
    clear_data = '--clear' in sys.argv
    cars_only = '--cars-only' in sys.argv
    
    try:
        with transaction.atomic():
            if clear_data:
                limpar_dados()
                print()
            
            # Criar carros
            cars = criar_carros()
            print()
            
            # Criar peças
            pecas = criar_pecas(cars)
            print()
            
            if not cars_only:
                # Criar pedidos
                pedidos = criar_pedidos(pecas)
                print()
            
            print('🎉 Banco de dados populado com sucesso!')
            print('\n📊 Resumo:')
            print(f'   🚗 Carros: {Car.objects.count()}')
            print(f'   🔧 Peças: {Peca.objects.count()}')
            print(f'   📋 Pedidos: {Pedido.objects.count()}')
            print(f'   📦 Itens: {ItemPedido.objects.count()}')
            
            print('\n🌐 Agora você pode:')
            print('   • Acessar o Django Admin: http://localhost:8000/admin/')
            print('   • Testar a API: http://localhost:8000/api/cars/')
            print('   • Usar o Frontend: http://localhost:3000/')

    except Exception as e:
        print(f'❌ Erro ao popular banco: {str(e)}')
        return 1
    
    return 0

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)