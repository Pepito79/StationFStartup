import pydantic_ai
from dotenv import load_dotenv
from typing import List ,Dict
import pydantic import BaseModel, Field
from pydantic_ai.models.gemini import GeminiModel
import json
import requests
import os
from pydantic_ai import Agent
from bs4 import BeautifulSoup



load_dotenv()
api=os.getenv('SCRAPPER_API_KEY')
modele='gemini-1.5-flash'


class Resume(BaseModel):
    objectif : str = Field(..., description = "Résume ce que fait cette startup")
    pb : str = Field(..., description ="Quel est le problème que résoud cette startup")
    public : str = Field(..., description = "Quel est le public visé et la taille de ce marché")
    concurrence : str = Field(..., description = "Analyse complète de la concurrence")

class Resultat_Web(BaseModel):
    Resultat: List[Resume] = Field(...,description="Fait un récapitulatif complet et succint qui va droit au but de chaque startup")

@web_agent.tool_plain
def extraireLiens(html : str)