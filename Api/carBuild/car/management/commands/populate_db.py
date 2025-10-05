from django.core.management.base import BaseCommand
from django.db import transaction
from car.models import Car, Peca, Pedido, ItemPedido
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de exemplo para carros, peças e pedidos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Limpa todos os dados antes de popular',
        )
        parser.add_argument(
            '--cars-only',
            action='store_true',
            help='Popula apenas carros e peças (sem pedidos)',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('🗑️  Limpando dados existentes...')
            ItemPedido.objects.all().delete()
            Pedido.objects.all().delete()
            Peca.objects.all().delete()
            Car.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✅ Dados limpos com sucesso!'))

        try:
            with transaction.atomic():
                # Criar carros
                cars = self.create_cars()
                self.stdout.write(f'🚗 Criados {len(cars)} carros')

                # Criar peças
                pecas = self.create_pecas(cars)
                self.stdout.write(f'🔧 Criadas {len(pecas)} peças')

                if not options['cars_only']:
                    # Criar pedidos
                    pedidos = self.create_pedidos(pecas)
                    self.stdout.write(f'📋 Criados {len(pedidos)} pedidos')

                self.stdout.write(
                    self.style.SUCCESS('🎉 Banco de dados populado com sucesso!')
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro ao popular banco: {str(e)}')
            )

    def create_cars(self):
        """Cria carros de exemplo"""
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
                self.stdout.write(f'  ✓ {car.modelo} ({car.ano})')

        return cars

    def create_pecas(self, cars):
        """Cria peças de exemplo para os carros"""
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
            {'nome': 'Pneu', 'valor_min': 200.00, 'valor_max': 600.00},
            {'nome': 'Bateria', 'valor_min': 180.00, 'valor_max': 400.00},
            {'nome': 'Óleo Motor 5W30', 'valor_min': 35.00, 'valor_max': 80.00},
            {'nome': 'Fluido de Freio', 'valor_min': 15.00, 'valor_max': 35.00},
            {'nome': 'Aditivo Radiador', 'valor_min': 12.00, 'valor_max': 30.00},
        ]

        pecas_especiais = {
            'Fusca': [
                {'nome': 'Carburador Weber', 'valor_min': 400.00, 'valor_max': 800.00},
                {'nome': 'Cilindro Mestre', 'valor_min': 150.00, 'valor_max': 300.00},
                {'nome': 'Caixa de Fusível Vintage', 'valor_min': 80.00, 'valor_max': 200.00},
            ],
            'Civic': [
                {'nome': 'Kit Embreagem VTEC', 'valor_min': 600.00, 'valor_max': 1200.00},
                {'nome': 'Sensor MAP', 'valor_min': 120.00, 'valor_max': 250.00},
                {'nome': 'Bobina de Ignição', 'valor_min': 180.00, 'valor_max': 350.00},
            ]
        }

        pecas = []
        
        # Criar peças genéricas para cada carro
        for car in cars:
            # Escolher aleatoriamente 8-12 peças genéricas por carro
            num_pecas = random.randint(8, 12)
            pecas_selecionadas = random.sample(pecas_genericas, num_pecas)
            
            for peca_data in pecas_selecionadas:
                valor = Decimal(str(random.uniform(
                    peca_data['valor_min'], 
                    peca_data['valor_max']
                ))).quantize(Decimal('0.01'))
                
                peca, created = Peca.objects.get_or_create(
                    nome=peca_data['nome'],
                    owner=car,
                    defaults={'valor': valor}
                )
                
                if created:
                    pecas.append(peca)
                    self.stdout.write(f'  ✓ {peca.nome} para {car.modelo} - R$ {peca.valor}')

            # Adicionar peças especiais se existirem para o modelo
            if car.modelo in pecas_especiais:
                for peca_data in pecas_especiais[car.modelo]:
                    valor = Decimal(str(random.uniform(
                        peca_data['valor_min'], 
                        peca_data['valor_max']
                    ))).quantize(Decimal('0.01'))
                    
                    peca, created = Peca.objects.get_or_create(
                        nome=peca_data['nome'],
                        owner=car,
                        defaults={'valor': valor}
                    )
                    
                    if created:
                        pecas.append(peca)
                        self.stdout.write(f'  ✓ {peca.nome} (especial) para {car.modelo} - R$ {peca.valor}')

        # Criar algumas peças sem owner (genéricas)
        pecas_sem_owner = [
            {'nome': 'Óleo Motor Universal 20W50', 'valor': 45.00},
            {'nome': 'Fluido de Freio DOT4', 'valor': 25.00},
            {'nome': 'Aditivo Combustível', 'valor': 18.00},
            {'nome': 'Cera Automotiva', 'valor': 35.00},
            {'nome': 'Shampoo Automotivo', 'valor': 22.00},
        ]

        for peca_data in pecas_sem_owner:
            peca, created = Peca.objects.get_or_create(
                nome=peca_data['nome'],
                owner=None,
                defaults={'valor': Decimal(str(peca_data['valor']))}
            )
            
            if created:
                pecas.append(peca)
                self.stdout.write(f'  ✓ {peca.nome} (universal) - R$ {peca.valor}')

        return pecas

    def create_pedidos(self, pecas):
        """Cria pedidos de exemplo"""
        pedidos = []
        
        # Criar 5-8 pedidos aleatórios
        num_pedidos = random.randint(5, 8)
        
        for i in range(num_pedidos):
            pedido = Pedido.objects.create()
            
            # Adicionar 1-5 itens aleatórios por pedido
            num_itens = random.randint(1, 5)
            pecas_pedido = random.sample(list(pecas), min(num_itens, len(pecas)))
            
            for peca in pecas_pedido:
                quantidade = random.randint(1, 3)
                
                # Verificar se é chassi (máximo 1)
                if 'chassi' in peca.nome.lower():
                    quantidade = 1
                
                ItemPedido.objects.create(
                    pedido=pedido,
                    peca=peca,
                    quantidade=quantidade
                )
            
            # Calcular total do pedido
            pedido.calcular_total()
            pedidos.append(pedido)
            
            self.stdout.write(f'  ✓ Pedido {pedido.id_unico} - R$ {pedido.valor_total}')

        return pedidos