# coding= utf-8
from django.core.management.base import BaseCommand, CommandError
from elecciones.models import Candidato, Eleccion, Contacto
from django.core.validators import email_re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import csv


class ContactosLoader:
    def __init__(self):
        self.failed = []
        self.empty = []

    def detectCandidate(self, line):
        nombre_candidato = line[0].decode('utf-8').strip()
        

        query = Candidato.objects.filter(nombre=nombre_candidato)
        if not query.count():
            print "no pude encontrar a "+ nombre_candidato
        else:
            candidato = query[0]
            email = line[2].decode('utf-8').strip()
            try:
                validate_email(email)
                Contacto.objects.get_or_create(candidato=candidato, valor=email)
                
            except:
                pass


            #Contacto.objects.get_or_create()
        return None
        # eleccion, created = Eleccion.objects.get_or_create(nombre=nombre_eleccion)
        # candidato, created = Candidato.objects.get_or_create(nombre=nombre_candidato, eleccion=eleccion)
        # return None

    def detectContacto(self, line):
        candidato = self.detectCandidate(line)
        return None
        # valor = line[2].decode('utf-8').strip()
        # if not valor:
        #   empty_data = {
        #       candidato.eleccion.nombre,
        #       candidato.nombre
        #   }
        #   self.empty.append(empty_data)
        #   return None

        # if email_re.match(valor):

        #   contacto, created = Contacto.objects.get_or_create(valor=valor, candidato=candidato)
        #   return contacto
        # failed_data = {
        #   candidato.eleccion.nombre,
        #   candidato.nombre,
        #   valor
        # }
        # self.failed.append(failed_data)


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