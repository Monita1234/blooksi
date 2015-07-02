
#-*-coding: utf-8-*-
# Vistas de la aplicacion libros
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from biblioteca.apps.libros.forms import *#add_prestamo_form, add_autor_form, delete_prestamo_form, edit_prestamo_form, edit_autor_form, add_editorial_form, add_categoria_form, add_bibliotecario_form, edit_bibliotecario_form, add_usuario_form, edit_usuario_form, add_ciudad_form, edit_ciudad_form, add_tipo_usuario_form, agregar_libro_form, agregar_biblioteca_form
from biblioteca.apps.libros.models import *#Prestamo, Autor, Editorial, Categoria, Bibliotecario, Usuario, Ciudad, Tipo_Usuario, Libro, Biblioteca
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth.models import User
from datetime import date
import django

from django.utils import simplejson



def administrar_view (request):
	return render_to_response('libros/administrar.html', context_instance = RequestContext(request))

def consultas_view (request):
	return render_to_response('libros/consultas.html', context_instance = RequestContext(request))


# PASO 1 reservar siver para  Bibliotecario y para usuarios registrados
def reservar_view(request,id_libro): #crear una reserva en estado RESERVADO
	if request.user.is_authenticated:# and request.user.is_staff:
		info = "" 
		#if request.user_is_authenticated() and request.user_is_staff():#modificado el 10 de abril
		if request.method == "POST": #si es POST
			formulario = add_prestamo_form(request.POST)
			if formulario.is_valid():
				add = formulario.save(commit =False)
				x = Libro.objects.get(id=id_libro)# modificacion 20 marzo 2015
				add.libro = x
				if date.today() <= add.fecha_devolucion:
					try: #guarda datos del bibliotecario al e
						y = Usuario.objects.get(tipo_usuario__nombre = "bibliotecario", user_id = request.user.id)
						#add.tipo_usuario = "bibliotecario"
						add.usuario = y
						add.bibliotecario = y.nombre
						add.estado_prestamo = "Efectuado"

						print request.user 
					except:
						print "Debe estar logueado"
					#estado_prestamo reservado, cancelado, efectuado
					try:
						if request.user.is_authenticated:# and request.user_is_staff:
							add.usuario = Usuario.objects.get(user__id = request.user.id)
							usu = add.usuario
							if usu.tipo_usuario.nombre != "bibliotecario":
								usu.estado = True
								print "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww"
								usu.update()
							
					except:
						info = "No se pudo guardar" # +++
					if x.disponibilidad == True:
						add.estado_prestamo = "Reservado"
						x.disponibilidad = False
					else:
						mensaje="El libro no esta disponible"
					x.save()
					add.save() # guarda la informacion
					info = "Guardado Satisfactoriamente"
					return HttpResponseRedirect ('/prestamos/')
				else:
					info="Error! La fecha de devolución ingresada no puede ser menor a la fecha actual "
		else:
			formulario = add_prestamo_form()
		ctx = {'form':formulario, 'informacion': info}
		return render_to_response('libros/add_prestamo.html', ctx, context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect ('/')

#PASO 2 aprobar el prestamo del libro LO REALIZA EL BIBLIOTECARIO
def aprobar_prestamo_view (request, id_prestar):
	if request.user.is_authenticated and request.user.is_staff:
		reservado = Prestamo.objects.get(id = id_prestar) 
		reservado.estado_prestamo = "Efectuado"

		reservado.save()
		return HttpResponseRedirect('/prestamos/')
	else:
		return HttpResponseRedirect ('/')

#PASO 3 puede servir par a los 2 usuarios que reservan BLIBLIOTECARIO y USUARIO REGISTRADO
def cancelar_prestamo_view (request, id_prestar):
	if request.user.is_authenticated and request.user.is_staff:
		reservado = Prestamo.objects.get(id = id_prestar) 
		reservado.estado_prestamo = "Cancelado"
		

		#reservado.libro.disponibilidad = True
		li =  reservado.libro
		li.disponibilidad = True
		li.save()


		#dev = cancelar prestamo
		reservado.save()
		return HttpResponseRedirect('/prestamos/')
	else:
		return HttpResponseRedirect ('/')

#PASO 4 VISTA PARA RETORNAR  LIBRO EN EL CUAL CAMBIE EL ESTADO DEL LIBRO A DISPONIBLE
def retornar_libro_view(request, id_prestar):
	if request.user.is_authenticated and request.user.is_staff:
		usu = ""
		pres = Prestamo.objects.get(pk = id_prestar)
		pres.fecha_devolucion = date.today()
		pres.estado_prestamo = 'Devuelto'
		li = pres.libro#.disponibilidad = True
		li.disponibilidad = True
		li.save()
		pres.save()
		return HttpResponseRedirect('/prestamos/')
	else:
		return HttpResponseRedirect ('/')

#PRESTA EL LIBRO EL BIBLIOTECARIO
def prestar_view(request, id_prestar):  #modificado el 17 de abril Funcion prestar
	if request.user.is_authenticated and request.user.is_staff:
		info = ""
		usu = ""
		pres = Prestamo.objects.get(pk = id_prestar)
		if usu:
			try:
				usu = Usuario.objects.get(tipo_usuario__nombre = "bibliotecario", user_id = request.user.id)
				pres.estado_prestamo = "Efectuado"
				pres.bibliotecario = usu.nombre
				pres.save()
				info = "Guardo Satisfactoriamente"
			except:
				print "no se pudo efectuar el prestamo"
				return HttpResponseRedirect ('/prestamo/%s'%(pres.id))
	else:
		return HttpResponseRedirect ('/')




#	ctx = {'form':formulario, 'informacion':info}
#	return render_to_response('libros/edit_prestamo.html',ctx , context_instance = RequestContext(request))

def edit_prestamo_view(request, id_editprest):
	if request.user.is_authenticated and request.user.is_staff:
		info = ""
		editprest = Prestamo.objects.get(pk = id_editprest)
		if request.method == "POST":
			formulario = add_prestamo_form(request.POST, instance=editprest)
			if formulario.is_valid():
				edit_prestamo = formulario.save(commit = False)
				
				edit_prestamo.save()
				info = "Guardo Satisfactoriamente"
				return HttpResponseRedirect ('/prestamos/')

		else:
			formulario = add_prestamo_form(instance = editprest)

		ctx = {'form':formulario, 'informacion':info}
		return render_to_response('libros/edit_prestamo.html',ctx , context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect ('/')

def eliminar_prestamo_view(request, id_prest):
	if request.user.is_authenticated and request.user.is_staff:

		info = "el prestamo se elimino safisfactoriamente"
		prest = Prestamo.objects.get(pk = id_prest)
		try:
			prest.delete()
			return HttpResponseRedirect ('/prestamos/')

		except:
			info = "La prestamo no existe"
			return HttpResponseRedirect ('/prestamos/')
	else:
		return HttpResponseRedirect ('/')


#autor
def add_autor_view(request):
	now = date.today()
	m=True
	if request.user.is_authenticated and request.user.is_staff:
		info = "" #inicializando
		if request.method == "POST": #si es POST
			formulario = add_autor_form(request.POST)
			if formulario.is_valid():
				add = formulario.save(commit =False)
				add.save()
				#formulario.save_m2m() # guarda la informacion
				ctx = {'form':formulario, 'now':now, 'm':m}
				info = "Guardado Satisfactoriamente"
				#return HttpResponseRedirect ('/autores/')
				return render_to_response('libros/add_autor.html', ctx, context_instance = RequestContext(request))
		else:
			formulario = add_autor_form()
		ctx = {'form':formulario, 'informacion': info ,'now':now}
		return render_to_response('libros/add_autor.html', ctx, context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect ('/')

	

def edit_autor_view(request, id_editautor):
	if request.user.is_authenticated and request.user.is_staff:
		info = ""
		editautor = Autor.objects.get(pk = id_editautor)
		if request.method == "POST":
			formulario = add_autor_form(request.POST, instance=editautor)
			if formulario.is_valid():
				edit_autor = formulario.save(commit = False)
				edit_autor.save()
				formulario.save_m2m()
				info = "Guardo Satisfactoriamente"
				return HttpResponseRedirect ('/autores/')

		else:
			formulario = edit_autor_form(instance = editautor)

		ctx = {'form':formulario, 'informacion':info}
		return render_to_response('libros/edit_autor.html',ctx , context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect ('/')



def eliminar_autor_view(request, id_aut):
	if request.user.is_authenticated and request.user.is_staff:
		info = ""
		a = None
		autor = Autor.objects.get (pk = id_aut)

		try:
			a = Libro.objects.get(autor__id = autor.id)
		except:
			pass
		if a == None:
			try:
				autor.delete()
				return HttpResponseRedirect('autores')
			except:
				info = "El Autor Que desea Eliminar No Existe"
				return render_to_response ('/autores')
		else:
				info = "El Autor No Se Puede Eliminar ya que Existe Algun Libro que Este Relacionado"
				return HttpResponseRedirect ('/autores')
	else:
		return HttpResponseRedirect ('/')



#editorial
def add_editorial_view(request):

	now = date.today()
	m=True
	if request.user.is_authenticated and request.user.is_staff:
		

		info = ""
		if request.method =="POST": #SI ES POST
			formulario = add_editorial_form(request.POST)
			if formulario.is_valid():
				add = formulario.save(commit = False)
				add.save()
				info = "Guardado Satisfactoriamente"
				ctx = {'form':formulario, 'now':now, 'm':m}
				informacion = "Se Guardo Satisfactoriamente"
				#return HttpResponseRedirect ('/editoriales/')
				return render_to_response('libros/add_editorial.html', ctx,context_instance = RequestContext(request))
		else:
			formulario = add_editorial_form()
		ctx = {'form':formulario,'info': info, 'now':now}
		return render_to_response('libros/add_editorial.html', ctx,context_instance = RequestContext(request))

	else:

		return HttpResponseRedirect ('/')

def edit_editorial_view(request, id_editorial):
	if request.user.is_authenticated and request.user.is_staff:
		info =""
		editorial = Editorial.objects.get(pk = id_editorial)

		if request.method == "POST":
			formulario = add_editorial_form(request.POST, instance = editorial)
			if formulario.is_valid():
				edit_editorial = formulario.save(commit = False)
				edit_editorial.save()
				info = " Guardado Satisfactoriamente"
				return HttpResponseRedirect ('/editoriales/')
		else:
			formulario = add_editorial_form(instance = editorial)
		ctx = {'form':formulario, 'informacion':info}
		return render_to_response('libros/edit_editorial.html', ctx,context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect ('/')

			
def eliminar_editorial_view(request, id_editorial):
	if request.user.is_authenticated and request.user.is_staff:

		info = ""
		e= None
		editorial = Editorial.objects.get (pk = id_editorial)

		try:
			e=Libro.objects.get(editorial__id =editorial.id)
		except:
			pass

		if e == None:

			try:
				editorial.delete()
				return HttpResponseRedirect('/editoriales/')

			except:
				info = "La Editorial Que desea Eliminar No Existe"
				return render_to_response ('/editoriales')
		else:

				info="La Editorial No Se Puede Eliminar ya que Existe Algun Libro que Este Relacionado"
				return HttpResponseRedirect('/editoriales/')
	else:
		return HttpResponseRedirect ('/')



#categoria
def add_categoria_view(request):

	now = date.today()
	m=True
	if request.user.is_authenticated and request.user.is_staff:

		info = ""
		if request.method == "POST":
			formulario = add_categoria_form(request.POST, request.FILES)
			if formulario.is_valid():
				add = formulario.save (commit = False)
				add.save()
				ctx = {'form':formulario, 'now':now, 'm':m}
				info = "Guardado Satisfactoriamente"
				return render_to_response ('libros/agregar_categoria.html', ctx,context_instance =RequestContext(request))
				
		else:
			formulario = add_categoria_form()
		ctx = {'form':formulario, 'informacion':info, 'now':now}
		return render_to_response ('libros/agregar_categoria.html', ctx,context_instance =RequestContext(request))
	else:
		return HttpResponseRedirect ('/')


		

	

def editar_categoria_view (request, id_prod):
	if request.user.is_authenticated and request.user.is_staff:

		info = ""
		prod = Categoria.objects.get(pk = id_prod)
		if request.method =="POST":
			formulario = add_categoria_form(request.POST, instance= prod)
			if formulario.is_valid():
				edit_prod = formulario.save(commit = False) 
				edit_prod.save()
				info ="Guardado Satisfactoriamente"
				return HttpResponseRedirect ('/categorias')
		else:
			formulario = add_categoria_form(instance = prod)

		ctx = {'form': formulario, 'informacion':info}
		return render_to_response('libros/editar_categoria.html', ctx, context_instance= RequestContext(request))
	else:
		return HttpResponseRedirect ('/')



def eliminar_categoria_view(request, id_prod):
	if request.user.is_authenticated and request.user.is_staff:

		info = "la categoria se elimino safisfactoriamente"
		prod = Categoria.objects.get(pk = id_prod)
		
		try:
			prod.delete()
			return HttpResponseRedirect ('/categorias')

		except:
			info = "La categoria no existe"
			return HttpResponseRedirect ('/categorias')
	else:
		return HttpResponseRedirect ('/')




#bibliotecario
def add_bibliotecario_view(request):
	if request.user.is_authenticated and request.user.is_staff:
		info = "inicializando"
		if request.method == "POST":
			formulario = add_bibliotecario_form(request.POST)
			if formulario.is_valid():
				add = formulario.save(commit = False)

				add.save() # guarda la informacion
			# guarda las relaciones ManyToMany
				info = "Guardado Satisfactoriamente"
				return HttpResponseRedirect ('/bibliotecarios/')
		else:
			formulario = add_bibliotecario_form()
		ctx = {'form':formulario, 'informacion':info}
		return render_to_response('libros/add_bibliotecario.html', ctx,context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect ('/')



def edit_bibliotecario_view(request, id_biblio):
	if request.user.is_authenticated and request.user.is_staff:

		info = ""
		biblio = Bibliotecario.objects.get(pk = id_biblio)
		if request.method == "POST":
			formulario = add_bibliotecario_form(request.POST, instance= biblio )
			if formulario.is_valid():
				edit_biblio = formulario.save(commit = False)
		
				edit_biblio.save()
				info = "Guardado Satisfactoriamente"
				return HttpResponseRedirect('/bibliotecarios/')
		else:
			formulario = add_bibliotecario_form(instance = biblio)
		ctx = {'form':formulario, 'informacion':info}
		return render_to_response('libros/edit_bibliotecario.html', ctx,context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect ('/')


def del_bibliotecario_view(request, id_biblio):
	if request.user.is_authenticated and request.user.is_staff:

		info = "inicializando"
		biblio = Bibliotecario.objects.get(pk = id_biblio)
		try:
			biblio.delete()
			return HttpResponseRedirect('/bibliotecarios')
		except:
			info = "Bibliotecario no se puede eliminar"
			return HttpResponseRedirect('/bibliotecarios')
	else:
		return HttpResponseRedirect ('/')


#usuario
def add_usuario_view(request):
	if request.user.is_authenticated and request.user.is_staff:

		info = "inicializando"
		if request.method == "POST": #si es POST
			formulario = add_usuario_form(request.POST)
			if formulario.is_valid():
				add = formulario.save(commit =False)
				add.save() # guarda la informacion
				info = "Guardado Satisfactoriamente"
				return HttpResponseRedirect ('/usuarios/')
		else:
			formulario = add_usuario_form()
		ctx = {'form':formulario, 'informacion': info}
		return render_to_response('libros/add_usuario.html', ctx,context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect ('/')


def edit_usuario_view(request, id_usua):
	if request.user.is_authenticated and request.user.is_staff:

		info = ""
		usua = Usuario.objects.get(pk = id_usua)
	
		if request.method == "POST":
			formulario = add_usuario_form(request.POST, request.FILES, instance=usua)
			formulario_user = edit_user_form(request.POST, instance = usua.user)
			if formulario.is_valid() and formulario_user.is_valid():
				edit_usua = formulario.save(commit = False)
				#e_user = 	
				#x = formulario_user.cleaned_data['password']
				edit_usua.save()
				usua.user.set_password(formulario_user.cleaned_data['clave'])
				#formulario_user.set_password("123123")
				formulario_user.save()
				info = "Guardado Satisfactoriamente"
				return HttpResponseRedirect('/usuarios/')
		else:
			formulario = add_usuario_form(instance = usua)
			formulario_user = edit_user_form(instance = usua.user)
		ctx = {'form':formulario, 'informacion':info, 'form_user': formulario_user}
		return render_to_response('libros/edit_usuario.html', ctx,context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect ('/')



def del_usuario_view(request,id_usua):	
	info = "Se inicio proceso de eliminacion del Usuario"
	usua = Usuario.objects.get(pk = id_usua)
	
	try:
		usua.delete()
		return HttpResponseRedirect ('/usuarios')

	except:
		info= "El Usuario que desea eliminar no existe"
		#return render_to_response('home/usuario.html')
		return HttpResponseRedirect ('/usuarios')



#tipo_usuario
def add_tipo_usuario_view(request):
	now = date.today()
	m=True
	if request.user.is_authenticated and request.user.is_staff:

		info = ""
		if request.method == "POST": #si es POST
			formulario = add_tipo_usuario_form(request.POST)
			if formulario.is_valid():
				add = formulario.save(commit =False)
				add.save() # guarda la informacion
				info = "Guardado Satisfactoriamente"
				ctx = {'form':formulario, 'now':now, 'm':m}
				return render_to_response('libros/add_tipo.html', ctx,context_instance = RequestContext(request))
		else:
			formulario = add_tipo_usuario_form()
		ctx = {'form':formulario, 'informacion': info, 'now':now}
		return render_to_response('libros/add_tipo.html', ctx,context_instance = RequestContext(request))
	
	else:
		return HttpResponseRedirect ('/')



def edit_tipo_usuario_view(request, id_tipo):
	if request.user.is_authenticated and request.user.is_staff:

		info = ""
		tipo = Tipo_Usuario.objects.get(pk = id_tipo)
		if request.method == "POST":
			formulario = add_tipo_usuario_form(request.POST, request.FILES, instance=tipo)
			if formulario.is_valid():
				edit_tipo = formulario.save(commit = False)
				
				edit_tipo.save()
				info = "Guardo Satisfactoriamente"
				return HttpResponseRedirect ('/tipos_usuarios/')

		else:
			formulario = add_tipo_usuario_form(instance = tipo)

		ctx = {'form':formulario, 'informacion':info}
		return render_to_response('libros/edit_tipo.html',ctx , context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect ('/')	

def eliminar_tipo_usuario_view(request, id_tipo):
	if request.user.is_authenticated and request.user.is_staff:

		info = "El tipo de usuario se elimino satisfactoriamente"
		try:
			tipo = Tipo_Usuario.objects.get(pk = id_tipo)
			tipo.delete()
			return HttpResponseRedirect('/tipos_usuarios')
		except:
			info = "El tipo de usuario que desea eliminar no existe"
			return HttpResponseRedirect ('/tipos_usuarios')   
	else:
		return HttpResponseRedirect ('/')



#ciudad
def add_ciudad_view(request):
	now = date.today()
	m=True
	if request.user.is_authenticated and request.user.is_staff:

		info = "inicializando"
		if request.method == "POST":
			formulario = add_ciudad_form(request.POST)
			if formulario.is_valid():
				add = formulario.save(commit = False)

				add.save() # guarda la informacion

			# guarda las relaciones ManyToMany
				info = "Guardado Satisfactoriamente"
				ctx = {'form':formulario, 'now':now, 'm':m}
				#return HttpResponseRedirect ('/ciudades/')
				return render_to_response('libros/add_ciudad.html', ctx,context_instance = RequestContext(request))
		else:
			formulario = add_ciudad_form()
		ctx = {'form':formulario, 'informacion':info, 'now':now}
		return render_to_response('libros/add_ciudad.html', ctx,context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect ('/')



def edit_ciudad_view(request, id_ciu):
	if request.user.is_authenticated and request.user.is_staff:
	
		info = ""
		ciu = Ciudad.objects.get(pk = id_ciu)
		if request.method == "POST":
			formulario = add_ciudad_form(request.POST, instance= ciu)
			if formulario.is_valid():
				edit_ciu = formulario.save(commit = False)
		
				edit_ciu.save()
				info = "Guardado Satisfactoriamente"
				return HttpResponseRedirect('/ciudades/')
		else:
			formulario = add_ciudad_form(instance = ciu)
		ctx = {'form':formulario, 'informacion':info}
		return render_to_response('libros/edit_ciudad.html', ctx,context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect ('/')


def del_ciudad_view(request, id_ciu):
	if request.user.is_authenticated and request.user.is_staff:

		info = "inicializando"
		ciu = Ciudad.objects.get(pk = id_ciu)
		try:
			ciu.delete()
			return HttpResponseRedirect('/ciudades')
		except:
			info = "Ciudad no se puede eliminar"
			return HttpResponseRedirect('/ciudades')	
	else:
		return HttpResponseRedirect ('/')
	


#libro
def agregar_libro_view (request):
	now = date.today()
	m=True
	if request.user.is_authenticated and request.user.is_staff:

		info = ""
		mensaje = ""

		if request.method == "POST":
			formulario = agregar_libro_form(request.POST, request.FILES)
			if formulario.is_valid():
				add = formulario.save(commit = False)
				#add.fecha_adquisicion
				#add.fecha_publicacion
				if add.fecha_adquisicion >=add.fecha_publicacion:


					add.save()
					ctx = {'form':formulario, 'now':now, 'm':m}
					info = "Guardado satisfactoriamente"
					return render_to_response('libros/agregar_libro.html', ctx,context_instance = RequestContext(request))
				else:
					mensaje="Error ! La fecha de adquisicion ingresada no puede ser menor a la de publicacion "
		else:
			formulario = agregar_libro_form()
		ctx = {'form':formulario, 'informacion':info, 'mensaje': mensaje, 'now':now}
		return render_to_response('libros/agregar_libro.html', ctx,context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect ('/')

		


#Nuevo
def editar_libro_view (request, id_prod):
	if request.user.is_authenticated and request.user.is_staff:

		info = ""
		prod = Libro.objects.get(pk = id_prod)
		if request.method == "POST":
			formulario = agregar_libro_form(request.POST,request.FILES, instance= prod) #FILES para agregar imagenes
			if formulario.is_valid():
				edit_prod = formulario.save(commit = False)
				formulario.save_m2m()
				edit_prod.save()
				info = "Guardado satisfactoriamente"
				return HttpResponseRedirect ('/libro/%s'%(prod.id))
				
		else:
			formulario = agregar_libro_form(instance = prod)

		ctx = {'form':formulario, 'informacion':info}
		return render_to_response('libros/editar_libro.html', ctx,context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect ('/')


#ELIMINAR LIBRO 
def del_view (request, id_prod): #obteniendo el objeto a eliminar 
	if request.user.is_authenticated and request.user.is_staff:
	
		info = "Se inicio el proceso de eliminacion"
		l = None # nul o vacio donde se puede almacenar un objeto
		#opc2 = []
		prod = Libro.objects.get(pk = id_prod)

		try: 
			l=prestamo.objects.get(libro__id =prod.id )
			#opc2 = prestamo.objects.filter( libro__id=prod.id)
		except: 
			pass

		if l== None: 

			try:
				prod.delete()
				return HttpResponseRedirect ('/libros')#cuando no se trabaja con paginator se agrega sin numero 
			except: 
				info = "EL libro que desea eliminar no existe"
				return HttpResponseRedirect ('/libros')
		else: 
				info = "El libro no se puede eliminar ya que existe algun prestamo asociado"		
				return HttpResponseRedirect ('/libros')
	else:
		return HttpResponseRedirect ('/')



#biblioteca

def agregar_biblioteca_view(request):
	if request.user.is_authenticated and request.user.is_staff:
		info ="inicializando"
		if request.method == "POST":
			formulario = agregar_biblioteca_form(request.POST)
			if formulario.is_valid():
				add = formulario.save(commit = False)
				add.save()#guarda la informacion
				info = "Guardo Satisfactoriamente"
				return HttpResponseRedirect ('/biblioteca/%s'%add.id)
		else:
			formulario =agregar_biblioteca_form()
		ctx = {'form':formulario,'informacion':info}
		return render_to_response('libros/agregar_biblioteca.html',ctx,context_instance = RequestContext(request))

	else:
		return HttpResponseRedirect ('/')


def editar_biblioteca_view(request,id_biblioteca):
	if request.user.is_authenticated and request.user.is_staff:
		info =""
		biblioteca = Biblioteca.objects.get(pk =id_biblioteca)
		if request.method == "POST":
			formulario = agregar_biblioteca_form(request.POST, instance= biblioteca)
			if formulario.is_valid():
				edit_biblioteca= formulario.save(commit = False)
				edit_biblioteca.save()
				info = "Guardo Satisfactoriamente"
				return HttpResponseRedirect ('/biblioteca/%s'% edit_biblioteca.id)
		else:

			formulario = agregar_biblioteca_form(instance = biblioteca)

		ctx = {'form':formulario,'informacion':info}
		return render_to_response('libros/editar_biblioteca.html',ctx,context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect ('/')



def eliminar_biblioteca_view(request, id_biblioteca):
	if request.user.is_authenticated and request.user.is_staff:
		info = "la biblioteca se elimino Satisfactoriamente"
		biblioteca = Biblioteca.objects.get(pk = id_biblioteca)
		try:
			biblioteca.delete()
			return HttpResponseRedirect ('/bibliotecas')
		except:
			info = "la biblioteca no existe"
			return render_to_response ('/bibliotecas')
	else:
		return HttpResponseRedirect ('/')



#buscar
def add_buscar_view(request):
	#if request.user.is_authenticated and request.user.is_staff:

		libros = []
		categorias = []
		autores = []
		editoriales = []
		busqueda = ""
		mensaje =""
		mensaje_error = False
		info = "inicializando"
		if request.method == "POST": #si es POST
			formulario = add_buscar_form(request.POST)
			busqueda = request.POST['busqueda']	
			if formulario.is_valid():
			#agregar	
				busqueda = formulario.cleaned_data['busqueda']
				add = formulario.save(commit =False)
				#add.save() # guarda la informacion
				info = "Guardado Satisfactoriamente"
				#buscar
				try:
					editoriales = Libro.objects.filter(editorial__nombre__iexact = busqueda)
					libros= Libro.objects.filter(nombre_libro__icontains= busqueda)
					autores = Libro.objects.filter(autor__nombre_autor__icontains = busqueda)

					cat = Categoria.objects.get(nombre__iexact=busqueda)
					categorias = Libro.objects.filter(categoria = cat)
					#codigo = Libro.objects.get(codigo= int(busqueda)) 
				except:
					print "QQQQQQQQQQQQQQQQQQQQQQQ", libros, categorias, autores , editoriales 
					if editoriales and libros and autores and categorias:
						pass
					else:
						mensaje_error = True
					#libro = Libro.objects.all(request.POST)
				if libros or categorias or autores or editoriales:
					add.resultados=True
				else:
					add.resultados=False
				add.save()
				print "-------------------------\n"
				print editoriales
		else:
			formulario = add_buscar_form()
		ctx = {'form':formulario, 'informacion': info, 'mensaje':mensaje, 'mensaje_error':mensaje_error, 'libro':libros, 'categoria':categorias, 'autor':autores, 'editorial':editoriales, 'busqueda':busqueda}
		return render_to_response('libros/add_buscar.html', ctx,context_instance = RequestContext(request))
	#else:
		#return HttpResponseRedirect ('/')


#consultar usuario (maria y cesar se aman)
def consultar_usuario_id_view(request):
	if request.user.is_authenticated and request.user.is_staff:
		mensaje = ""
		usua =""
		if request.user.is_authenticated():
			if request.method == "POST":
				formulario	 = consultar_usuario_id_form(request.POST) #creamos un objeto de Loguin form
				if formulario.is_valid(): #si la informacion enviada es correcta
					tipo_id=formulario.cleaned_data['tipo_id']
					ide= formulario.cleaned_data['identificacion'] #guarda informacion ingresada del formulario
					try:
						usua=Usuario.objects.get(tipo_id=tipo_id,identificacion=ide)
						mensaje = "Se encontro el Usuario con el Numero de Identificacion " + ide + " sus Datos son:"

						#return HttpResponseRedirect('/usuario/%s'%usua.id)		
					except:
						mensaje = "Usuario no encontrado" #verificampos si el usuario ya esta autenticado o logueado}
				else:
					mensaje = "El campo no debe estar vacio, por favor ingrese un valor"
							
		 #si esta logueando lo redirigimos a la pagina principal
		else: #si no esta authenticado
			return HttpResponseRedirect('/')
		formulario = consultar_usuario_id_form() #creamos un formulario nuevo en limpio
		ctx = {'form':formulario, 'mensaje':mensaje, 'usuario':usua} # variable de contexto para pasar info a login.html
		return render_to_response('home/consultar.html', ctx,context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect ('/')


#register view

def register_view(request):
		now = date.today()
		m=True
		
		mensaje = ""
		fecha_nac=""
		if request.method == "POST":
			form_a = RegisterForm(request.POST)
			form_b = add_usuario_form(request.POST, prefix = "b")
			if form_b.is_valid() and form_a.is_valid():
				usuario 		= form_a.cleaned_data['username']
				email 			= form_a.cleaned_data['email']
				password_one	= form_a.cleaned_data['password_one']
				password_two 	= form_a.cleaned_data['password_two']
				tipo_usuario 	= form_b.cleaned_data['tipo_usuario']
				u = User.objects.create_user(username = usuario,email = email, password = password_one)

				if  form_b.cleaned_data['fecha_nac'] < now:

					try:
					
						u.save() #guarda el objeto
						b = form_b.save(commit=False)
						b.tipo_usuario = tipo_usuario
						'''b.add_usuario_form = a
						'''
						b.user= u 
						
						b.save()
					
					except:
						pass
					ctx = {'form_a':form_a, 'form_b':form_b, 'now':now, 'm':m}
					#return HttpResponseRedirect ('/registro')
					return render_to_response('home/register.html/', ctx,context_instance = RequestContext(request))
				else:
					mensaje = "Error! La Fecha de nacimiento debe ser menor  a la fecha actual"	
			else:
				info = "fallo"

		else:
			form_a = RegisterForm()
			form_b = add_usuario_form(prefix = "b")
		ctx = {'form_a':form_a, 'form_b':form_b, 'now':now, 'mensaje':mensaje}	
		return render_to_response ('home/register.html',ctx, context_instance= RequestContext(request))	
		
		



#REGISTRAR BIBLIOTECARIO ---
def register_bibliotecario_view(request):
	if request.user.is_authenticated and request.user.is_staff:

		now = date.today()
		if (request.user.is_authenticated() and request.user.is_staff and request.user.is_superuser):
			if request.method == "POST":
				form_a = RegisterForm(request.POST)
				form_b = add_bibliotecario_form(request.POST, prefix = "b")
				if form_b.is_valid() and form_a.is_valid():
					usuario 		= form_a.cleaned_data['username']
					email 			= form_a.cleaned_data['email']
					password_one	= form_a.cleaned_data['password_one']
					password_two 	= form_a.cleaned_data['password_two']

					u = User.objects.create_user(username = usuario,email = email, password = password_one)
					b = form_b.save(commit=False)
					'''b.add_usuario_form = a
					'''
					try:
						tipo = Tipo_Usuario.objects.get(nombre='bibliotecario')
						b.tipo_usuario = tipo
						u.is_staff = True
						u.is_superuser = True
						u.save() #guarda el objeto
						b.user= u 
						b.save()
					except:
						mensaje = "No se puede crear un bibliotecario porque no existe un tipo bibliotecario"
					return HttpResponseRedirect('/bibliotecarios/')
					#return render_to_response('home/confirmacion.html',context_instance = RequestContext(request))
				else:
					info = "fallo"	
			else:
				form_a = RegisterForm()
				form_b = add_bibliotecario_form(prefix = "b")
			ctx = {'form_a':form_a, 'form_b':form_b, 'now':now}	
			return render_to_response ('home/register.html',ctx, context_instance= RequestContext(request))	

		else: #por sino es super administrador
			return HttpResponseRedirect('/bibliotecarios/')
	else:
		return HttpResponseRedirect ('/')


#VISTA DE BUSCAR LIBRO POR TITULO, CATEGORIA O AUTOR: CONSULTAR DISPONIBLES 
def consultar_disponibles_view (request): 
	if request.user.is_authenticated and request.user.is_staff:
		busqueda1 = []
		busqueda2 = []
		busqueda3 = []
		lista_cat = []
		formulario = buscar_form(request.POST)
		if request.method =="POST":
			if formulario.is_valid():
				c = formulario.cleaned_data ['busqueda']
				#print c

	#Aqui se esta utilizando un query 
				try:
					busqueda1 = Libro.objects.filter(nombre_libro__icontains = c, disponibilidad = True)# La palabra icontains se utiliza
					# para que encuentre a cualquier objeto que contenga la palabra q se guarda en la variable busqueda
					busqueda3 = Libro.objects.filter(autor__nombre__icontains	= c, disponibilidad = True)
					busqueda2 = Categoria.objects.get(nombre__icontains=c)# busqueda cuando hay una relacion de muchos a muchos 
					lista_cat = Libro.objects.filter(categoria = busqueda2, disponibilidad = True)
					print "se encontro  %s"%(c) 
				except:
					print "no se encontro nada %s"%(c) 
		#Funcion contains se refiere a sacar un nombre o titulo que contenga lo que se le esta pidiendo. 
		#c.lower () se utilizan para minusculas
		# Formulario vacio para obtener la informacion
		else:
			formulario = buscar_form()
		#c.upper() se utilizan para mayusculas
		# en esta parte a la variable ctx se le pasa lo que hay en el formulario y lo que se quiere buscar
		mensaje = "La busqueda ha sido exitosa"
		ctx = {'form': formulario, 'buscar1': busqueda1, 'buscar2': lista_cat, 'buscar3': busqueda3, 'msg':mensaje }
		return render_to_response('libros/consultar_disponibles.html',ctx,context_instance=RequestContext(request))

	else:
		return HttpResponseRedirect ('/')


def consultar_codigo_view(request):
	if request.user.is_authenticated and request.user.is_staff:
		disponibilidad = ""
		L = ""
		info=""
		formulario = consultar_codigo_form(request.POST)
		if request.method == "POST":
			if formulario.is_valid():
				c = formulario.cleaned_data['codigo']
				try:
					L =Libro.objects.get(codigo = c)
					info = "El libro esta disponible"
					return HttpResponseRedirect('/libro/%s'%L.id)
				except:
					print c
					info = "El libro con el codigo "+c+" no existe!!!!!"
		else:
			formulario = consultar_codigo_form()

		ctx = {'info':info,'form':formulario, 'libro_encontrado':L,}
		return render_to_response('libros/consultar_codigo.html',ctx,context_instance=RequestContext(request)) 
	else:
		return HttpResponseRedirect ('/')


