from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CargaForm
from .models import Carga

def _filtrar_cargas(request):
    cargas = Carga.objects.all()
    busca = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()
    if busca:
        cargas = cargas.filter(
            Q(codigo__icontains=busca)
            | Q(cliente__icontains=busca)
            | Q(origem__icontains=busca)
            | Q(destino__icontains=busca)
        )
    if status in Carga.Status.values:
        cargas = cargas.filter(status=status)
    return cargas, busca, status


@login_required
def dashboard(request):
    cargas, busca, status = _filtrar_cargas(request)
    context = {
        'cargas': cargas[:8],
        'busca': busca,
        'status_selecionado': status,
        'total_cargas': Carga.objects.count(),
        'em_transito': Carga.objects.filter(status=Carga.Status.EM_TRANSITO).count(),
        'aguardando': Carga.objects.filter(status=Carga.Status.AGUARDANDO).count(),
        'entregues': Carga.objects.filter(status=Carga.Status.ENTREGUE).count(),
        'peso_total': Carga.objects.aggregate(total=Sum('peso'))['total'] or 0,
    }
    return render(request, 'cargas/dashboard.html', context)


@login_required
def lista(request):
    cargas, busca, status = _filtrar_cargas(request)
    return render(request, 'cargas/lista.html', {
        'cargas': cargas, 'busca': busca, 'status_selecionado': status,
        'status_choices': Carga.Status.choices,
    })


@login_required
def criar(request):
    form = CargaForm(request.POST or None)
    if form.is_valid():
        carga = form.save()
        messages.success(request, f'Carga {carga.codigo} cadastrada com sucesso.')
        return redirect(carga)
    return render(request, 'cargas/form.html', {'form': form, 'titulo': 'Nova carga'})


@login_required
def editar(request, pk):
    carga = get_object_or_404(Carga, pk=pk)
    form = CargaForm(request.POST or None, instance=carga)
    if form.is_valid():
        carga = form.save()
        messages.success(request, f'Carga {carga.codigo} atualizada com sucesso.')
        return redirect(carga)
    return render(request, 'cargas/form.html', {
        'form': form, 'titulo': f'Editar carga {carga.codigo}', 'carga': carga,
    })


@login_required
def detalhe(request, pk):
    return render(request, 'cargas/detalhe.html', {
        'carga': get_object_or_404(Carga, pk=pk),
    })


@user_passes_test(lambda user: user.is_staff)
def excluir(request, pk):
    carga = get_object_or_404(Carga, pk=pk)
    if request.method == 'POST':
        codigo = carga.codigo
        carga.delete()
        messages.success(request, f'Carga {codigo} removida.')
        return redirect('cargas:lista')
    return render(request, 'cargas/excluir.html', {'carga': carga})
