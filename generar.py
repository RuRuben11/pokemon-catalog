import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests
import pandas as pd
import numpy as np
import io
from io import BytesIO



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

#Generate individual figures for default Pokemons

for mon in range(1,10):
    pkmn = generate_pokemon(mon)
    pkmn.save("figures/pokemon_"+str(pokemon_id)+".png")


#Evo chains

for chain in range(27,100):
    test = pokemon_species[pokemon_species["evolution_chain_id"] == chain]
    #Pokemons in the evolutionay chain
    nrow_evo = test.evolves_from_species_id.value_counts().max()
    ncol_evo = len(test)
    matrix = np.zeros((nrow_evo,ncol_evo))
    matrix[:,0] = test[test["evolves_from_species_id"].isna()].id.values[0]
    all_evos = test["id"].values
    x,y =0,0
    if len(matrix[0]) > 1:
        for x in range(len(matrix)):
            y=0
            while matrix[x,y] in test.evolves_from_species_id.values:
                present_evos = test[test["evolves_from_species_id"] == matrix[x:,y][0]].id.values
                matrix[x,y+1] = np.array(list(set(present_evos) & set(all_evos)))[0]
                if len(test[test["evolves_from_species_id"] == present_evos[0]]) <= 1:        
                    all_evos = all_evos[all_evos != matrix[x,y+1]]
                y+=1



    matrix = matrix.astype(int)
    evo_matrix = matrix.tolist()
    for x in range(len(evo_matrix)):
        evo_matrix[x] = [i for i in evo_matrix[x] if i != 0]
    #Images of the pokemons
    evo_image = [[] for _ in range(nrow_evo)]
    x,y =0,0
    for x in range(nrow_evo):
        y=0
        for a in evo_matrix[x]:
            evo_image[x].append(Image.open('figures/pokemon_'+str(int(a))+'.png'))
            y+=1

    #Mechanism of evolution
    if ncol_evo > 1:
        evo_mech = [[] for _ in range(nrow_evo)]
        for x in range(nrow_evo):
            y=0
            for a in evo_matrix[x][:(len(evo_matrix[0])-1)]:
                evo_mech[x].append(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == matrix[x,y+1]].evolution_trigger_id.values[0])
                y+=1

    evo_text, evo_object= evolution_data(evo_matrix, evo_mech)
    if ncol_evo > 1:
        evo_append = [[] for _ in range(nrow_evo)]
        for x in range(nrow_evo):
            y=0
            for a in evo_mech[x]:
                if pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].gender_id.values[0] == 1:
                    evo_append[x].append(ImageLocal('resources/other/female.png',25,25))
                elif pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].gender_id.values[0] == 2:
                    evo_append[x].append(ImageLocal('resources/other/male.png',25,25))
                elif pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].time_of_day.values[0] == 'night':
                    evo_append[x].append(ImageLocal('resources/other/moon.png',25,25))
                elif pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].time_of_day.values[0] == 'day':
                    evo_append[x].append(ImageLocal('resources/other/sun.png',25,25))
                elif pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].needs_overworld_rain.values[0] == 1:
                    evo_append[x].append(ImageLocal('resources/other/rain.png',25,25))
                else:
                    evo_append[x].append(Image.new('RGBA', (25,25)))
                y+=1

    a = plot_EvoLine(evo_matrix, evo_image, evo_text, evo_append)
    a.save("figures/evolutions/evochain_"+str(chain)+".png")



img =ImageURL("https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/"+str(mon)+".png",400,400)
n_types=len(pokemon_types[pokemon_types["pokemon_id"] == mon])
type1_pkmn=pokemon_types[(pokemon_types["slot"] == 1) & (pokemon_types["pokemon_id"] == mon)].type_id.values.astype(int)[0]
img2=ImageURL(types[type1_pkmn]['sprite'],100,22)

if n_types == 2:
    type2_pkmn=pokemon_types[(pokemon_types["slot"] == 2) & (pokemon_types["pokemon_id"] == mon)].type_id.values.astype(int)[0]
    img3=ImageURL(types[type2_pkmn]['sprite'],100,22)

