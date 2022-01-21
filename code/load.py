#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
from colour import Color
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import urllib.request
import requests
import pandas as pd
import numpy as np
import math
import io
import random
import statistics

#Extract and edit data from PokeAPI
pokemon_url = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon.csv'
pokemon_species_url = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon_species.csv'
pokemon_types_url = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon_types.csv'
pokemon_species_names_url = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon_species_names.csv'
pokemon_forms_url = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon_forms.csv'
pokemon_evolutions_url = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon_evolution.csv'
pokemon_stats_url = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon_stats.csv'
move_names_url = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/move_names.csv'
pokemon_form_names_url='https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon_form_names.csv'

pokemon = pd.read_csv(pokemon_url)
pokemon_species = pd.read_csv(pokemon_species_url)
pokemon_types = pd.read_csv(pokemon_types_url)
pokemon_species_names = pd.read_csv(pokemon_species_names_url)
pokemon_forms = pd.read_csv(pokemon_forms_url)
pokemon_evolutions = pd.read_csv(pokemon_evolutions_url)
pokemon_stats = pd.read_csv(pokemon_stats_url)
move_names = pd.read_csv(move_names_url)
pokemon_form_names = pd.read_csv(pokemon_form_names_url)

pokemon_regional = pd.read_csv('pokemon_regionals.csv')
evolution_regional = pd.read_csv('evolution_regionals.csv')

pokemon_species = pokemon_species.append(pd.DataFrame(data=pokemon_regional))
pokemon_evolutions = pokemon_evolutions.append(pd.DataFrame(data=evolution_regional))

pokemon_species.evolves_from_species_id[pokemon_species.identifier == 'perrserker'] = 10158.0
pokemon_species.evolves_from_species_id[pokemon_species.identifier == 'sirfetchd'] = 10163.0
pokemon_species.evolves_from_species_id[pokemon_species.identifier == 'mr-rime'] = 10165.0
pokemon_species.evolves_from_species_id[pokemon_species.identifier == 'cursola'] = 10170.0
pokemon_species.evolves_from_species_id[pokemon_species.identifier == 'obstagoon'] = 10172.0
pokemon_species.evolves_from_species_id[pokemon_species.identifier == 'runerigus'] = 10176.0

pokemon_species_names_esp = pokemon_species_names[pokemon_species_names["local_language_id"] == 7]
move_names_esp = move_names[move_names["local_language_id"] == 7]
pokemon_form_names_esp = pokemon_form_names[pokemon_form_names["local_language_id"] == 7]
pokemon_species_names_esp["genus2"] = pokemon_species_names_esp["genus"].str.replace("Pokémon ", "").values
pokemon_species_names_esp['name'] = pokemon_species_names_esp['name'].replace({'\u2640':''}, regex=True)
pokemon_species_names_esp['name'] = pokemon_species_names_esp['name'].replace({'\u2642':''}, regex=True)

pokemon_forms.loc[pokemon_forms["form_identifier"] == "mega-x", "form_identifier"] = "mega"
pokemon_forms.loc[pokemon_forms["form_identifier"] == "mega-y", "form_identifier"] = "mega"
pokemon_forms.loc[pokemon_forms["form_identifier"] == "eternamax", "form_identifier"] = "gmax"

#Define fonts
font_name = ImageFont.truetype("resources/fonts/Flexo-Medium.ttf", 32)
font_desc = ImageFont.truetype("resources/fonts/Flexo-Medium.ttf", 20)
font_num = ImageFont.truetype("resources/fonts/Meslo_LG_S_Regular_400.ttf", 36)
font_data = ImageFont.truetype("resources/fonts/Flexo-Medium.ttf", 18)
font_data2 = ImageFont.truetype("resources/fonts/Flexo-Bold.ttf", 18)



#Functions

def all_same(items):
    return all(x == items[0] for x in items)

def ImageURL(url, size_x, size_y):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    newsize=(size_x,size_y)
    return img.resize(newsize)

