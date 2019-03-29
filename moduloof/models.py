from tkinter import CASCADE

from django.db import models


class Cliente(models.Model):
    nome = models.CharField(max_length=200, blank=False, null=False)
    responsavel = models.CharField(max_length=200, blank=False, null=False)
    telefone = models.CharField(max_length=12, blank=False, null=False)

    def __str__(self):
        return self.nome


class Tpfilme(models.Model):
    tipo = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return self.tipo


class Tpadesivo(models.Model):
    tipo = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return self.tipo


class Filme_bopp(models.Model):
    descricao = models.CharField(max_length=200, blank=False, null=False)
    tipo = models.ForeignKey(Tpfilme, on_delete=CASCADE, blank=False, null=False)
    micragem = models.DecimalField(max_digits=2, decimal_places=0, blank=False, null=False)
    gramatura = models.DecimalField(max_digits=3, decimal_places=1, blank=False, null=False)
    rendimento = models.DecimalField(max_digits=3, decimal_places=1, blank=False, null=False)
    valor_de_venda = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)

    def __str__(self):
        return self.descricao


class Acabamento(models.Model):
    tipo = models.CharField(max_length=200, blank=False, null=False)
    incremento = models.DecimalField(max_digits=3, decimal_places=0, blank=False, null=False)

    def __str__(self):
        return self.tipo


class Orcamento_filme(models.Model):
    data_criacao = models.DateTimeField(auto_now_add=True)
    data = models.DateTimeField()
    cliente = models.ForeignKey(Cliente, on_delete=CASCADE, blank=False, null=False)
    servico = models.CharField(max_length=400, blank=False, null=False)
    material = models.ForeignKey(Filme_bopp, on_delete=CASCADE, blank=False, null=False)
    acabamento = models.ForeignKey(Acabamento, on_delete=CASCADE, blank=False, null=False)
    comp = models.DecimalField(max_digits=3, decimal_places=0, blank=False, null=False)
    larg = models.DecimalField(max_digits=3, decimal_places=0, blank=False, null=False)
    quantidade = models.DecimalField(max_digits=7, decimal_places=0, blank=False, null=False)

    def __str__(self):
        return self.cliente.nome + ' - ' + self.servico


class Adesivo(models.Model):
    descricao = models.CharField(max_length=200, blank=False, null=False)
    tipo = models.ForeignKey(Tpadesivo, on_delete=CASCADE, blank=False, null=False)
    valor_de_venda = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.descricao


class Orcamento_adesivo(models.Model):
    data_criacao = models.DateTimeField(auto_now_add=True)
    data = models.DateTimeField()
    cliente = models.ForeignKey(Cliente, on_delete=CASCADE, blank=False, null=False)
    servico = models.CharField(max_length=400, blank=False, null=False)
    material = models.ForeignKey(Adesivo, on_delete=CASCADE, blank=False, null=False)
    acabamento = models.ForeignKey(Acabamento, on_delete=CASCADE, blank=False, null=False)
    comp = models.DecimalField(max_digits=3, decimal_places=0, blank=False, null=False)
    larg = models.DecimalField(max_digits=3, decimal_places=0, blank=False, null=False)
    quantidade = models.DecimalField(max_digits=7, decimal_places=0, blank=False, null=False)

    def __str__(self):
        return self.cliente.nome + ' - ' + self.servico
