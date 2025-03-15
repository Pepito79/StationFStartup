#!/usr/bin/env python3
from bs4 import BeautifulSoup, Comment
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
import re
import listeLiens


load_dotenv()
api=os.getenv('GOOGLE_GEMINI_KEY')
gemini='gemini-1.5-flash'


"""Creation des classes demandées à l'agent IA"""
class ResultatParLien(BaseModel):
    Nom: str = Field(..., description="Nom de la startup")
    Objectif: str = Field(..., description="Description détaillée en français de la mission et de la valeur ajoutée de la startup , il faut au moins 5 lignes claires et précises.")
    Probleme: str = Field(..., description="Problème traité en français, son importance et ses conséquences sur le marché")
    Secteur: str = Field(..., description="Secteur d'activité de la startup")
class ResulatFinal(BaseModel):
    Resultat: List[ResultatParLien] = Field(...,description="Le resultat final qui est le ResultatParLien de chaque lien")
    
webAgent = Agent(
    gemini,
    result_type= ResulatFinal,
    system_prompt = (
    "Analyse lien par lien (il faut parcourir tous les liens dans la liste {listeLiens.listeLiens}}) dans la liste ournie par l'utilisateur. Pour chaque lien dans la liste qui correspondant à une startup, "
    "utilise l'outil {webAgent} afin de comprendre son objectif, son domaine d'activité et sa mission, le tout en français.","Tu traiteras tous les liens de la liste et impérativement ." ,
    "Si tu ne comprend pas la première fois un lien tu devra reanalysé le contenu qui te sera retourné par l'outil {visite_lien} jusqu'à ce que tu comprennes."
)
)


@webAgent.tool_plain
def visiter_lien(lien: str):
    """Un lien est donné en arg le but est de scrappe les données du lien et en extraire le texte """
    response = requests.get(lien)
    soup= BeautifulSoup(response.text,'html.parser')
    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()
    final= soup.prettify()
    return md(final)

def main():
    resultat= webAgent.run_sync(f"{listeLiens.listeLiens}").data
    res_dict=resultat.model_dump()
    with open("Description","a") as file:
        for i, dico in enumerate(res_dict['Resultat']):
            file.write(f"### 🚀 Startup {i}: {dico["Nom"]} \n\n")
            file.write(f"Objectif de la startup: \n {dico['Objectif']}\n\n")
            file.write(f"**📌 Problème:** \n {dico['Probleme']}\n\n")
            file.write(f"**🏢 Secteur:** \n {dico['Secteur']}\n\n")
            print(f" Stratup n°{i} analysée")

if __name__ == "__main__":
    main()