def ImageLocal(directory, size_x, size_y):
    img = Image.open(directory)
    newsize=(size_x,size_y)
    return img.resize(newsize)

def find_max_list(list):
    list_len = [len(i) for i in list]
    return max(list_len)

def expand_list(l, n):
    l.extend([0] * (n - len(l)))
    l = l[:n]
    return l

def plotPokemonCard(mon, form = 'default',output=''):
    id_mon = mon
    if form != 'default':
        mon=pokemon[(pokemon['species_id']==mon) & pokemon['identifier'].str.contains(form)].id.values[0]
        form_mon = pokemon_forms[pokemon_forms["pokemon_id"] == mon].id.values[0]
    else:
        form_mon = mon
    
    img =ImageURL("https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/"+str(mon)+".png",400,400)
    n_types=len(pokemon_types[pokemon_types["pokemon_id"] == mon])
    type1_pkmn=pokemon_types[(pokemon_types["slot"] == 1) & (pokemon_types["pokemon_id"] == mon)].type_id.values.astype(int)[0]
    img2=ImageURL(types[type1_pkmn]['sprite'],100,22)

    color=Color(types[type1_pkmn]['color_light'])
    colors = list(color.range_to(Color(types[type1_pkmn]['color_dark']),101))

    array_ps=pokemon_stats[pokemon_stats['stat_id']==1].base_stat
    array_at=pokemon_stats[pokemon_stats['stat_id']==2].base_stat
    array_de=pokemon_stats[pokemon_stats['stat_id']==3].base_stat
    array_as=pokemon_stats[pokemon_stats['stat_id']==4].base_stat
    array_ds=pokemon_stats[pokemon_stats['stat_id']==5].base_stat
    array_ve=pokemon_stats[pokemon_stats['stat_id']==6].base_stat


    if n_types == 2:
        type2_pkmn=pokemon_types[(pokemon_types["slot"] == 2) & (pokemon_types["pokemon_id"] == mon)].type_id.values.astype(int)[0]
        img3=ImageURL(types[type2_pkmn]['sprite'],100,22)


    with Image.new('RGBA', (400, 637)) as im:
        im.paste(img, (0, 100))
        
        if n_types == 1:
            im.paste(img2,(150,500))
        else:
            im.paste(img2,(95,500))
            im.paste(img3,(205,500))
        
        draw = ImageDraw.Draw(im)
        draw.rounded_rectangle((60, 10, 360, 62), fill="white", outline="black",width=4, radius=70)
        draw.rounded_rectangle((60, 58, 360, 100), fill="grey", outline="black",width=4, radius=70)
        draw.rectangle((38, 535, 362, 565), fill=types[type1_pkmn]['color_light'])
        draw.line(((38,565),(362,565)), fill =types[type1_pkmn]['color_dark'], width = 4)
        draw.ellipse((35, 10, 125, 100), fill = types[type1_pkmn]['color'], outline ='black',width=4)
        draw.text((135,21), pokemon_species_names_esp[(pokemon_species_names_esp["pokemon_species_id"] == id_mon)].name.values.astype(str)[0].astype('U'), fill = "black", font = font_name)
        if form == 'default':
            draw.text((135,70), pokemon_species_names_esp[(pokemon_species_names_esp["pokemon_species_id"] == id_mon)].genus2.values.astype(str)[0].astype('U'), fill = "white", font = font_desc)
        else:
            if form != 'galar':
                draw.text((135,70), pokemon_form_names_esp[(pokemon_form_names_esp["pokemon_form_id"] == form_mon)].form_name.values.astype(str)[0].astype('U'), fill = "white", font = font_desc)
            else:
                draw.text((135,70), 'Forma de Galar', fill = "white", font = font_desc)
        draw.text((48,33), str(id_mon).zfill(3), fill = "white", font = font_num)
        
        alt = str(round(pokemon[(pokemon["id"] == mon)].height.values[0]*0.1,1))+' m'
        w, h = draw.textsize(alt, font = font_data2)
        draw.text((113-(w/2)+28,542), alt, fill = "black", font = font_data2)
        draw.text((113-(w/2)-28,542), "Altura:", fill = "black", font = font_data)
        
        peso = str(round(pokemon[(pokemon["id"] == mon)].weight.values[0]*0.1,1))+' kg'
        w, h = draw.textsize(peso, font = font_data2)
        draw.text((283-(w/2)+24,542), peso, fill = "black", font = font_data2)
        draw.text((283-(w/2)-24,542), "Peso:", fill = "black", font = font_data)
        
        draw.line(((38,565),(362,565)), fill =types[type1_pkmn]['color_dark'], width = 4)
        
        vel=pokemon_stats[(pokemon_stats["pokemon_id"]==mon) & (pokemon_stats["stat_id"]==6)].base_stat.values[0]
        draw.rectangle((38, 567, 146, 597), fill=str(colors[int(round(stats.percentileofscore(array_ve, vel),0))]))
        draw.text((38+8,574), "VE:", fill = "black", font = font_data)
        w, h = draw.textsize(str(vel), font = font_data2)
        draw.text(((146+73)/2-(w/2),574), str(vel), fill = "black", font = font_data2)
        
        ps=pokemon_stats[(pokemon_stats["pokemon_id"]==mon) & (pokemon_stats["stat_id"]==1)].base_stat.values[0]
        draw.rectangle((38, 597, 146, 627), fill=str(colors[int(round(stats.percentileofscore(array_ps, ps),0))]))
        draw.text((38+8,604), "PS:", fill = "black", font = font_data)
        w, h = draw.textsize(str(ps), font = font_data2)        
        draw.text(((146+73)/2-(w/2),604), str(ps), fill = "black", font = font_data2)
        
        att=pokemon_stats[(pokemon_stats["pokemon_id"]==mon) & (pokemon_stats["stat_id"]==2)].base_stat.values[0]
        draw.rectangle((146, 567, 254, 597), fill=str(colors[int(round(stats.percentileofscore(array_at, att),0))]))
        draw.text((146+8,574), "AT:", fill = "black", font = font_data)
        w, h = draw.textsize(str(att), font = font_data2)
        draw.text(((254+181)/2-(w/2),574), str(att), fill = "black", font = font_data2)
        
        defe=pokemon_stats[(pokemon_stats["pokemon_id"]==mon) & (pokemon_stats["stat_id"]==3)].base_stat.values[0]
        draw.rectangle((146, 597, 254, 627), fill=str(colors[int(round(stats.percentileofscore(array_de, defe),0))]))
        draw.text((146+8,604), "DF:", fill = "black", font = font_data)
        w, h = draw.textsize(str(defe), font = font_data2)
        draw.text(((254+181)/2-(w/2),604), str(defe), fill = "black", font = font_data2)
        
        satt=pokemon_stats[(pokemon_stats["pokemon_id"]==mon) & (pokemon_stats["stat_id"]==4)].base_stat.values[0]
        draw.rectangle((254, 567, 362, 597), fill=str(colors[int(round(stats.percentileofscore(array_as, satt),0))]))
        draw.text((254+8,574), "AS:", fill = "black", font = font_data)
        w, h = draw.textsize(str(satt), font = font_data2)
        draw.text(((362+289)/2-(w/2),574), str(satt), fill = "black", font = font_data2)
        
        sdef=pokemon_stats[(pokemon_stats["pokemon_id"]==mon) & (pokemon_stats["stat_id"]==5)].base_stat.values[0]        
        draw.rectangle((254, 597, 362, 627), fill=str(colors[int(round(stats.percentileofscore(array_ds, sdef),0))]))        
        draw.text((254+8,604), "DS:", fill = "black", font = font_data)
        w, h = draw.textsize(str(sdef), font = font_data2)
        draw.text(((362+289)/2-(w/2),604), str(sdef), fill = "black", font = font_data2)

        if 'mega' in pokemon_forms[pokemon_forms["pokemon_id"].isin(pokemon[pokemon["species_id"] == mon].id.values)].form_identifier.values:
            img4=ImageURL('https://archives.bulbagarden.net/media/upload/b/bb/Tretta_Mega_Evolution_icon.png',30,30)
            im.paste(img4,(320,85), img4)
        
        if 'gmax' in pokemon_forms[pokemon_forms["pokemon_id"].isin(pokemon[pokemon["species_id"] == mon].id.values)].form_identifier.values:
            img4=ImageURL('https://archives.bulbagarden.net/media/upload/9/9f/Dynamax_icon.png',30,23)
            im.paste(img4,(285,89), img4)
        im.save(output+"pokemon_"+str(mon)+".png")

