from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Visita
from .forms import VisitaForm

def visitas_list(request):
    hoy = timezone.localdate()
    visitas = Visita.objects.filter(fecha_registro=hoy).order_by('-id')
    visitas_hoy = visitas.count()
    return render(request, 'visita_list.html', {'visitas': visitas, 'visitas_hoy': visitas_hoy})

def visitas_create(request):
    if request.method == 'POST':
        form = VisitaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('visitas_list')
    else:
        form = VisitaForm()
    return render(request, 'visita_crear.html', {'form': form})

def visita_detail(request, pk):
    visita = get_object_or_404(Visita, pk=pk, fecha_registro=timezone.localdate())
    return render(request, 'visita_detail.html', {'visita': visita})