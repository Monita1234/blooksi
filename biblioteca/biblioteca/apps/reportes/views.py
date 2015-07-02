#-*-coding: utf-8-*-
from io import BytesIO
from django.forms import extras
from reportlab.lib import colors
from django.shortcuts import render
from reportlab.platypus import Table
from datetime import  date, timedelta
from reportlab.lib.pagesizes import letter
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponseRedirect, HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from django.core.paginator import Paginator, EmptyPage, InvalidPage

from biblioteca.apps.reportes.forms import  *
from biblioteca.apps.libros.forms import *
from biblioteca.apps.libros.models import *

import os
from reportlab.platypus import Paragraph
from reportlab.platypus import Image
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Spacer

from biblioteca.apps.reportes.forms import reporte_busqueda_form
from biblioteca.apps.libros.models import Busqueda, Libro

from reportlab.platypus import Paragraph, Image, SimpleDocTemplate, Spacer


from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts import *
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.widgets.markers  import makeMarker
from reportlab import *
#from django.http import HttpResponseRedirect
from reportlab.lib.colors import Color, blue, red, yellow

from reportlab.graphics.charts.piecharts import Pie

from reportlab.graphics.charts.legends import Legend
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
import datetime

x = date.today()
y = date.today()

x1 = 0
y1 = 0
b = date.today()

def reportes_view(request):

	if request.user.is_authenticated():
		return render_to_response('home/reportes.html',context_instance = RequestContext(request)) 
	else:
		return HttpResponseRedirect('/')

#Las Negras
def reporte_libros_mes_view(request):
	mensaje= ""
	if request.user.is_authenticated():
		info_enviado = True
		fecha_libro = ""
		#hoy = date.today()
		#mes = hoy.month
		mes = 0
 		anio = 0
		prest_libro = []

		if request.method == "POST":
			reportes = libro_mes_form(request.POST)
			if reportes.is_valid():
				info_enviado = True
				fecha_libro = reportes.cleaned_data['fecha_consulta']
				mes = fecha_libro.month
				anio = fecha_libro.year
				prest_libro = Prestamo.objects.filter(fecha_prestamo__month = mes, fecha_prestamo__year = anio)
				global x1, y1
				y1 = prest_libro.count()
				if (mes == 1):
					x1= Prestamo.objects.filter(fecha_prestamo__month = mes+11, fecha_prestamo__year = anio-1).count()
					x1m = mes+11
				else:
					x1= Prestamo.objects.filter(fecha_prestamo__month = mes-1, fecha_prestamo__year = anio).count()
					x1m = mes-1

				global b 
				b = fecha_libro		
				reportes = libro_mes_form()
				if len(prest_libro) == 0:
					mensaje = "No se encontraron libros prestados"




		else:                                                                  
			reportes = libro_mes_form()
		ctx = {'reporte_libro':reportes, 'prest_libro':prest_libro, 'info_enviado':info_enviado, 'fecha_libro':fecha_libro, 'mensaje':mensaje}
		return render_to_response('reportes/reporte_libro_mes.html',ctx, context_instance = RequestContext(request)) 
	else:
		return HttpResponseRedirect('/')



