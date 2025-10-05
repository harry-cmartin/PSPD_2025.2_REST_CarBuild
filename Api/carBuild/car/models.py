from django.db import models
from django.contrib.auth.models import User
import uuid

class Car(models.Model):
    modelo = models.CharField(max_length=30)
    ano = models.IntegerField()
    
    def __str__(self):
        return f"{self.modelo} ({self.ano})"

class Peca(models.Model):
    nome = models.CharField(max_length=50)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='pecas', blank=True, null=True)
    
    def __str__(self):
        return self.nome

class Pedido(models.Model):
    id_unico = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data_pedido = models.DateTimeField(auto_now_add=True)
    
    def gerar_relatorio(self):
        """Gera um relatório com nome das peças e quantidades"""
        relatorio = []
        for item in self.itens.all():
            relatorio.append({
                'nome_peca': item.peca.nome,
                'quantidade': item.quantidade,
                'valor_unitario': float(item.peca.valor),
                'subtotal': float(item.subtotal)
            })
        return {
            'id_pedido': str(self.id_unico),
            'data_pedido': self.data_pedido.strftime('%d/%m/%Y %H:%M'),
            'itens': relatorio,
            'valor_total': float(self.valor_total)
        }
    
    def calcular_total(self):
        """Calcula o valor total do pedido baseado nos itens"""
        total = sum(item.subtotal for item in self.itens.all())
        self.valor_total = total
        self.save()
        return total
    
    def __str__(self):
        return f"Pedido #{self.id_unico}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    peca = models.ForeignKey(Peca, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.quantidade}x {self.peca.nome}"
    
    @property
    def subtotal(self):
        return self.quantidade * self.peca.valor
    