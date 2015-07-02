# Create your views here.
from django.shortcuts  import render_to_response
from django.template import RequestContext
from biblioteca.apps.libros.models import *#Prestamo, Autor, Editorial, Categoria, Bibliotecario, Usuario, Ciudad, Tipo_Usuario, Libro, Biblioteca
from datetime import date
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from biblioteca.apps.home.forms import libronuevo_form,Login_form
import django

from django.utils import simplejson


def index_view (request):
	return render_to_response('home/index.html', context_instance = RequestContext(request))
#administador
def administrar_view (request):
	return render_to_response('libros/administrar.html', context_instance = RequestContext(request))
def reservas_view (request):
	reservas = Prestamo.objects.filter(estado_prestamo="Reservado")
	ctx = {'reservas' :reservas}
	return render_to_response ('home/reservas.html', ctx, context_instance = RequestContext(request))



def single_autor_view(request, id_editautor):
	editautor = Autor.objects.get(id = id_editautor)
	ctx = {'autor':editautor}
	return render_to_response('home/single_autor.html',ctx,context_instance = RequestContext(request))

def prestamos_view(request):
	tipo = Prestamo.objects.filter()
	ctx = {'prestamos' :tipo}
	return render_to_response ('home/prestamos.html', ctx, context_instance = RequestContext(request))

def single_prestamo_view(request, id_editprest):
	editprest = Prestamo.objects.get(id = id_editprest)
	ctx = {'prestamo':editprest}
	return render_to_response('home/single_prestamo.html',ctx,context_instance = RequestContext(request))


#editorial
def editoriales_view(request):
	if request.method=="POST":
	
		if "product_id" in request.POST:
			try:
				l = None
				id_product = request.POST['product_id']
				p= Editorial.objects.get(pk=id_product)
				try:
					l = Libro.objects.get(editorial__id = id_product)
				except:
					l = None
				if l == None:
					p.delete()
					#p.delete()
					mensaje={"status":"True","product_id":id_product}
				return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')
			except:
				mensaje={"status":"False"}
				return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')
	lista_e = Editorial.objects.all()
	ctx = {'editoriales' :lista_e}
	return render_to_response ('home/editoriales.html', ctx, context_instance = RequestContext(request))

	#autor
def autores_view(request):
	if request.method=="POST":
	
		if "product_id" in request.POST:
			try:
				l = None
				id_product = request.POST['product_id']
				a = Autor.objects.get(pk=id_product)
				try:
					l = Libro.objects.get(autor__id = id_product)
				except:
					l = None
				if l == None:
					a.delete()
					#p.delete()
					mensaje={"status":"True","product_id":id_product}
				return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')
			except:
				mensaje={"status":"False"}
				return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')
	lista_a = Autor.objects.all()
	ctx = {'autores' :lista_a}
	return render_to_response ('home/autor.html', ctx, context_instance = RequestContext(request))




	
	

def single_editorial_view(request, id_editorial):
	editorial = Editorial.objects.get(id = id_editorial)
	ctx = {'editorial':editorial}
	return render_to_response('home/single_editorial.html',ctx, context_instance = RequestContext(request))

#categoria
def categorias_view (request):
	prod = Categoria.objects.filter()
	ctx = {'categorias':prod}
	return render_to_response('home/categorias.html',ctx, context_instance = RequestContext(request))

def single_categoria_view (request, id_prod):
	prod = Categoria.objects.get(id = id_prod)
	ctx = {'Categoria':prod,}
	return render_to_response ('home/single_categoria.html',ctx, context_instance = RequestContext(request))



#bibliotecario
def  bibliotecarios_view (request):
	biblio = Usuario.objects.filter(tipo_usuario__nombre = 'bibliotecario')
	ctx = {'bibliotecarios': biblio}
	return render_to_response ('home/bibliotecarios.html', ctx, context_instance = RequestContext(request))

def single_bibliotecarios_view(request, id_biblio):
	usua = Usuario.objects.get(id = id_biblio)
	ctx = {'usuario':usua}
	return render_to_response('home/single_usuario.html',ctx,context_instance = RequestContext(request))

#usuario
def usuarios_view(request):
	
	if request.method=="POST":
	
		if "product_id" in request.POST:
			try:
				l = None
				id_usuario = request.POST['product_id']
				p = Usuario.objects.get(pk=id_usuario)
				u = User.objects.get (pk = p.user.id)
				try:
					l = Prestamo.objects.get(usuario__id = id_usuario, usuario__user__id = u.id)
				except:
					l = None
				if l == None:
					u.delete()
					#p.delete()
					mensaje={"status":"True","product_id":p.id}
				return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')
			except:
				mensaje={"status":"False"}
				return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')
	p = Usuario.objects.all()
	ctx = {'usuarios':p}
	return render_to_response ('home/usuarios.html', ctx, context_instance = RequestContext(request))

def single_usuario_view(request, id_usua):
	usua = Usuario.objects.get(id = id_usua)
	ctx = {'usuario':usua}
	return render_to_response('home/single_usuario.html',ctx,context_instance = RequestContext(request))