def generar_pdf_libros_mes(request):
	print "Genero el PDF"
	mes = 0
	anio = 0
	story=[]
	response = HttpResponse(content_type='application/pdf')
	pdf_name = "reporte_libro.pdf"  # llamado clientes
	# la linea 26 es por si deseas descargar el pdf a tu computadora
	# response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
	buff = BytesIO()
	doc = SimpleDocTemplate(buff,
							pagesize=letter,
							rightMargin=40,
							leftMargin=40,
							topMargin=60,
							bottomMargin=18,
							)
	reporte_libro = []
	styles = getSampleStyleSheet()
	fichero_imagen="biblioteca/media/images/Reports-banner.jpg"
	imagen_logo = Image(os.path.realpath(fichero_imagen),width=400,height=100)
	story.append(imagen_logo)
	reporte_libro.append(imagen_logo)
	fecha_reporte = Paragraph("Fecha del reporte: "+str(date.today()), styles['Heading1'])
	reporte_libro.append(fecha_reporte)
	header = Paragraph("Listado de Libros que Fueron prestados en el mes", styles['Normal'])
	reporte_libro.append(header)
	headings = ('Nombre', 'Fecha devolución','Fecha Prestamo')
	

	#fecha_libro = reportes.cleaned_data['fecha_consulta']
	mes = b.month
	anio = b.year
	i = mes 
	j = mes
	
	all_libros = [(p.libro.nombre_libro, p.fecha_devolucion, p.fecha_prestamo) for p in Prestamo.objects.filter(fecha_prestamo__month = mes, fecha_prestamo__year = anio)]
	print all_libros

	t = Table([headings] + all_libros)
	t.setStyle(TableStyle(
		[
			('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
			('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
			('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
		]
	))

	#GRAFICA DE BARRAS
	drawing = Drawing(400, 200)
	data = [(x1, y1)]
	bc = VerticalBarChart()
	bc.x = 50
	bc.y = 50
	bc.height = 125
	bc.width = 300
	bc.data = data
	bc.bars[0].fillColor = colors.yellow
	bc.bars[1].fillColor = colors.red
	bc.strokeColor = colors.black
	bc.valueAxis.valueMin = 0
	bc.valueAxis.valueMax = y1+10
	try:
		o = y1 / 2
		if type(o) == 'float':
			bc.valueAxis.valueStep = y1+0.5
		if type(o) == 'int':
			bc.valueAxis.valueStep = o

	except:
		"Nos se puede"


	bc.categoryAxis.labels.boxAnchor = 'ne'
	bc.categoryAxis.labels.dx = 8
	bc.categoryAxis.labels.dy = -2
	bc.categoryAxis.labels.angle = 0
	if mes == 1:
		i = mes + 11
	else:
		j = mes - 1	



	bc.categoryAxis.categoryNames = [ datetime.date(anio, j, 1).strftime('%B'), datetime.date(anio, i, 1).strftime('%B')]
	drawing.add(bc)

	bc.barLabels.nudge = 20
	bc.barLabelFormat = '%0.0f'
	bc.barLabels.dx = 0
	bc.barLabels.dy = 0
	bc.barLabels.boxAnchor = 'n' # irrelevant (becomes 'c')
	bc.barLabels.fontName = 'Helvetica'
	bc.barLabels.fontSize = 14

	reporte_libro.append(drawing)
	reporte_libro.append(t)
	doc.build(reporte_libro)
	response.write(buff.getvalue())
	buff.close()
	return response


#Las primas
def reporte_usuarios_mes_view(request):
	
	if request.user.is_authenticated():
		info_enviado = True
		fecha_usuarios = ""
		#hoy = date.today()
		#mes = hoy.month
		mes = 0
		anio = 0
		usuarios = []
		mensaje = ""
		error_fecha = ""
		error_vacio = ""
		

		if request.method == "POST":
			reportes = fecha_mes_form(request.POST)
			if reportes.is_valid():
				info_enviado = True
				fecha_usuarios= reportes.cleaned_data['fecha']
				if fecha_usuarios <= date.today():
					global x
					x = fecha_usuarios
					mes = fecha_usuarios.month
					anio = fecha_usuarios.year
					usuarios = Prestamo.objects.filter(fecha_prestamo__month =mes,fecha_prestamo__year = anio)
					mensaje = "Exito!"
				else:
					error_fecha = "Error! La Fecha Igresada no Puede Ser Mayor a la Fecha Actual"
			else:
				error_vacio = "El Campo No Debe Estar Vacio"


		else:                                                                  
			reportes = fecha_mes_form()
		ctx = {'reporte_usuarios':reportes,'mensaje':mensaje,'error_vacio':error_vacio,'error_fecha':error_fecha, 'usuarios':usuarios, 'info_enviado':info_enviado, 'fecha_usuarios':fecha_usuarios }
		return render_to_response('reportes/reporte_usuarios_mes.html',ctx, context_instance = RequestContext(request)) 
	else:
		return HttpResponseRedirect('/')

def generar_pdf_usuarios_mes(request):
    print "Genero el PDF"
    mes =0
    anio =0
    story =[]
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "reporte_usuarios_mes.pdf"  # llamado clientes
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=60,
                            bottomMargin=18,
                            )
    reportes = []
    styles = getSampleStyleSheet()
    fichero_imagen="biblioteca/media/images/biblio1.png" 
    imagen_logo=Image(os.path.realpath(fichero_imagen),width=400,height=100)
    story.append(imagen_logo)
    reportes.append(imagen_logo)
    header = Paragraph("Listado de usuarios que prestaron libros en el mes", styles['Heading1'])
    reportes.append(header)
    headings = ('Fecha Prestamo', 'Usuario', 'Nombre del Libro', 'Fecha Devolucion')
    mes = x.month
    anio = x.year
	
    allreportes = [(i.fecha_prestamo, i.usuario.nombre, i.libro.nombre_libro, i.fecha_devolucion) for i in Prestamo.objects.filter(fecha_prestamo__month =mes,fecha_prestamo__year = anio)]
    print allreportes

    t = Table([headings] + allreportes)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))
    reportes.append(t)
    doc.build(reportes)
    response.write(buff.getvalue())
    buff.close()
    return response


