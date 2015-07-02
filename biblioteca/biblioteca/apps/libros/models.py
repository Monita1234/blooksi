from django.db import models
from django.contrib.auth.models import User
#-*-coding: utf-8-*-

tipo_id = (
	('cedula', 'cedula'),
	('ti', 'ti'),
	('pasaporte', 'pasaporte'),
	('libreta militar', 'libreta militar'),
)


#Clase "Tipo_Usuario" Yaki ft Jennifer
class Tipo_Usuario (models.Model):
	nombre = models.CharField(max_length = 100)
	def __unicode__ (self):
		return self.nombre


genero= (
	('femenino', 'Femenino'),
	('masculino', 'Masculino'),
)


#estado prestamo 
estado_prestamo = (
	('Reservado', 'Reservado'),
('Cancelado', 'Cancelado'),
('Efectuado', 'Efectuado'), 
('Devuelto', 'Devuelto'), 
	)

estado = (
	('bueno', 'Bueno'),

('regular','Regular'),
('malo', 'Malo'),
)



#Clase "Editorial" Las Primas
class Editorial (models.Model):
	nombre 		= models.CharField(max_length=200)
	direccion 	= models.CharField(max_length=200)
	telefono 	= models.CharField(max_length=200)
	correo 		= models.CharField(max_length=200)

	def __unicode__ (self):
		return self.nombre

#Clase "Evelin ft Carolina"
class Categoria (models.Model):
	nombre = models.CharField(max_length = 200)

	def __unicode__(self):
		return self.nombre



#Clase "Autor" Poto, George
class Autor (models.Model):
	nombre_autor			=	models.CharField(max_length= 100)
	nacionalidad			=	models.CharField(max_length= 100)
	fecha_nacimiento		=	models.DateField()
	categoria				=	models.ManyToManyField(Categoria, null = True, blank = True)
	def __unicode__ (self):
		return self.nombre_autor

	
#Clase "Ciudad" Stefy ft Gomez
class Ciudad (models.Model):
	nombre = models.CharField(max_length = 200)
	
	def __unicode__ (self):
		return self.nombre


# cuando una clase depende de otra esta se coloca al final, 
# como en este caso; la clase libro depende de la clase categoria 
#Clase "libro" Verito ft Sofi
class Libro (models.Model): 
	def url (self,filename): 
		ruta = "MultimediaData/Libro/%s/%s"%(self.nombre_libro, str(filename))
		return ruta

	nombre_libro	= models.CharField(max_length = 200)
	autor			= models.ForeignKey(Autor)#Las llaves foraneas no deben ser nulas
	imagen			= models.ImageField(upload_to = url, null = True, blank = True)
	categoria		= models.ManyToManyField(Categoria, null = True, blank = True)
	editorial		= models.ForeignKey(Editorial, on_delete = models.PROTECT) 
	paginas			= models.IntegerField()
	version			= models.CharField(max_length = 10)
	tomo			= models.IntegerField()
	codigo			= models.CharField(max_length = 200, unique = True)# Con el atributo de unique el codigo se define como unico por lo que NO permitira ingresar un libro con el mismo codigo.
	isbn			= models.CharField(max_length = 200, null = True, blank = True)
	estado			= models.CharField(max_length = 200, choices = estado)
	disponibilidad  = models.BooleanField()
	observacion		= models.TextField(max_length= 400, null = True, blank = True)
	fecha_publicacion	= models.DateField()
	fecha_adquisicion	= models.DateField()
	

	def __unicode__(self):
		return self.nombre_libro

#Clase "Biblioteca" Las Primas"
class Biblioteca (models.Model):
	nombre  	=models.CharField(max_length=200)
	direccion 	=models.CharField(max_length=200)
	telefono	=models.CharField(max_length=200)
	correo 		=models.CharField(max_length=200)
	reglamento  =models.TextField(max_length=200)

	def __unicode__ (self):
		return self.nombre


#Clase "Usuario" Mary ft Cesar
class Usuario (models.Model):

	def url (self,filename):
		ruta = "MultimediaData/Users/%s/%s"%(self.user.username, filename)
		return ruta

	nombre         			 = 	models.CharField(max_length = 100)
	apellido       			 = 	models.CharField(max_length = 100)
	tipo_id					 = 	models.CharField(max_length = 100, choices = tipo_id)
	identificacion     	   	 = 	models.CharField(max_length = 100, unique = True)
	fecha_nac       	     = 	models.DateField()
	telefono        	   	 = 	models.CharField(max_length = 100)		
	direccion        	   	 = 	models.CharField(max_length = 100)
	genero					 = 	models.CharField(max_length = 200, choices = genero)
	ciudad                   = 	models.ForeignKey(Ciudad)
	tipo_usuario             =	models.ForeignKey(Tipo_Usuario)
	user 					 =	models.OneToOneField(User)
	photo 					 =	models.ImageField(upload_to = url, null = True, blank = True)
	tiene_prestamo 			 =	models.BooleanField(default = False)

	def __unicode__ (self):
		return self.nombre 

#Clase "Bibliotecario" Stefy ft Gomez 
class Bibliotecario (models.Model):
	nombre 			= models.CharField(max_length = 200)
	apellidos		= models.CharField(max_length = 200)
	telefono		= models.CharField(max_length = 200)
	direcccion		= models.CharField(max_length = 200)
	correo			= models.CharField(max_length = 200)
	genero			= models.CharField(max_length = 200, choices = genero)
	#usuario 		= models.()

	def __unicode__ (self):
		return self.nombre


#clase "Prestamo" Poto, George
class Prestamo (models.Model):
	fecha_prestamo 	=  models.DateField(auto_now =True) # 
	fecha_devolucion=  models.DateField() 
	libro 			=  models.ForeignKey(Libro)#
	bibliotecario   =  models.CharField(max_length=100 , null = True, blank = True) 
	usuario 		=  models.ForeignKey(Usuario)# captura  usuario que reservo el libro 
	estado_prestamo =  models.CharField(max_length = 200, choices = estado_prestamo)#
	
	def __unicode__ (self):
		return self.libro.nombre_libro 

class Busqueda (models.Model):
	busqueda = models.CharField(max_length = 100)
	fecha 	 = models.DateField(auto_now=True)
	resultados = models.BooleanField(default=True)

	def __unicode__ (self):
		return self.busqueda

