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



#Extract and edit data from PokeAPI
pokemon_url = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon.csv'
pokemon_species_url = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon_species.csv'
pokemon_types_url = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon_types.csv'
pokemon_desc_url = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon_species_names.csv'
pokemon_forms_url = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon_forms.csv'
pokemon_evolutions_url = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon_evolution.csv'
pokemon_stats_url = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon_stats.csv'
move_names_url = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/move_names.csv'

pokemon = pd.read_csv(pokemon_url)
pokemon_species = pd.read_csv(pokemon_species_url)
pokemon_types = pd.read_csv(pokemon_types_url)
pokemon_desc = pd.read_csv(pokemon_desc_url)
pokemon_forms = pd.read_csv(pokemon_forms_url)
pokemon_evolutions  = pd.read_csv(pokemon_evolutions_url)
pokemon_stats = pd.read_csv(pokemon_stats_url)
move_names = pd.read_csv(move_names_url)

pokemon_desc_esp = pokemon_desc[pokemon_desc["local_language_id"] == 7]
move_names_esp = move_names[move_names["local_language_id"] == 7]
pokemon_desc_esp["genus"] = pokemon_desc_esp["genus"].str.replace("Pokémon ", "").values

pokemon_forms.loc[pokemon_forms["form_identifier"] == "mega-x", "form_identifier"] = "mega"
pokemon_forms.loc[pokemon_forms["form_identifier"] == "mega-y", "form_identifier"] = "mega"
pokemon_forms.loc[pokemon_forms["form_identifier"] == "eternamax", "form_identifier"] = "gmax"

#Define fonts
font_name = ImageFont.truetype("resources/fonts/Flexo-Medium.ttf", 32)
font_desc = ImageFont.truetype("resources/fonts/Flexo-Medium.ttf", 20)
font_num = ImageFont.truetype("resources/fonts/Meslo_LG_S_Regular_400.ttf", 36)
font_data = ImageFont.truetype("resources/fonts/Flexo-Medium.ttf", 18)
font_data2 = ImageFont.truetype("resources/fonts/Flexo-Bold.ttf", 18)



exec(open('code/load.py').read())


#Generate individual figures for default Pokemons

for pokemon_id in range(1,10):
    pkmn = generate_pokemon(pokemon_id)
    pkmn.save("figures/pokemon_"+str(pokemon_id)+".png")


#Evo chains

for chain in range(449,476):
    image = plotEvoLine(chain)
    image.save("figures/evolutions/evochain_"+str(chain)+".png")
    print(chain)


pokemon_species[pokemon_species["evolution_chain_id"] == chain]


evo_matrix = generateEvoMatrix(chain)
evo_image = generateEvoImages(evo_matrix)
evo_mech = generateEvoMechanism(evo_matrix)
evo_text, evo_object= generateEvoData(evo_matrix, evo_mech)
evo_append = generateEvoData2(evo_matrix, evo_mech)
image = generateEvoPlot(evo_matrix, evo_image, evo_text, evo_object, evo_append)


############# WIP ##################

array_ps=pokemon_stats[pokemon_stats['stat_id']==1].base_stat
array_at=pokemon_stats[pokemon_stats['stat_id']==2].base_stat
array_de=pokemon_stats[pokemon_stats['stat_id']==3].base_stat
array_as=pokemon_stats[pokemon_stats['stat_id']==4].base_stat
array_ds=pokemon_stats[pokemon_stats['stat_id']==5].base_stat
array_ve=pokemon_stats[pokemon_stats['stat_id']==6].base_stat

round(stats.percentileofscore(array_ps, ps),0)



exec(open('code/load.py').read())

for pkmn in range(1,899):
    im = plotPokemonCard(pkmn)
    im.save('results/pokemon/pokemon_'+str(pkmn)+'.png')