#jennifer 9 junio
def reporte_busqueda_view(request):
	info_enviado = True
	fecha_inicio = ""
	fecha_final = ""
	mensaje = ""
	mensaje2 = ""
	b = []
	lista = []
	c = 0
	t = []
	i = ""
	j = 0
	busqueda = ""
	li=[]

	mensaje_error= False
	
	
	#formulario = reporte_busqueda_form()
	#try
	if request.method == "POST": #Envio de informacion por POST
		reportes = reporte_busqueda_form(request.POST)
		print "---------------"
		#try:
		if reportes.is_valid():
			info_enviado = True
			fecha_inicio = reportes.cleaned_data['fecha_ini']
			fecha_final = reportes.cleaned_data['fecha_fin']
			if fecha_inicio <= date.today():
				global x
				x = fecha_inicio 
				if fecha_final <= date.today(): 
					global y
					y = fecha_final
					if fecha_inicio  <= fecha_final:
						t = Busqueda.objects.all()
						b = Busqueda.objects.values('busqueda', 'resultados').filter(fecha__range=(fecha_inicio, fecha_final)).distinct()
						for i in b:
							print "________________",i.get("busqueda")
							for j in t:
								print "===============",j.busqueda
								if j.busqueda == i.get("busqueda") and j.fecha >= fecha_inicio and j.fecha <= fecha_final:
									c = c + 1
									print c
							lista.append(c)
							c=0		
						print lista , len(lista)

						li = zip(b,lista)				
						print li
						print "_________________________________\n",b 


						if li == []:
							mensaje = "No hay reportes en las fechas ingresadas"




					else:
						mensaje="Error ! La Fecha Inicial  Ingresada No Puede Ser Mayor A La Fecha Final Para Generar Su Reporte "
				else:
					mensaje = "Error ! la Fecha Final Debe Ser Menor A La Fecha Actual Para Generar Su Reporte "
			else:
				mensaje = "Error ! La Fecha Inicial Debe Ser Menor A La Fecha Actual Para Generar Su Reporte "
		else:
			mensaje2="Los Campos No Deben Estar Vacios Para Generar Su Reporte "
		

			print "---------------", busqueda#.count()
			#S= busqueda.count()

	else: #GET
			reportes = reporte_busqueda_form()
	

	ctx = {'form':reportes,'busqueda':b,'li':li, 'reporte1':reportes,'mensaje':mensaje,'mensaje2':mensaje2,'lista':lista,'info_enviado':info_enviado, 'fecha_ini':fecha_inicio, 'fecha_fin':fecha_final, 'mensaje_error':mensaje_error}		
	return render_to_response('reportes/reportes_busquedas.html',ctx, context_instance = RequestContext(request)) 





