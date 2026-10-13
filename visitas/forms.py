import re

from django import forms
from .models import Visita

class VisitaForm(forms.ModelForm):
    rut = forms.CharField(
        max_length=12,
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-xl border border-slate-300 bg-white px-3.5 py-3 text-sm text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-sky-600 focus:ring-4 focus:ring-sky-100'
        })
    )

    def clean_nombre(self):
        nombre = ' '.join(self.cleaned_data['nombre'].split())
        if not nombre:
            raise forms.ValidationError('Ingresa el nombre del visitante.')
        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü .'-]+", nombre):
            raise forms.ValidationError('El nombre solo puede contener letras y espacios.')
        return nombre

    def clean_rut(self):
        rut = self.cleaned_data['rut'].strip().replace('.', '').replace(' ', '').upper()
        if not re.fullmatch(r'\d{7,8}-[0-9K]', rut):
            raise forms.ValidationError('Ingresa el RUT con formato 12345678-5.')

        cuerpo, digito = rut.split('-')
        suma = 0
        multiplicador = 2
        for numero in reversed(cuerpo):
            suma += int(numero) * multiplicador
            multiplicador = 2 if multiplicador == 7 else multiplicador + 1

        resto = 11 - (suma % 11)
        digito_valido = '0' if resto == 11 else 'K' if resto == 10 else str(resto)
        if digito != digito_valido:
            raise forms.ValidationError('El dígito verificador del RUT no es válido.')
        return rut

    def clean_motivo_visita(self):
        motivo = ' '.join(self.cleaned_data['motivo_visita'].split())
        if not motivo:
            raise forms.ValidationError('Ingresa el motivo de la visita.')
        return motivo

    def clean(self):
        cleaned_data = super().clean()
        hora_entrada = cleaned_data.get('hora_entrada')
        hora_salida = cleaned_data.get('hora_salida')
        if hora_entrada and hora_salida and hora_salida <= hora_entrada:
            self.add_error('hora_salida', 'La hora de salida debe ser posterior a la hora de entrada.')
        return cleaned_data

    class Meta:
        model = Visita
        fields = ['nombre', 'rut', 'hora_entrada', 'hora_salida', 'motivo_visita']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'block w-full rounded-xl border border-slate-300 bg-white px-3.5 py-3 text-sm text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-sky-600 focus:ring-4 focus:ring-sky-100'}),
            'rut': forms.TextInput(attrs={'class': 'block w-full rounded-xl border border-slate-300 bg-white px-3.5 py-3 text-sm text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-sky-600 focus:ring-4 focus:ring-sky-100'}),
            'hora_entrada': forms.TimeInput(attrs={'class': 'block w-full rounded-xl border border-slate-300 bg-white px-3.5 py-3 text-sm text-slate-900 outline-none transition focus:border-sky-600 focus:ring-4 focus:ring-sky-100', 'type': 'time'}),
            'hora_salida': forms.TimeInput(attrs={'class': 'block w-full rounded-xl border border-slate-300 bg-white px-3.5 py-3 text-sm text-slate-900 outline-none transition focus:border-sky-600 focus:ring-4 focus:ring-sky-100', 'type': 'time'}),
            'motivo_visita': forms.Textarea(attrs={'class': 'block min-h-32 w-full resize-y rounded-xl border border-slate-300 bg-white px-3.5 py-3 text-sm leading-6 text-slate-900 outline-none transition focus:border-sky-600 focus:ring-4 focus:ring-sky-100', 'rows': 4})
        }
        labels = {
            'hora_salida': 'Hora de salida (opcional)',
        }
        help_texts = {
            'hora_salida': 'Déjala vacía si la persona todavía está en el recinto.',
        }