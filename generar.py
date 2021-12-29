import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests
import pandas as pd
import numpy as np
import io
from io import BytesIO

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

#Types dictionary
types = {
    1: {'name': 'normal', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/c/c4/latest/20191221233818/Tipo_normal.png', 'color': '#A8A878', 'color_dark': '#6D6D4E', 'color_light': '#C6C6A7'},
    2: {'name': 'fighting', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/f/f9/latest/20191221233728/Tipo_lucha.png', 'color': '#C03028', 'color_dark': '#7D1F1A', 'color_light': '#D67873'},
    3: {'name': 'flying', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/9/9d/latest/20191113212951/Tipo_volador.png', 'color': '#A890F0', 'color_dark': '#6D5E9C', 'color_light': '#C6B7F5'},
    4: {'name': 'poison', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/9/92/latest/20191113212951/Tipo_veneno.png', 'color': '#A040A0', 'color_dark': '#682A68', 'color_light': '#C183C1'},
    5: {'name': 'ground', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/7/7d/latest/20191113212951/Tipo_tierra.png', 'color': '#E0C068', 'color_dark': '#927D44', 'color_light': '#EBD69D'},
    6: {'name': 'rock', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/0/05/latest/20191113212950/Tipo_roca.png', 'color': '#B8A038', 'color_dark': '#786824', 'color_light': '#D1C17D'},
    7: {'name': 'bug', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/6/6e/latest/20191113212836/Tipo_bicho.png', 'color': '#A8B820', 'color_dark': '#6D7815', 'color_light': '#C6D16E'},
    8: {'name': 'ghost', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/5/5f/latest/20191113212837/Tipo_fantasma.png', 'color': '#705898', 'color_dark': '#493963', 'color_light': '#A292BC'},
    9: {'name': 'steel', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/e/e1/latest/20191113212835/Tipo_acero.png', 'color': '#B8B8D0', 'color_dark': '#787887', 'color_light': '#D1D1E0'},
    10: {'name': 'fire', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/a/a7/latest/20191113212837/Tipo_fuego.png', 'color': '#F08030', 'color_dark': '#9C531F', 'color_light': '#F5AC78'},
    11: {'name': 'water', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/6/64/latest/20191113212835/Tipo_agua.png', 'color': '#6890F0', 'color_dark': '#445E9C', 'color_light': '#9DB7F5'},
    12: {'name': 'grass', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/c/ca/latest/20191113212949/Tipo_planta.png', 'color': '#78C850', 'color_dark': '#4E8234', 'color_light': '#A7DB8D'},
    13: {'name': 'electric', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/5/5d/latest/20191113212836/Tipo_el%C3%A9ctrico.png', 'color': '#F8D030', 'color_dark': '#A1871F', 'color_light': '#FAE078'},
    14: {'name': 'psychic', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/f/f5/latest/20191113212950/Tipo_ps%C3%ADquico.png', 'color': '#F85888', 'color_dark': '#A13959', 'color_light': '#FA92B2'},
    15: {'name': 'ice', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/1/13/latest/20191113212837/Tipo_hielo.png', 'color': '#98D8D8', 'color_dark': '#638D8D', 'color_light': '#BCE6E6'},
    16: {'name': 'dragon', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/c/cb/latest/20191113212836/Tipo_drag%C3%B3n.png', 'color': '#7038F8', 'color_dark': '#4924A1', 'color_light': '#A27DFA'},
    17: {'name': 'dark', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/5/5a/latest/20191113212950/Tipo_siniestro.png', 'color': '#705848', 'color_dark': '#49392F', 'color_light': '#A29288'},
    18: {'name': 'fairy', 'sprite': 'https://images.wikidexcdn.net/mwuploads/wikidex/5/59/latest/20191113212837/Tipo_hada.png', 'color': '#EE99AC', 'color_dark': '#9B6470', 'color_light': '#F4BDC9'}
}


#Extract and edit data from PokeAPI
pokemon_url = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon.csv'
pokemon_species_url = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon_species.csv'
pokemon_types_url = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon_types.csv'
pokemon_desc_url = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon_species_names.csv'
pokemon_forms_url = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon_forms.csv'
pokemon_evolutions_url = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon_evolution.csv'

pokemon = pd.read_csv(pokemon_url)
pokemon_species = pd.read_csv(pokemon_species_url)
pokemon_types = pd.read_csv(pokemon_types_url)
pokemon_desc = pd.read_csv(pokemon_desc_url)
pokemon_forms = pd.read_csv(pokemon_forms_url)
pokemon_evolutions  = pd.read_csv(pokemon_evolutions_url)

pokemon_desc_esp = pokemon_desc[pokemon_desc["local_language_id"] == 7]
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

for mon in range(300,899):
    img =ImageURL("https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/"+str(mon)+".png",400,400)
    n_types=len(pokemon_types[pokemon_types["pokemon_id"] == mon])
    type1_pkmn=pokemon_types[(pokemon_types["slot"] == 1) & (pokemon_types["pokemon_id"] == mon)].type_id.values.astype(int)[0]
    img2=ImageURL(types[type1_pkmn]['sprite'],100,22)
    if n_types == 2:
        type2_pkmn=pokemon_types[(pokemon_types["slot"] == 2) & (pokemon_types["pokemon_id"] == mon)].type_id.values.astype(int)[0]
        img3=ImageURL(types[type2_pkmn]['sprite'],100,22)
    with Image.new('RGBA', (400, 580)) as im:
        im.paste(img, (0, 100))
        if n_types == 1:
            im.paste(img2,(150,500))
        else:
            im.paste(img2,(95,500))
            im.paste(img3,(205,500))
        draw = ImageDraw.Draw(im)
        draw.rounded_rectangle((60, 10, 360, 62), fill="white", outline="black",width=4, radius=70)
        draw.rounded_rectangle((60, 58, 360, 100), fill="grey", outline="black",width=4, radius=70)
        draw.rectangle((35, 535, 360, 575), fill=types[type1_pkmn]['color_light'])
        draw.ellipse((35, 10, 125, 100), fill = types[type1_pkmn]['color'], outline ='black',width=4)
        draw.text((135,21), pokemon_species[(pokemon_species["id"] == mon)].identifier.values.astype(str)[0].capitalize(), fill = "black", font = font_name)
        draw.text((135,70), pokemon_desc_esp[(pokemon_desc_esp["pokemon_species_id"] == mon)].genus.values.astype(str)[0], fill = "white", font = font_desc)
        draw.text((48,33), str(mon).zfill(3), fill = "white", font = font_num)
        draw.text((65,548), "Altura:", fill = "black", font = font_data)
        draw.text((210,548), "Peso:", fill = "black", font = font_data)
        draw.text((123,548), str(round(pokemon[(pokemon["id"] == mon)].height.values[0]*0.1,1))+' m', fill = "black", font = font_data2)
        draw.text((260,548), str(round(pokemon[(pokemon["id"] == mon)].weight.values[0]*0.1,1))+' kg', fill = "black", font = font_data2)
    im.save("figures/pokemon_"+str(mon)+".png")




#Evo chains
test = pokemon_species[pokemon_species["evolution_chain_id"] == 26]

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

if ncol_evo > 1:
    evo_text = [[] for _ in range(nrow_evo)]
    evo_object = [[] for _ in range(nrow_evo)]
    for x in range(nrow_evo):
        y=0
        for a in evo_mech[x]:
            if a == 1:
                if np.isfinite(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].minimum_level.values[0]):
                    evo_text[x].append('Nivel '+ str(int(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].minimum_level.values[0])))
                    evo_object[x].append(ImageLocal("resources/items/item_50.png", 44,44))
                elif np.isfinite(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].minimum_happiness.values[0]):
                    evo_text[x].append('Amistad')
                    evo_object[x].append(ImageLocal("resources/items/item_50.png", 44,44))
                elif np.isfinite(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].location_id.values[0]):
                    evo_text[x].append('Ubicación')
                    evo_object[x].append(ImageLocal("resources/items/item_50.png", 44,44))                    
                y+=1
            elif a == 2:
                evo_text[x].append('Intercamb.')
                if pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].held_item_id.isna().values[0]:
                    evo_object[x].append('https://cdn-icons-png.flaticon.com/512/103/103588.png')
                else:
                    evo_item=str(int(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].held_item_id.values[0]))
                    evo_object[x].append(ImageLocal('resources/items/item_'+ evo_item +'.png', 44,44))
                y+=1
            elif a == 3:
                evo_text[x].append('Objeto')
                evo_item=str(int(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].trigger_item_id.values[0]))
                evo_object[x].append(ImageLocal('resources/items/item_'+ evo_item +'.png', 44,44))
                y+=1
            elif a == 4:
                evo_text[y] = 'Shedinja'
                response = requests.get('https://w7.pngwing.com/pngs/324/645/png-transparent-pokemon-go-gotcha-video-game-jynx-pokeball-orange-pokemon-technology.png')
                evo_object[y] = Image.open(BytesIO(response.content))
                newsize=(44,44)
                evo_object[y]=evo_object[y].resize(newsize)
            elif a == 5:
                evo_text[y] = 'Sirfetchd'
                response = requests.get('https://w7.pngwing.com/pngs/324/645/png-transparent-pokemon-go-gotcha-video-game-jynx-pokeball-orange-pokemon-technology.png')
                evo_object[y] = Image.open(BytesIO(response.content))
                newsize=(44,44)
                evo_object[y]=evo_object[y].resize(newsize)


#Color of the line
evo_type = pokemon_types[(pokemon_types["slot"] == 1) & (pokemon_types["pokemon_id"] == evo_matrix[0][0])].type_id.values[0]

with Image.new('RGBA', ((550*len(evo_matrix[0]))-150, (580*len(evo_matrix)))) as im:
    draw = ImageDraw.Draw(im)
    for x in range(len(evo_matrix)):
        y = 0
        for a in evo_matrix[x]:
            if all_same([item[y] for item in evo_matrix]):
                im.paste(evo_image[x][y], (0+(550*y), int(580*len(evo_matrix)/2-290)))
            else:
                im.paste(evo_image[x][y], (0+(550*y), 0+(580*x)))
            y+=1
    for x in range(len(evo_text)):
        y = 0
        for text in evo_text[x]:
            if all_same([item[y+1] for item in evo_matrix]):
                draw.rectangle((400+(550*y), 310+int(580*len(evo_matrix)/2-290), 510+(550*y), 340+int(580*len(evo_matrix)/2-290)), fill=types[evo_type]['color_light'])
                draw.polygon([(550+(550*y),325+int(580*len(evo_matrix)/2-290)), (510+(550*y), 290+int(580*len(evo_matrix)/2-290)), (510+(550*y),360+int(580*len(evo_matrix)/2-290))], fill = types[evo_type]['color_light'])
                draw.text((425+(550*y),317+int(580*len(evo_matrix)/2-290)), text, fill = "black", font = font_desc)
                im.paste(evo_object[x][y], (444+(550*y),255+int(580*len(evo_matrix)/2-290)))
            else:
                draw.rectangle((400+(550*y), 310+(580*x), 510+(550*y), 340+(580*x)), fill=types[evo_type]['color_light'])
                draw.polygon([(550+(550*y),325+(580*x)), (510+(550*y), 290+(580*x)), (510+(550*y),360+(580*x))], fill = types[evo_type]['color_light'])
                draw.text((425+(550*y),317+(580*x)), text, fill = "black", font = font_desc)
                im.paste(evo_object[x][y], (444+(550*y),255+(580*x)))
            y+=1


im.save("out.png")




#Paste icon if mega or gmax form
if 'mega' in pokemon_forms[pokemon_forms["pokemon_id"].isin(pokemon[pokemon["species_id"] == mon].id.values)].form_identifier.values:
    response = requests.get('https://megaevolutionradio.radio12345.com/users.img/2805091/96/53/438455218965.thumb.png')
    img4 = Image.open(BytesIO(response.content))
    newsize2=(30,30)
    img4=img4.resize(newsize2)
    im.paste(img4,(320,85), img4)

if 'gmax' in pokemon_forms[pokemon_forms["pokemon_id"].isin(pokemon[pokemon["species_id"] == mon].id.values)].form_identifier.values:
    response = requests.get('https://megaevolutionradio.radio12345.com/users.img/2805091/96/53/438455218965.thumb.png')
    img4 = Image.open(BytesIO(response.content))
    newsize2=(30,30)
    img4=img4.resize(newsize2)
    im.paste(img4,(320,85))