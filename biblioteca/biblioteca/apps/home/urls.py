from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('biblioteca.apps.home.views',
	#url(r'^$','index_view', name = 'vista_principal'),
	
	
	url(r'^libronuevo/$','libronuevo_view', name = 'vista_libronuevo'),
	url(r'^login/$','login_view', name = 'vista_login'),
	url(r'^logout/$','logout_view', name = 'vista_logout'),



	#prestamos
	url(r'^prestamos/$','prestamos_view', name = 'vista_prestamos'),
	url(r'^prestamo/(?P<id_editprest>.*)/$', 'single_prestamo_view', name = 'vista_single_prestamo'),
	url(r'^reservas/$','reservas_view',name = 'vista_reservas'),
	
	url(r'^mis_reservas/$','mis_reservas_view',name = 'vista_mis_reservas'),
	
	#autores
	url(r'^autores/$','autores_view', name = 'vista_autores'),
	url(r'^autor/(?P<id_editautor>.*)/$', 'single_autor_view', name = 'vista_single_autor'),

	#editorial
	url(r'^editoriales/$','editoriales_view', name = 'vista_editoriales'),
	url(r'^editorial/(?P<id_editorial>.*)/$', 'single_editorial_view', name= 'vista_single_editorial'),
	
	#categoria
	url(r'^categorias/$','categorias_view', name = 'vista_categorias'),
	url(r'^categoria/(?P<id_prod>.*)/$','single_categoria_view', name = 'vista_info_categoria'),

	#biblotecario
	url(r'^bibliotecarios/$','bibliotecarios_view', name= 'vista_bibliotecarios'),
	url(r'^bibliotecario/(?P<id_biblio>.*)/$', 'single_bibliotecarios_view', name = 'vista_single_bibliotecario'),

	#usuario
	url(r'^usuarios/$', 'usuarios_view', name = 'vista_usuarios'),
	url(r'^usuario/(?P<id_usua>.*)/$', 'single_usuario_view', name = 'vista_single_usuario'),

	#cuidad
	url(r'^ciudades/$','ciudades_view', name= 'vista_ciudades'), 
	url(r'^ciudad/(?P<id_ciu>.*)/$', 'single_ciudades_view', name = 'vista_single_ciudad'),

	#tipo_usuario
	url(r'^tipos_usuarios/$','tipos_usuarios_view', name = 'vista_tipos_usuarios'),
	url(r'^tipo_usuario/(?P<id_tipo>.*)/$','single_tipo_usuario_view', name = 'vista_single_tipo_usuario'),

	#libros
	url(r'^libros/$', 'libros_view', name = 'vista_libros'),
	#url(r'^libros/page/(?P<pagina>.*)/$', 'libros_view', name = 'vista_libros'),
	url(r'^libro/(?P<id_prod>.*)/$', 'single_libro_view', name = 'vista_single_libro'),

	#biblioteca
	url(r'^bibliotecas/$','bibliotecas_view', name ='vista_bibliotecas'),
	url(r'^biblioteca/(?P<id_biblioteca>.*)/$','single_biblioteca_view', name ='vista_single_biblioteca'),
	
	#Webservices JSON y XML
	url(r'^ws/libro/$','ws_libro_view', name = 'ws_libro_url'),

	url(r'^contacto/$', 'contacto_view', name = 'vista_contacto'),

	)