def generateEvoMatrix(chain):
    test = pokemon_species[pokemon_species["evolution_chain_id"] == chain]

    if math.isnan(test.evolves_from_species_id.value_counts().max()):
        n_max_evo = 1
    else:
        n_max_evo = test.evolves_from_species_id.value_counts().max()

    nrow_evo = n_max_evo * test.evolves_from_species_id.isna().sum()
    ncol_evo = len(test)
    matrix = np.zeros((nrow_evo,ncol_evo))

    if len(test[test["evolves_from_species_id"].isna()].id) == 1:
        matrix[:,0] = test[test["evolves_from_species_id"].isna()].id.values[0]
    else:
        inicial_evos = []
        if np.isnan(test['evolves_from_species_id'].values).all():
            inicial_evos.extend(list(test['id'].values))
        else:
            for i in range(test.evolves_from_species_id.isna().sum()):
                if test[test["evolves_from_species_id"].isna()].id.values[i] in test['evolves_from_species_id'].values:
                    inicial_evos.extend([test[test["evolves_from_species_id"].isna()].id.values[i]] * test['evolves_from_species_id'].value_counts()[test[test["evolves_from_species_id"].isna()].id.values[i]])
                else:
                    inicial_evos.append(test[test["evolves_from_species_id"].isna()].id.values[i])
        for i in range(nrow_evo):
            matrix[i][0] = inicial_evos[i]
    
    all_evos = test["id"].values
    x,y =0,0

    if (len(matrix[0]) > 1) & (not (np.isnan(test['evolves_from_species_id'].values).all())):
        for x in range(len(matrix)):
            y=0
            while matrix[x,y] in test.evolves_from_species_id.values:
                present_evos = test[test["evolves_from_species_id"] == matrix[x:,y][0]].id.values
                matrix[x,y+1] = np.array(list(set(present_evos) & set(all_evos))).min()
                if len(test[test["evolves_from_species_id"] == present_evos[0]]) <= 1:
                    all_evos = all_evos[all_evos != matrix[x,y+1]]
                y+=1

    matrix = matrix.astype(int)
    evo_matrix = matrix.tolist()

    for x in range(len(evo_matrix)):
        evo_matrix[x] = [i for i in evo_matrix[x] if i != 0]

    final_length = find_max_list(evo_matrix)

    for x in range(len(evo_matrix)):
        expand_list(evo_matrix[x], final_length)
    

    return evo_matrix