#GENERAR PDF


x = date.today()

def generar_pdf_busquedas_view(request):
    print "Genero el PDF"
    fecha_m = ""
    
    fecha_a = ""
    b=[]
    t=[]
    fecha_inicio = x
    fecha_final = y
    c=0
    story =[]

    


    response = HttpResponse(content_type='application/pdf')
    pdf_name = "reporte_busqueda.pdf"  # llamado clientes
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=60,
                            bottomMargin=18,
                            )
    reportes = []
    styles = getSampleStyleSheet()
    fichero_imagen="biblioteca/media/images/Reports-banner.jpg"

    imagen_logo=Image(os.path.realpath(fichero_imagen),width=400,height=100)
    story.append(imagen_logo)
    reportes.append(imagen_logo)

    header = Paragraph("Fecha del reporte: "+str(date.today()), styles['Heading1'])
    
    header2 = Paragraph("Reporte de las busquedas realizadas entre la fecha "+str(fecha_inicio)+" hasta la fecha "+str(fecha_final) + "\n", styles['Normal'])
    salto_linea = Paragraph("\n\n", styles["Normal"])

    header3 = Paragraph("Total De Busquedas " + "\n", styles['Normal'])
    salto_linea = Paragraph("\n\n", styles["Normal"])
    
    reportes.append(Spacer(1, 12))
    reportes.append(header)
    reportes.append(Spacer(1, 12))
    reportes.append(header2)
    reportes.append(Spacer(1, 12))
    reportes.append(header3)
    reportes.append(Spacer(1, 12))
    

    headings = ('Busqueda', 'Resultado',)# 'Cantidad_Veces_Buscadas')
    lista=[]
    t = Busqueda.objects.all()
    b = Busqueda.objects.filter(fecha__range=(fecha_inicio, fecha_final)).values('busqueda', 'resultados').distinct()

#GRAFICAS BARRA
    total_busquedas=Busqueda.objects.all().count() #TOTAL BUSQUEDAS
    si=Busqueda.objects.filter(resultados=True).count() #BUSUEDAS ENCONTRADAS (SI)
    no=total_busquedas-si #BUSQUEDAS NO ENCONTRADAS (NO)


#GRAFICAS PASTEL
    


    for i in b:
        print "________________",i.get("busqueda")
        for j in t:
            print "===============",j.busqueda
            if j.busqueda == i.get("busqueda") and j.fecha >= fecha_inicio and j.fecha <= fecha_final:
                c = c + 1
                print c
        lista.append(c)
        c=0     
    print lista , len(lista)

    li = zip(b,lista)               
    '''
    for i in b:
        print "________________",i.get("busqueda")
        for j in t:
            print "===============",j.busqueda
            if j.busqueda == i.get("busqueda"):
                c = c + 1
                print c
        lista.append(c)
        c=0
        li = zip(b,lista)
    '''

    #allreportes = [ (i.busqueda, i.resultados) for i in Busqueda.objects.filter(fecha__range=(fecha_inicio, fecha_final)).values('busqueda', 'resultados').distinct()]

   # allreportes = [ i.values() for i in Busqueda.objects.filter(fecha__range=(fecha_inicio, fecha_final)).values('busqueda', 'resultados').distinct()]

    allreportes = [ i.values() for i in Busqueda.objects.filter(fecha__range=(fecha_inicio, fecha_final)).values('busqueda', 'resultados').distinct()]

   
    print allreportes


    t = Table([headings] + allreportes)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))

