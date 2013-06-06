# coding= utf-8
from django.core.management.base import BaseCommand, CommandError
from elecciones.models import Candidato, Eleccion, Contacto
from django.core.validators import email_re
from popit.models import ApiInstance as PopitApiInstance
from django.conf import settings
import csv


class ContactosLoader:
	def __init__(self):
		self.failed = []
		self.empty = []
		self.popit_api_instance = None

	def getPopitApiInstance(self):
		if self.popit_api_instance is None:
			api_instance, created = PopitApiInstance.objects.get_or_create(url=settings.POPIT_API_URL)
			self.popit_api_instance = api_instance
		return self.popit_api_instance


	def detectCandidate(self, line):
		nombre_candidato = line[0].decode('utf-8').strip()
		nombre_eleccion = line[1].decode('utf-8').strip()
		eleccion, created = Eleccion.objects.get_or_create(nombre=nombre_eleccion)
		
		candidato, created = Candidato.objects.get_or_create(
			api_instance= self.getPopitApiInstance(),
			nombre=nombre_candidato, 
			eleccion=eleccion)
		return candidato

	def detectContacto(self, line):
		candidato = self.detectCandidate(line)
		valor = line[2].decode('utf-8').strip()
		if not valor:
			empty_data = {
				candidato.eleccion.nombre,
				candidato.nombre
			}
			self.empty.append(empty_data)
			return None

		if email_re.match(valor):

			contacto, created = Contacto.objects.get_or_create(valor=valor, candidato=candidato)
			return contacto
		failed_data = {
			candidato.eleccion.nombre,
			candidato.nombre,
			valor
		}
		self.failed.append(failed_data)
		return None


class Command(BaseCommand):
    def handle(self, *args, **options):
        reader = csv.reader(open(args[0], 'rb'), delimiter=',')

        contactos_loader = ContactosLoader()
        for line in reader:
            contacto = contactos_loader.detectContacto(line)
            if contacto is not None:
            	print u"Eleccion: "+ contacto.candidato.eleccion.nombre+u" | Candidato: "+contacto.candidato.nombre\
            	+u" | Contacto: "+contacto.valor

        print u"Los siguientes contactos no pudieron ser ingresados"
        print contactos_loader.failed

        print u"Los siguientes contactos están vacíos"
        print contactos_loader.empty