# -*- coding: utf-8 -*-

from django.test import TestCase
from elecciones.models import Eleccion, Candidato
from elecciones.management.commands.candideit_importer import *
from elecciones.management.commands import candideit_importer
import json
from ludibrio import Stub
import slumber
from slumber import Resource
import encodings.idna
from ludibrio.matcher import *


class CandideitLoaderTestCase(TestCase):
    def setUp(self):
        response_json = open("elecciones/tests/sample_data/candideit_api_response.json")
        fiera_candidate_json = open("elecciones/tests/sample_data/fiera_candidate.json")
        fiera_sin_links_json = open("elecciones/tests/sample_data/fiera_sin_links.json")
        fiera_sin_twitter_json = open("elecciones/tests/sample_data/fiera_con_un_link_pero_sin_twitter.json")
        self.parsed_elections = json.load(response_json)
        self.parsed_fiera = json.load(fiera_candidate_json)
        self.fiera_sin_links = json.load(fiera_sin_links_json)
        self.fiera_sin_twitter = json.load(fiera_sin_twitter_json)
        self.username = "fiera"
        self.api_key = "keyfiera"
        self.syncronizer = Syncronizer(self.username, self.api_key)
        with Stub() as api:
            api.election.get(username=self.username, api_key=self.api_key,offset=0) >> self.parsed_elections
            api.candidate(176).get(username=self.username, api_key=self.api_key) >> self.parsed_fiera


        #Here is where I mock the api
        self.syncronizer.api = api




    def test_syncronize_elections(self):
        
        self.syncronizer.sync_elections()

        #Now there should be an election

        elections = Eleccion.objects.all()

        self.assertEquals(elections.count(), 1)
        self.assertEquals(elections[0].nombre, u"asdasdfggggggggga")
        self.assertEquals(elections[0].slug, u"asdasdfggggggggga")
        self.assertEquals(elections[0].main_embedded, u"http://example.com/lfalvarez/asdasdfgggggggggggga/embeded")

    def test_it_does_not_create_two_elections_with_the_same_name(self):
        self.syncronizer.sync_elections()
        self.syncronizer.sync_elections()

        self.assertEquals(Eleccion.objects.count(), 1)        


    def test_syncronize_candidates(self):
        election = Eleccion.objects.create(nombre="laeleccion")
        self.syncronizer.sync_candidates(election, self.parsed_elections["objects"][0]["candidates"])

        self.assertEquals(Candidato.objects.filter(eleccion=election).count(), 2)
        self.assertEquals(Candidato.objects.get(nombre=u"cand 1").eleccion, election)
        self.assertEquals(Candidato.objects.get(nombre=u"cand 2").eleccion, election)

    def test_it_loads_candidate_twitter(self):
        election = Eleccion.objects.create(nombre="laeleccion")
        candidate = Candidato.objects.create(nombre="Fiera", eleccion=election)
        self.syncronizer.sync_twitter(candidate, self.parsed_elections["objects"][0]["candidates"][0]["id"])
        fiera = Candidato.objects.get(nombre="Fiera")
        self.assertEquals(fiera.twitter, "Fiera")

    def test_it_matches_twitter(self):
        self.assertEquals(self.syncronizer._matcher("http://twitter.com/Fiera"), "Fiera")
        self.assertEquals(self.syncronizer._matcher("https://twitter.com/Fiera"), "Fiera")
        self.assertEquals(self.syncronizer._matcher("http://www.twitter.com/Fiera"), "Fiera")
        self.assertEquals(self.syncronizer._matcher("https://twitter.com/Fiera"), "Fiera")
        self.assertEquals(self.syncronizer._matcher("http://twitter.com/#!/Fiera"), "Fiera")
        self.assertEquals(self.syncronizer._matcher("http://twitter.com/#!/Fiera/"), "Fiera")

    



    def test_it_does_not_have_problems_with_other_links(self):
        with Stub() as api:
            api.candidate(178).get(username=self.username, api_key=self.api_key) >> self.fiera_sin_twitter

        self.syncronizer.api = api
        election = Eleccion.objects.create(nombre="laeleccion")
        candidate = Candidato.objects.create(nombre="Fiera", eleccion=election)
        self.syncronizer.sync_twitter(candidate, 178)
        fiera = Candidato.objects.get(nombre="Fiera")
        self.assertTrue(fiera.twitter is None)




    def test_it_does_not_create_twice_a_candidate(self):
        election = Eleccion.objects.create(nombre="laeleccion")
        self.syncronizer.sync_candidates(election, self.parsed_elections["objects"][0]["candidates"])
        self.syncronizer.sync_candidates(election, self.parsed_elections["objects"][0]["candidates"])

        self.assertEquals(Candidato.objects.filter(eleccion=election).count(), 2)


    def test_syncronize_both(self):
        self.syncronizer.sync_elections()

        self.assertEquals(Candidato.objects.all().count(), 2)
        self.assertEquals(Candidato.objects.filter(nombre=u"cand 1").count(), 1)
        self.assertEquals(Candidato.objects.filter(nombre=u"cand 2").count(), 1)

    def test_it_gets_twitters_when_syncronizing_everything(self):
        self.syncronizer.sync_elections()

        fieri = Candidato.objects.get(nombre=u"cand 1")

        self.assertEquals(fieri.twitter, "Fiera")

    def test_it_loads_several_pages(self):
        response_json_1 = open("elecciones/tests/sample_data/big_json_1.json")
        response_json_2 = open("elecciones/tests/sample_data/big_json_2.json")
        parsed_elections_1 = json.load(response_json_1)
        parsed_elections_2 = json.load(response_json_2)
        username = "fiera"
        api_key = "keyfiera"
        syncronizer = Syncronizer(username, api_key)
        with Stub() as api:
            api.election.get(username=self.username, api_key=self.api_key,offset=0) >> parsed_elections_1
            api.election.get(username=self.username, api_key=self.api_key,offset=20) >> parsed_elections_2
            api.candidate(kind_of(int)).get(username=self.username, api_key=self.api_key) >> self.parsed_fiera

        #Here is where I mock the api
        syncronizer.api = api

        syncronizer.sync_elections()
        self.assertEquals(Eleccion.objects.count(), 26)




        