#tipo_usuario
def tipos_usuarios_view(request):


	if request.method=="POST":
	
		if "product_id" in request.POST:
			try:
				l = None
				id_product = request.POST['product_id']
				p = Tipo_Usuario.objects.get(pk=id_product)
				try:
					l = Usuario.objects.get(tipo_usuario__id = id_product)
				except:
					l = None
				if l == None:
					p.delete()
					#p.delete()
					mensaje={"status":"True","product_id":id_product}
				return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')
			except:
				mensaje={"status":"False"}
				return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')


	tipo = Tipo_Usuario.objects.all()
	ctx = {'tipos_usuarios' :tipo}
	return render_to_response ('home/tipo_usuario.html', ctx, context_instance = RequestContext(request))

def single_tipo_usuario_view(request, id_tipo):
	tipo = Tipo_Usuario.objects.get(id = id_tipo)
	ctx = {'tipos_usuarios' :tipo}
	return render_to_response ('home/single_tipo.html', ctx, context_instance = RequestContext(request))






	

def single_ciudades_view(request, id_ciu):
	ciu = Ciudad.objects.get(id = id_ciu) #obtenemos las categorias del producto encontrado
	ctx = {'ciudad':ciu}
	return render_to_response('home/single_ciudad.html',ctx,context_instance = RequestContext(request))

#ciudad
def  ciudades_view (request):
	if request.method=="POST":
	
		if "product_id" in request.POST:
			try:
				l = None
				id_product = request.POST['product_id']
				p = Ciudad.objects.get(pk=id_product)
				try:
					l = Usuario.objects.get(ciudad__id = id_product)
				except:
					l = None
				if l == None:
					p.delete()
					#p.delete()
					mensaje={"status":"True","product_id":id_product}
				return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')
			except:
				mensaje={"status":"False"}
				return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')
	lista_c = Ciudad.objects.all()
	ctx = {'ciudades' :lista_c}
	return render_to_response ('home/ciudades.html', ctx, context_instance = RequestContext(request))
#libro 
def libros_view (request):
	if request.method=="POST":
	
		if "product_id" in request.POST:
			try:
				l = None
				id_product = request.POST['product_id']
				p= Libro.objects.get(pk=id_product)
				try:
					l = Prestamo.objects.get(libro__id = id_product)
				except:
					l = None
				if l == None:
					p.delete()
					#p.delete()
					mensaje={"status":"True","product_id":id_product}
				return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')
			except:
				mensaje={"status":"False"}
				return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')
	lista_l = Libro.objects.all()
	ctx = {'libros' :lista_l}
	return render_to_response('home/libros.html',ctx, context_instance = RequestContext(request))

	

def single_libro_view (request, id_prod): 
	prod = Libro.objects.get(id = id_prod)
	#cat = prod.categoria.all()
	ctx = {'libro':prod}# 'categoria': cat}
	return render_to_response('home/single_libro.html',ctx, context_instance = RequestContext(request))

#biblioteca
def bibliotecas_view (request):
	b =Biblioteca.objects.filter()
	ctx = {'bibliotecas': b }
	return render_to_response('home/biblioteca.html',ctx, context_instance = RequestContext(request))

def single_biblioteca_view(request, id_biblioteca):
	b= Biblioteca.objects.get (id = id_biblioteca)
	ctx = {'biblioteca': b }
	return render_to_response('home/single_biblioteca.html',ctx,context_instance = RequestContext(request))

def libronuevo_view(request):
	info = "inicializando"
	fecha_inicio = ""
	nuevos = []
	h = date.today()
	mensaje = ""

	if request.method == "POST":
		formulario = libronuevo_form(request.POST)
		if formulario.is_valid():
			
			info = True 
			fecha_inicio = formulario.cleaned_data['fecha_inicio']
			
			if fecha_inicio < h:
				nuevos = Libro.objects.filter(fecha_publicacion__range =(fecha_inicio, h))#se hace un rango de los ultimos libros comprados
			else:
				mensaje = "no hay libros"

			formulario = libronuevo_form()
		ctx = {'form':formulario, 'informacion':info, 'nuevos':nuevos, 'mensaje':mensaje}
		return render_to_response ('home/libronuevo.html', ctx,context_instance =RequestContext(request))

	else:
		formulario = libronuevo_form()
	ctx = {'form':formulario, 'informacion':info, 'nuevos':nuevos, 'mensaje':mensaje}
	return render_to_response ('home/libronuevo.html', ctx,context_instance =RequestContext(request))

def login_view(request):
	mensaje = ""
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		if request.method == "POST":
			formulario = Login_form(request.POST)
			if formulario.is_valid():
				usu = formulario.cleaned_data['usuario']
				pas = formulario.cleaned_data['clave']
				usuario = authenticate(username = usu, password = pas)
				if usuario is not None and usuario.is_active:
					login(request, usuario)
					return HttpResponseRedirect('/')
				else:
					mensaje = "usuario y/o clave incorrecta"
		formulario = Login_form()
		ctx = {'form':formulario, 'mensaje':mensaje}
		return render_to_response ('home/login.html', ctx, context_instance =RequestContext(request))

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

