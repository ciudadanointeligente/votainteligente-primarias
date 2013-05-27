# coding= utf-8
from django.core.management.base import BaseCommand, CommandError
from elecciones.models import Candidato, Eleccion
import csv

class CandidatosLoader:
	def detectCandidate(self, line):
		eleccion = self.detectEleccion(line)
		nombre_candidato = line[1].decode('utf-8').strip()
		partido_candidato = line[2].decode('utf-8').strip()
		candidato, created = Candidato.objects.get_or_create(nombre=nombre_candidato, eleccion=eleccion, partido=partido_candidato)
		return candidato

	def detectEleccion(self, line):
		nombre_eleccion = line[0].decode('utf-8').strip()
		eleccion, created = Eleccion.objects.get_or_create(nombre=nombre_eleccion)
		return eleccion


class Command(BaseCommand):
    def handle(self, *args, **options):
        reader = csv.reader(open(args[0], 'rb'), delimiter=',')

        candidatos_loader = CandidatosLoader()
        for line in reader:
            candidato = candidatos_loader.detectCandidate(line)
            if candidato is not None:
            	print u"Eleccion: "+ candidato.eleccion.nombre+u" | Candidato: "+candidato.nombre