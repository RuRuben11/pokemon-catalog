import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests
import pandas as pd
import numpy as np
import math
import io
from io import BytesIO
from colour import Color
from scipy import stats

exec(open('code/load.py').read())

#Extract and edit data from PokeAPI
pokemon_url = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon.csv'
pokemon_species_url = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon_species.csv'
pokemon_types_url = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon_types.csv'
pokemon_species_names_url = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon_species_names.csv'
pokemon_forms_url = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon_forms.csv'
pokemon_evolutions_url = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon_evolution.csv'
pokemon_stats_url = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon_stats.csv'
move_names_url = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/move_names.csv'

pokemon = pd.read_csv(pokemon_url)
pokemon_species = pd.read_csv(pokemon_species_url)
pokemon_types = pd.read_csv(pokemon_types_url)
pokemon_species_names = pd.read_csv(pokemon_species_names_url)
pokemon_forms = pd.read_csv(pokemon_forms_url)
pokemon_evolutions  = pd.read_csv(pokemon_evolutions_url)
pokemon_stats = pd.read_csv(pokemon_stats_url)
move_names = pd.read_csv(move_names_url)

pokemon_species_names_esp = pokemon_species_names[pokemon_species_names["local_language_id"] == 7]
move_names_esp = move_names[move_names["local_language_id"] == 7]
pokemon_species_names_esp["genus2"] = pokemon_species_names_esp["genus"].str.replace("Pokémon ", "").values

pokemon_forms.loc[pokemon_forms["form_identifier"] == "mega-x", "form_identifier"] = "mega"
pokemon_forms.loc[pokemon_forms["form_identifier"] == "mega-y", "form_identifier"] = "mega"
pokemon_forms.loc[pokemon_forms["form_identifier"] == "eternamax", "form_identifier"] = "gmax"

#Define fonts
font_name = ImageFont.truetype("resources/fonts/Flexo-Medium.ttf", 32)
font_desc = ImageFont.truetype("resources/fonts/Flexo-Medium.ttf", 20)
font_num = ImageFont.truetype("resources/fonts/Meslo_LG_S_Regular_400.ttf", 36)
font_data = ImageFont.truetype("resources/fonts/Flexo-Medium.ttf", 18)
font_data2 = ImageFont.truetype("resources/fonts/Flexo-Bold.ttf", 18)


#Generate individual figures for default Pokemons

for pkmn in range(1,899):
    im = plotPokemonCard(pkmn)
    im.save('results/pokemon/pokemon_'+str(pkmn)+'.png')


#Evo chains

for chain in range(12,14):
    image = plotEvoLine(chain)
    image.save("results/evolutions/evochain_"+str(chain)+".png")
    print(chain)