#GRAFICA DE BARRAS
    drawing = Drawing(400, 200)
    data = [(si, no)]
    bc = VerticalBarChart()
    bc.x = 50
    bc.y = 50
    bc.height = 125
    bc.width = 300
    bc.data = data
    bc.bars[0].fillColor = colors.green
    bc.bars[1].fillColor = colors.red
    bc.strokeColor = colors.red
    bc.fillColor = colors.yellow
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = total_busquedas+10
    try:
        r = total_busquedas/2
        if type(r) == 'float':
            bc.valueAxis.valueStep = total_busquedas+0.5
        if type(r) == 'int':
            bc.valueAxis.valueStep = r
    except:
        "Nos se puede"


    bc.categoryAxis.labels.boxAnchor = 'ne'
    bc.categoryAxis.labels.dx = 8
    bc.categoryAxis.labels.dy = -2
    bc.categoryAxis.labels.angle = 0
    bc.categoryAxis.categoryNames = ['Encontradas', 'No Encontradas']
    drawing.add(bc)

    bc.barLabels.nudge = 20
    bc.barLabelFormat = '%0.0f'
    bc.barLabels.dx = 0
    bc.barLabels.dy = 0
    bc.barLabels.boxAnchor = 'n' # irrelevant (becomes 'c')
    bc.barLabels.fontName = 'Helvetica'
    bc.barLabels.fontSize = 14





    
#GRAFICAS DE PASTEL

    d = Drawing(400, 200)
    pc = Pie()
    pc.x = 125
    pc.y = 25
    pc.data = lista
    print lista
    #pc.data = [7, 1, 1, 1, 1, 2]

    pc.labels = [ str(i.values()) for i in Busqueda.objects.filter(fecha__range=(fecha_inicio, fecha_final)).values('busqueda').distinct()]
    #pc.labels = ['example1', 'example2', 'example3', 'example4', 'example5', 'example6']
    pc.sideLabels = 1
    pc.width = 150
    pc.height = 150
    pc.slices.strokeWidth=1#0.5
    pc.slices[0].fillColor = colors.yellow
    pc.slices[1].fillColor = colors.thistle
    pc.slices[2].fillColor = colors.cornflower
    pc.slices[3].fillColor = colors.lightsteelblue
    pc.slices[4].fillColor = colors.aquamarine
    pc.slices[5].fillColor = colors.cadetblue
    d.add(pc)



    legend = Legend() 
    legend.x               = 370
    legend.y               = 0
    legend.dx              = 8 
    legend.dy              = 8 
    legend.fontName        = 'Helvetica' 
    legend.fontSize        = 7 
    legend.boxAnchor       = 'n' 
    legend.columnMaximum   = 10 
    legend.strokeWidth     = 1 
    legend.strokeColor     = colors.black  
    legend.deltax          = 75 
    legend.deltay          = 10 
    legend.autoXPadding    = 5 
    legend.yGap            = 0 
    legend.dxTextSpace     = 5 
    legend.alignment       = 'right' 
    legend.dividerLines    = 1|2|4 
    legend.dividerOffsY    = 4.5 
    legend.subCols.rpad    = 30 
     
    #Insertemos nuestros propios colores
    colores  = [colors.blue, colors.red, colors.green, colors.yellow, colors.pink]
    for i, color in enumerate(colores): 
        pc.slices[i].fillColor = color
         
    legend.colorNamePairs  = [(
                                pc.slices[i].fillColor, 
                                (pc.labels[i][0:20], '%0.2f' % pc.data[i])
                               ) for i in xrange(len(pc.data))]
     
    d.add(pc) 
    
    

    reportes.append(t)
    d.add(legend)
    story.append(d)
    reportes.append(drawing)
    reportes.append(d)
    doc.build(reportes)
    response.write(buff.getvalue())
    buff.close()
    return response