def generateEvoImages(evo_matrix):
    evo_image = [[] for _ in range(len(evo_matrix))]
    for x in range(len(evo_matrix)):
        y=0
        for a in evo_matrix[x]:
            if a == 0:
                evo_image[x].append(Image.new('RGBA', (500, 675)))
            else:
                evo_image[x].append(Image.open('results/pokemon/pokemon_'+str(int(a))+'.png'))
            y+=1
    return evo_image

def generateEvoMechanism(evo_matrix):
    evo_mech = [[] for _ in range(len(evo_matrix))]
    if len(evo_matrix[0]) > 1:
        for x in range(len(evo_matrix)):
            y=0
            for a in evo_matrix[x][:(len(evo_matrix[0])-1)]:
                if evo_matrix[x][y+1] in pokemon_evolutions["evolved_species_id"].unique():
                    evo_mech[x].append(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].evolution_trigger_id.values[0])
                else:
                    evo_mech[x].append(0)
                y+=1
    return evo_mech


def generateEvoData(evo_matrix, evo_mech):
    evo_text = [[] for _ in range(len(evo_matrix))]
    evo_object = [[] for _ in range(len(evo_matrix))]
    if len(evo_matrix[0]) > 1:
        for x in range(len(evo_matrix)):
            y=0
            for a in evo_mech[x]:
                if a == 1:
                    if np.isfinite(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].minimum_level.values[0]):
                        evo_text[x].append('Nivel '+ str(int(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].minimum_level.values[0])))
                        evo_object[x].append(ImageLocal("resources/items/item_50.png", 44,44))
                    elif np.isfinite(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].minimum_happiness.values[0]):
                        evo_text[x].append('Amistad')
                        evo_object[x].append(ImageLocal("resources/items/item_50.png", 44,44))
                    elif np.isfinite(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].held_item_id.values[0]):
                        evo_text[x].append('Subir nivel')
                        evo_item=str(int(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].held_item_id.values[0]))
                        evo_object[x].append(ImageLocal('resources/items/item_'+ evo_item +'.png', 44,44))
                    elif np.isfinite(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].known_move_id.values[0]):
                        evo_move=int(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].known_move_id.values[0])
                        ataque=move_names_esp[move_names_esp["move_id"]==evo_move].name.values[0]
                        evo_text[x].append(ataque)
                        evo_object[x].append(ImageLocal('resources/items/item_50.png', 44,44))
                    elif np.isfinite(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].known_move_type_id.values[0]):
                        evo_move=int(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].known_move_type_id.values[0])
                        ataque=types[evo_move]['name']
                        evo_text[x].append('MT de '+ataque)
                        evo_object[x].append(ImageLocal('resources/items/item_50.png', 44,44))
                    elif np.isfinite(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].minimum_beauty.values[0]):
                        evo_text[x].append('Belleza')
                        evo_object[x].append(ImageLocal('resources/items/item_50.png', 44,44))
                    elif np.isfinite(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].party_species_id.values[0]):
                        party = pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].party_species_id.values[0]
                        evo_text[x].append('Subir nivel')
                        evo_object[x].append(ImageURL("https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/"+str(int(party))+".png", 44,44))                
                    elif np.isfinite(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].location_id.values[0]):
                        evo_object[x].append(ImageLocal("resources/items/item_50.png", 44,44))
                        if pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].location_id.values[0] in (10,379,629):
                            evo_text[x].append('Campo magn.')
                        elif pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].location_id.values[0] in (8,375,650):
                            evo_text[x].append('Roca musgo')
                        elif pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].location_id.values[0] in (48,380,640,775):
                            evo_text[x].append('Roca hielo')
                    else:
                        evo_text[x].append('Campo magn.')
                        evo_object[x].append(ImageLocal("resources/items/item_50.png", 44,44))
                elif a == 2:
                    evo_text[x].append('Intercambio')
                    if pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].held_item_id.notna().values[0]:
                        evo_item=str(int(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].held_item_id.values[0]))
                        evo_object[x].append(ImageLocal('resources/items/item_'+ evo_item +'.png', 44,44))
                    elif pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].trade_species_id.notna().values[0]:
                        evo_species=str(int(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].trade_species_id.values[0]))
                        evo_object[x].append(ImageURL('https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/'+ evo_species +'.png', 44,44))                     
                    else:
                        evo_object[x].append(ImageURL('https://cdn-icons-png.flaticon.com/512/103/103588.png',44,44))
                elif a == 3:
                    evo_text[x].append('Objeto')
                    if np.isnan(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].trigger_item_id.values[0]):
                        evo_object[x].append(Image.new('RGBA', (44,44)))
                    else:
                        evo_item=str(int(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].trigger_item_id.values[0]))
                        evo_object[x].append(ImageLocal('resources/items/item_'+ evo_item +'.png', 44,44))
                elif a == 4:
                    evo_text[x].append('Espacio')
                    evo_object[x].append(ImageLocal('resources/items/item_4.png', 44,44))
                elif a == 5:
                    if evo_matrix[x][y+1] == 865:
                        evo_text[x].append('3 críticos')
                        evo_object[x].append(ImageLocal('resources/items/item_236.png', 44,44))
                    elif evo_matrix[x][y+1] == 867:
                        evo_text[x].append('-49 PS')
                        evo_object[x].append(ImageLocal('resources/items/item_252.png', 44,44))
                    elif evo_matrix[x][y+1] == 869:
                        evo_text[x].append('Girar')
                        evo_object[x].append(ImageLocal('resources/items/item_1167.png', 44,44))
                    elif evo_matrix[x][y+1] == 892:
                        evo_text[x].append('Torre DLC')
                        evo_object[x].append(ImageURL('https://cdn-icons-png.flaticon.com/512/463/463574.png', 44,44))            
                y+=1
    return evo_text, evo_object