with Image.new('RGBA', (400, 630)) as im:
    im.paste(img, (0, 100))
    if n_types == 1:
        im.paste(img2,(150,500))
    else:
        im.paste(img2,(95,500))
        im.paste(img3,(205,500))
    draw = ImageDraw.Draw(im)
    draw.rounded_rectangle((60, 10, 360, 62), fill="white", outline="black",width=4, radius=70)
    draw.rounded_rectangle((60, 58, 360, 100), fill="grey", outline="black",width=4, radius=70)
    draw.rectangle((40, 535, 360, 565), fill=types[type1_pkmn]['color_light'])
    draw.rectangle((40, 560, 360, 624), fill=types[type1_pkmn]['color_light'])
    draw.line(((40,567),(360,567)), fill =types[type1_pkmn]['color_dark'], width = 4)
    draw.ellipse((35, 10, 125, 100), fill = types[type1_pkmn]['color'], outline ='black',width=4)
    draw.text((135,21), pokemon_species[(pokemon_species["id"] == mon)].identifier.values.astype(str)[0].capitalize(), fill = "black", font = font_name)
    draw.text((135,70), pokemon_desc_esp[(pokemon_desc_esp["pokemon_species_id"] == mon)].genus.values.astype(str)[0], fill = "white", font = font_desc)
    draw.text((48,33), str(mon).zfill(3), fill = "white", font = font_num)
    alt = str(round(pokemon[(pokemon["id"] == mon)].height.values[0]*0.1,1))+' m'
    w, h = draw.textsize(alt, font = font_data2)
    draw.text((113-(w/2)+28,543), alt, fill = "black", font = font_data2)
    draw.text((113-(w/2)-28,543), "Altura:", fill = "black", font = font_data)
    peso = str(round(pokemon[(pokemon["id"] == mon)].weight.values[0]*0.1,1))+' kg'
    w, h = draw.textsize(peso, font = font_data2)
    draw.text((283-(w/2)+24,543), peso, fill = "black", font = font_data2)
    draw.text((283-(w/2)-24,543), "Peso:", fill = "black", font = font_data)
    draw.text((60,575), "Vel:", fill = "black", font = font_data)
    draw.text((100,575), str(pokemon_stats[(pokemon_stats["pokemon_id"]==mon) & (pokemon_stats["stat_id"]==6)].base_stat.values[0]), fill = "black", font = font_data2)
    draw.text((60,602), "PS:", fill = "black", font = font_data)
    draw.text((100,602), str(pokemon_stats[(pokemon_stats["pokemon_id"]==mon) & (pokemon_stats["stat_id"]==1)].base_stat.values[0]), fill = "black", font = font_data2)
    draw.text((155,575), "At:", fill = "black", font = font_data)
    draw.text((188,575), str(pokemon_stats[(pokemon_stats["pokemon_id"]==mon) & (pokemon_stats["stat_id"]==2)].base_stat.values[0]), fill = "black", font = font_data2)
    draw.text((155,602), "Df:", fill = "black", font = font_data)
    draw.text((188,602), str(pokemon_stats[(pokemon_stats["pokemon_id"]==mon) & (pokemon_stats["stat_id"]==3)].base_stat.values[0]), fill = "black", font = font_data2)
    draw.text((240,575), "At Esp:", fill = "black", font = font_data)
    draw.text((306,575), str(pokemon_stats[(pokemon_stats["pokemon_id"]==mon) & (pokemon_stats["stat_id"]==4)].base_stat.values[0]), fill = "black", font = font_data2)
    draw.text((240,602), "Df Esp:", fill = "black", font = font_data)
    draw.text((306,602), str(pokemon_stats[(pokemon_stats["pokemon_id"]==mon) & (pokemon_stats["stat_id"]==5)].base_stat.values[0]), fill = "black", font = font_data2)


    if 'mega' in pokemon_forms[pokemon_forms["pokemon_id"].isin(pokemon[pokemon["species_id"] == mon].id.values)].form_identifier.values:
        img4=ImageURL('https://archives.bulbagarden.net/media/upload/b/bb/Tretta_Mega_Evolution_icon.png',30,30)
        im.paste(img4,(320,85), img4)
    
    if 'gmax' in pokemon_forms[pokemon_forms["pokemon_id"].isin(pokemon[pokemon["species_id"] == mon].id.values)].form_identifier.values:
        img4=ImageURL('https://archives.bulbagarden.net/media/upload/9/9f/Dynamax_icon.png',30,23)
        im.paste(img4,(285,89), img4)


im.save("out2.png")

pokemon_stats[pokemon_stats["pokemon_id"] == mon]
#Paste icon if mega or gmax form
