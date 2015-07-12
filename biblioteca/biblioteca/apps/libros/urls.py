from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('biblioteca.apps.libros.views',


		url(r'^administrar/$','administrar_view', name = 'vista_administrar'),
		#url(r'^add/prestamo/$','add_prestamo_view',name = 'vista_add_prestamo'),
		
		url(r'^reservar/(?P<id_libro>.*)/$','reservar_view',name = 'vista_reservar'),
		url(r'^aprobar/prestamo/(?P<id_prestar>.*)/$','aprobar_prestamo_view',name = 'vista_aprobar_prestamo'),
		url(r'^cancelar/prestamo/(?P<id_prestar>.*)/$','cancelar_prestamo_view',name = 'vista_cancelar_prestamo'),
		url(r'^retornar/libro/(?P<id_prestar>.*)/$','retornar_libro_view',name = 'vista_retornar_libro'),
		
		#url(r'^prestar/(?P<id_prestar>.*)/$','prestar_view',name = 'vista_prestar'),
		
		url(r'^edit/prestamo/(?P<id_editprest>.*)/$', 'edit_prestamo_view', name = 'vista_edit_prestamo'),
		url(r'^eliminar/prestamo/(?P<id_prest>.*)/$','eliminar_prestamo_view',name= 'vista_eliminar_prestamo'),

		

		#autor
		url(r'^add/autor/$','add_autor_view',name = 'vista_add_autor'),
		url(r'^edit/autor/(?P<id_editautor>.*)/$', 'edit_autor_view', name = 'vista_edit_autor'),
		url(r'^eliminar/autor/(?P<id_aut>.*)/$','eliminar_autor_view',name= 'vista_eliminar_autor'),

		#editorial
		url(r'^add/editorial/$','add_editorial_view',name = 'vista_agregar_editorial'),
		url(r'^edit/editorial/(?P<id_editorial>.*)/$','edit_editorial_view', name = 'vista_editar_editorial'),
		url(r'^eliminar/editorial/(?P<id_editorial>.*)/$','eliminar_editorial_view', name = 'vista_eliminar_editorial'),
		
		#categoria
		url(r'^add/categoria/$','add_categoria_view',name= 'vista_agregar_categoria'),
		url(r'^edit/categoria/(?P<id_prod>.*)/$','editar_categoria_view',name= 'vista_editar_categoria'),
		url(r'^eliminar/categoria/(?P<id_prod>.*)/$','eliminar_categoria_view',name= 'vista_eliminar_categoria'),

		
		
		#usuario
		url(r'^add/usuario/$','add_usuario_view',name = 'vista_agregar_usuario'),
		url(r'^edit/usuario/(?P<id_usua>.*)/$', 'edit_usuario_view', name = 'vista_editar_usuario'),
		url(r'^del/usuario/(?P<id_usua>.*)/$', 'del_usuario_view', name = 'vista_eliminar_usuario'),
		
		url(r'^consultar_usuario_id/$','consultar_usuario_id_view', name = 'vista_consultar_usuario_id'),

		url(r'^registrar/bibliotecario/$','register_bibliotecario_view',name = 'vista_registrar_bibliotecario'),

		#tipo_usuario
		url(r'^add/tipo-usuario/$','add_tipo_usuario_view',name = 'vista_agregar_tipo'),
		url(r'^edit/tipo-usuario/(?P<id_tipo>.*)/$', 'edit_tipo_usuario_view', name = 'vista_editar_tipo'),
		url(r'^eliminar/tipo-usuario/(?P<id_tipo>.*)/$', 'eliminar_tipo_usuario_view', name = 'vista_eliminar_tipo'),

		#ciudad
		url(r'^add/ciudad/$','add_ciudad_view',name = 'vista_agregar_ciudad'),
		url(r'^edit/ciudad/(?P<id_ciu>.*)/$', 'edit_ciudad_view', name = 'vista_editar_ciudad'),
		url(r'^del/ciudad/(?P<id_ciu>.*)/$', 'del_ciudad_view', name = 'vista_eliminar_ciudad'),

		#libro
		url(r'^add/libros/$', 'agregar_libro_view', name = 'vista_agregar_libros'),
		url(r'^edit/libro/(?P<id_prod>.*)/$', 'editar_libro_view', name = 'vista_editar_libros'),
		url(r'^del/libro/(?P<id_prod>.*)/$', 'del_view', name= 'vista_eliminar_cosmetico'),

		#biblioteca
		url(r'^add/biblioteca/$','agregar_biblioteca_view', name ='vista_agregar_biblioteca'),
		url(r'^edit/biblioteca/(?P<id_biblioteca>.*)/$','editar_biblioteca_view', name ='vista_editar_biblioteca'),
		url(r'^eliminar/biblioteca/(?P<id_biblioteca>.*)/$','eliminar_biblioteca_view', name = 'vista_eliminar_biblioteca'),

		#buscar
		url(r'^buscar/$','add_buscar_view', name= 'vista_buscar'), 
		url(r'^$','add_buscar_view', name= 'vista_principal'), 

		url(r'^registro/$','register_view', name= 'vista_registro'),


		#BUSCAR LIBRO POR TITULO, AUTOR O CATEGORIA
		url(r'^consultar_disponibles/$','consultar_disponibles_view', name= 'vista_consultar_disponibles'),

		url(r'^consultarlibrocodigo/$','consultar_codigo_view', name = 'vista_consultar_codigo'),
		url(r'^consultas/$','consultas_view', name = 'vista_consultas'),

		#info sobre nosotros
		url(r'^info/$','info_view', name = 'vista_info'),

)