def generateEvoData2(evo_matrix, evo_mech):
    evo_append = [[] for _ in range(len(evo_matrix))]
    if len(evo_matrix[0]) > 1:
        for x in range(len(evo_matrix)):
            y=0
            for a in evo_mech[x]:
                if evo_matrix[x][y+1] in pokemon_evolutions["evolved_species_id"].unique():
                    if pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].gender_id.values[0] == 1:
                        evo_append[x].append(ImageLocal('resources/other/female.png',44,44))
                    elif pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].gender_id.values[0] == 2:
                        evo_append[x].append(ImageLocal('resources/other/male.png',44,44))
                    elif pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].time_of_day.values[0] == 'night':
                        evo_append[x].append(ImageLocal('resources/other/moon.png',44,44))
                    elif pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].time_of_day.values[0] == 'day':
                        evo_append[x].append(ImageLocal('resources/other/sun.png',44,44))
                    elif pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].needs_overworld_rain.values[0] == 1:
                        evo_append[x].append(ImageLocal('resources/other/rain.png',44,44))
                    else:
                        evo_append[x].append(Image.new('RGBA', (44,44)))
                else:
                    evo_append[x].append(Image.new('RGBA', (44,44)))
                y+=1
    return evo_append

def generateEvoPlot(evo_matrix, evo_image, evo_text, evo_object, evo_append):
    evo_type = pokemon_types[(pokemon_types["slot"] == 1) & (pokemon_types["pokemon_id"] == evo_matrix[0][0])].type_id.values[0]
    with Image.new('RGBA', ((550*len(evo_matrix[0]))-150, (675*len(evo_matrix)))) as im:
        draw = ImageDraw.Draw(im)
        for x in range(len(evo_matrix)):
            y = 0
            for a in evo_matrix[x]:
                aa = [item[y] for item in evo_matrix]
                if all_same(aa):
                    im.paste(evo_image[x][y], (0+(550*y), int(675*len(evo_matrix)/2-330)))
                elif len(aa) != len(set(aa)):
                    z = statistics.mean([index for index, element in enumerate(aa) if element == aa[x]])
                    im.paste(evo_image[x][y], (0+(550*y), int(0+(675*z))))
                else:
                    im.paste(evo_image[x][y], (0+(550*y), 0+(675*x)))
                y+=1
        for x in range(len(evo_text)):
            y = 0
            for text in evo_text[x]:
                if all_same([item[y+1] for item in evo_matrix]):
                    draw.rectangle((400+(550*y), 310+int(675*len(evo_matrix)/2-290), 510+(550*y), 340+int(675*len(evo_matrix)/2-290)), fill=types[evo_type]['color_light'])
                    draw.polygon([(550+(550*y),325+int(675*len(evo_matrix)/2-290)), (510+(550*y), 290+int(675*len(evo_matrix)/2-290)), (510+(550*y),360+int(675*len(evo_matrix)/2-290))], fill = types[evo_type]['color_light'])
                    w, h = draw.textsize(text, font = font_data2)
                    draw.text((455-(w/2)+(550*y),317+int(675*len(evo_matrix)/2-290)), text, fill = "black", font = font_desc)                    
                    im.paste(evo_object[x][y], (444+(550*y),255+int(675*len(evo_matrix)/2-290)))
                    im.paste(evo_append[x][y], (444+(550*y), 345+int(675*len(evo_matrix)/2-290)),evo_append[x][y])
                else:
                    draw.rectangle((400+(550*y), 310+(675*x), 510+(550*y), 340+(675*x)), fill=types[evo_type]['color_light'])
                    draw.polygon([(550+(550*y),325+(675*x)), (510+(550*y), 290+(675*x)), (510+(550*y),360+(675*x))], fill = types[evo_type]['color_light'])
                    w, h = draw.textsize(text, font = font_data2)
                    draw.text((455-(w/2)+(550*y),317+(675*x)), text, fill = "black", font = font_desc)
                    im.paste(evo_object[x][y], (444+(550*y),255+(675*x)))
                    im.paste(evo_append[x][y], (444+(550*y), 345+(675*x)),evo_append[x][y])
                y+=1
    return im

