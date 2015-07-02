from django import forms

class libro_mes_form(forms.Form):
	#fecha_ini = forms.DateField(widget = forms.TextInput(), label='Fecha Inicial')
	fecha_consulta = forms.DateField(widget = forms.TextInput(attrs={'id':'datepicker'}), label='Mes del Reporte')

class fecha_mes_form(forms.Form):
	fecha = forms.DateField(widget = forms.TextInput(attrs={'id':'datepicker'}), label='fecha')


class reporte_busqueda_form(forms.Form):
	fecha_ini = forms.DateField(widget = forms.TextInput(attrs={'id':'datepicker'}), label='fecha Inicial')
	fecha_fin = forms.DateField(widget = forms.TextInput(attrs={'id':'datepicker1'}), label='fecha Final')
	