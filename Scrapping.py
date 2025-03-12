#!/usr/bin/env python3
from bs4 import BeautifulSoup
import json
import os
import pydantic_ai
from pydantic_ai import Agent
from pydantic import BaseModel,Field
from typing import Dict, List, Optional
import requests
from markdownify import markdownify as md
from googlesearch import search
from dotenv import load_dotenv
import time
import ListeStartup


load_dotenv()
api=os.getenv('GOOGLE_GEMINI_KEY')
gemini='gemini-1.5-flash'

listeStartup = ListeStartup.liste  

"""Trouver le site de chaque stratup pour donner le contenu au llm"""

# Ouvrir le fichier pour écrire les liens
with open("liste_links.txt", "a") as file:
    for startup in listeStartup:
        q = search(startup, num_results=1)  # Effectuer une recherche avec le nom de la startup
        i = 0
        for lien in q:
            file.write(lien + "\n") 
            print(f"Lien n°{i} écrit")
            i += 1

print("Les liens ont été écrits dans le fichier liste_links.txt")

"""Creation des classes demandées à l'agent IA"""
class ResultatParLien(BaseModel):
    Objectif: str = Field(..., description="Résume l'objectif de la startup")
    Probleme: str = Field(...,description="Identifie le problème auquel la startup répond")
    Secteur : str = Field(...,description="Quelle est le secteur visé par la startup")

class ResulatFinal(BaseModel):
    Resultat: List[ResultatParLien] = Field(...,"Le resultat final qui est le ResultatParLien de chaque lien")
    
webAgent = Agent(
    gemini,
    result_type= ResulatFinal,
    system_prompt=(
    'effecte une recherche pour chaque startup présent dans la liste qui va t être ','donnée par l utilisateur.' , 'Il faudra que tu utilises l outil {WebSearcher}' ,
    'pour chaque stratup ')
)

@WebSearcher.tool_plain
def RechercheStartup( nom_startup : str):
    for j in search(nom_startup, num=1):
        