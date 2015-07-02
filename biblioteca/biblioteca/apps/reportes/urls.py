from django.conf.urls.defaults import *

urlpatterns = patterns('biblioteca.apps.reportes.views',
#	url(r'^historia/(?P<id_his>.*)/$','singleHistoria_view',name='vista_single_historia'),
	
	url(r'^reportes/$', 'reportes_view', name = 'vista_reportes'),


	#Las primas
	url(r'^reportes/usuarios_por_mes/$', 'reporte_usuarios_mes_view', name = 'vista_reporte_usuarios_mes'),
	url(r'^generar_pdf_usuarios_mes/$', 'generar_pdf_usuarios_mes', name='generar_pdf_usuarios_mes'),

	#las negras
	url(r'^reportes/libro_por_mes/$', 'reporte_libros_mes_view', name = 'vista_reporte_libros_mes'),
	url(r'^reporte_usuarios_mes_view/$','generar_pdf_libros_mes', name='reporte_libros_prestados_mes_pdf'),
	
	#Jennifer & Yaki
	url(r'^reporte_busqueda/$','reporte_busqueda_view', name = 'vista_reporte_busqueda'),
	url(r'^generar_pdf_busquedas/$','generar_pdf_busquedas_view', name = 'pdf_busquedas'),
	
)