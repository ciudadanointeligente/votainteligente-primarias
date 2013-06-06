# coding= utf-8
from django.core.management.base import BaseCommand, CommandError
from elecciones.models import Candidato
from popit.models import ApiInstance as PopitApiInstance
from django.conf import settings

class Command(BaseCommand):
	def handle(self, *args, **options):
		api_instance, created = PopitApiInstance.objects.get_or_create(url=settings.POPIT_API_URL)
		Candidato.fetch_all_from_api(instance=api_instance)