def plotEvoLine(chain, output=''):
    evo_matrix = generateEvoMatrix(chain)
    evo_image = generateEvoImages(evo_matrix)
    evo_mech = generateEvoMechanism(evo_matrix)
    evo_text, evo_object= generateEvoData(evo_matrix, evo_mech)
    evo_append = generateEvoData2(evo_matrix, evo_mech)
    image = generateEvoPlot(evo_matrix, evo_image, evo_text, evo_object, evo_append)
    image.save(output+"evochain_"+str(chain)+".png")


def ProfessorOak(n_starters = 3, output = ''):
    starter_forms = list(pokemon_species[(np.isnan(pokemon_species["evolves_from_species_id"])) & (pokemon_species["is_legendary"]==0) & (pokemon_species["is_mythical"]==0)].id.values)
    options = random.sample(starter_forms,n_starters)
    options.sort()
    with Image.new('RGBA', ((550*len(options)-150, 775))) as im:
        draw = ImageDraw.Draw(im)
        for x in range(len(options)):
            im.paste(Image.open('results/pokemon/pokemon_'+str(int(options[x]))+'.png'), (0+(550*x), 0))
            draw.rectangle((20, 660, 550*len(options)-170, 755), fill='white', width = 2, outline="black")
            draw.rectangle((25, 665, 550*len(options)-175, 750), fill='white', width = 2, outline="black")
            draw.text(((550*len(options)-150)/2-157,692), 'Escoge tu Pokémon...', fill = "black", font = font_name)
    im.save(output + 'ProfessorOak.png')

