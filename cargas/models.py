from django.db import models
from django.urls import reverse


class Carga(models.Model):
    class Status(models.TextChoices):
        AGUARDANDO = 'aguardando', 'Aguardando coleta'
        EM_TRANSITO = 'em_transito', 'Em trânsito'
        ENTREGUE = 'entregue', 'Entregue'
        CANCELADA = 'cancelada', 'Cancelada'

    codigo = models.CharField('código', max_length=20, unique=True)
    descricao = models.CharField('descrição da carga', max_length=160)
    cliente = models.CharField('cliente', max_length=120)
    origem = models.CharField('origem', max_length=120)
    destino = models.CharField('destino', max_length=120)
    tipo = models.CharField('tipo de carga', max_length=80)
    peso = models.DecimalField('peso (kg)', max_digits=10, decimal_places=2)
    valor = models.DecimalField('valor da carga', max_digits=12, decimal_places=2)
    data_coleta = models.DateField('data prevista para coleta')
    status = models.CharField(
        'status',
        max_length=20,
        choices=Status.choices,
        default=Status.AGUARDANDO,
    )
    observacoes = models.TextField('observações', blank=True)
    criado_em = models.DateTimeField('criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('atualizado em', auto_now=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'carga'
        verbose_name_plural = 'cargas'

    def __str__(self):
        return f'{self.codigo} - {self.descricao}'

    def get_absolute_url(self):
        return reverse('cargas:detalhe', kwargs={'pk': self.pk})

# Create your models here.