def ChampionTeam(output = ''):
    a = set(pokemon_species["evolves_from_species_id"].values).symmetric_difference(set(pokemon_species["id"].values))
    a = {x for x in a if x==x}
    options = random.sample(a,6)
    with Image.new('RGBA', (int(550*(len(options)/2)-150), 1405)) as im:
        draw = ImageDraw.Draw(im)
        draw.rectangle((20, 660+630, int(550*(len(options)/2)-170), 755+630), fill='white', width = 2, outline="black")
        draw.rectangle((25, 665+630, int(550*(len(options)/2)-175), 750+630), fill='white', width = 2, outline="black")
        draw.text(((int(550*3)/2-300,692+630)), 'Bienvenido al Salón de la Fama!', fill = "black", font = font_name)
        y=0
        for x in range(3):
            im.paste(Image.open('results/pokemon/pokemon_'+str(int(options[x]))+'.png'), (0+(550*x), 0))
        for x in range(3,6):
            im.paste(Image.open('results/pokemon/pokemon_'+str(int(options[x]))+'.png'), (0+(550*y), 630))
            y+=1
    im.save(output+'ChampionTeam.png')


#Types dictionary

types = {
    1: {'name': 'Normal', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/c/c4/latest/20191221233818/Tipo_normal.png', 'color': '#A8A878', 'color_dark': '#6D6D4E', 'color_light': '#C6C6A7'},
    2: {'name': 'Lucha', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/f/f9/latest/20191221233728/Tipo_lucha.png', 'color': '#C03028', 'color_dark': '#7D1F1A', 'color_light': '#D67873'},
    3: {'name': 'Volador', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/9/9d/latest/20191113212951/Tipo_volador.png', 'color': '#A890F0', 'color_dark': '#6D5E9C', 'color_light': '#C6B7F5'},
    4: {'name': 'Veneno', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/9/92/latest/20191113212951/Tipo_veneno.png', 'color': '#A040A0', 'color_dark': '#682A68', 'color_light': '#C183C1'},
    5: {'name': 'Tierra', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/7/7d/latest/20191113212951/Tipo_tierra.png', 'color': '#E0C068', 'color_dark': '#927D44', 'color_light': '#EBD69D'},
    6: {'name': 'Roca', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/0/05/latest/20191113212950/Tipo_roca.png', 'color': '#B8A038', 'color_dark': '#786824', 'color_light': '#D1C17D'},
    7: {'name': 'Bicho', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/6/6e/latest/20191113212836/Tipo_bicho.png', 'color': '#A8B820', 'color_dark': '#6D7815', 'color_light': '#C6D16E'},
    8: {'name': 'Fantasma', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/5/5f/latest/20191113212837/Tipo_fantasma.png', 'color': '#705898', 'color_dark': '#493963', 'color_light': '#A292BC'},
    9: {'name': 'Acero', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/e/e1/latest/20191113212835/Tipo_acero.png', 'color': '#B8B8D0', 'color_dark': '#787887', 'color_light': '#D1D1E0'},
    10: {'name': 'Fuego', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/a/a7/latest/20191113212837/Tipo_fuego.png', 'color': '#F08030', 'color_dark': '#9C531F', 'color_light': '#F5AC78'},
    11: {'name': 'Agua', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/6/64/latest/20191113212835/Tipo_agua.png', 'color': '#6890F0', 'color_dark': '#445E9C', 'color_light': '#9DB7F5'},
    12: {'name': 'Planta', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/c/ca/latest/20191113212949/Tipo_planta.png', 'color': '#78C850', 'color_dark': '#4E8234', 'color_light': '#A7DB8D'},
    13: {'name': 'Eléctrico', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/5/5d/latest/20191113212836/Tipo_el%C3%A9ctrico.png', 'color': '#F8D030', 'color_dark': '#A1871F', 'color_light': '#FAE078'},
    14: {'name': 'Psíquico', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/f/f5/latest/20191113212950/Tipo_ps%C3%ADquico.png', 'color': '#F85888', 'color_dark': '#A13959', 'color_light': '#FA92B2'},
    15: {'name': 'Hielo', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/1/13/latest/20191113212837/Tipo_hielo.png', 'color': '#98D8D8', 'color_dark': '#638D8D', 'color_light': '#BCE6E6'},
    16: {'name': 'Dragón', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/c/cb/latest/20191113212836/Tipo_drag%C3%B3n.png', 'color': '#7038F8', 'color_dark': '#4924A1', 'color_light': '#A27DFA'},
    17: {'name': 'Siniestro', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/5/5a/latest/20191113212950/Tipo_siniestro.png', 'color': '#705848', 'color_dark': '#49392F', 'color_light': '#A29288'},
    18: {'name': 'Hada', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/5/59/latest/20191113212837/Tipo_hada.png', 'color': '#EE99AC', 'color_dark': '#9B6470', 'color_light': '#F4BDC9'}
}
