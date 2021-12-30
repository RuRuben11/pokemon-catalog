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

def generate_pokemon(pokemon_id):
    img =ImageURL("https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/"+str(pokemon_id)+".png",400,400)
    n_types=len(pokemon_types[pokemon_types["pokemon_id"] == pokemon_id])
    type1_pkmn=pokemon_types[(pokemon_types["slot"] == 1) & (pokemon_types["pokemon_id"] == pokemon_id)].type_id.values.astype(int)[0]
    img2=ImageURL(types[type1_pkmn]['sprite'],100,22)
    if n_types == 2:
        type2_pkmn=pokemon_types[(pokemon_types["slot"] == 2) & (pokemon_types["pokemon_id"] == pokemon_id)].type_id.values.astype(int)[0]
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
        draw.text((135,21), pokemon_species[(pokemon_species["id"] == pokemon_id)].identifier.values.astype(str)[0].capitalize(), fill = "black", font = font_name)
        draw.text((135,70), pokemon_desc_esp[(pokemon_desc_esp["pokemon_species_id"] == pokemon_id)].genus.values.astype(str)[0], fill = "white", font = font_desc)
        draw.text((48,33), str(pokemon_id).zfill(3), fill = "white", font = font_num)
        draw.text((65,548), "Altura:", fill = "black", font = font_data)
        draw.text((210,548), "Peso:", fill = "black", font = font_data)
        draw.text((123,548), str(round(pokemon[(pokemon["id"] == pokemon_id)].height.values[0]*0.1,1))+' m', fill = "black", font = font_data2)
        draw.text((260,548), str(round(pokemon[(pokemon["id"] == pokemon_id)].weight.values[0]*0.1,1))+' kg', fill = "black", font = font_data2)
    return im

def evolution_data(evo_matrix, evo_mech):
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
                    elif np.isfinite(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].held_item_id.values[0]):
                        evo_text[x].append('Subir nivel')
                        evo_item=str(int(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].held_item_id.values[0]))
                        evo_object[x].append(ImageLocal('resources/items/item_'+ evo_item +'.png', 44,44))
                    elif np.isfinite(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].known_move_id.values[0]):
                        evo_move=str(int(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].known_move_id.values[0]))
                        ataque=move_names_esp[move_names_esp["move_id"]==evo_move].name.values[0]
                        evo_text[x].append('MT:'+ataque)
                        evo_object[x].append(ImageLocal('resources/items/item_50.png', 44,44))
                    elif np.isfinite(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].known_move_type_id.values[0]):
                        evo_move=str(int(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].known_move_type_id.values[0]))
                        ataque=types[evo_move]['name']
                        evo_text[x].append('Ataque '+ataque)
                        evo_object[x].append(ImageLocal('resources/items/item_50.png', 44,44))
                    elif np.isfinite(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].minimum_beauty.values[0]):
                        evo_text[x].append('Belleza')
                        evo_object[x].append(ImageLocal('resources/items/item_50.png', 44,44))
                    elif np.isfinite(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].party_species_id.values[0]):
                        party = pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].party_species_id.values[0]
                        evo_text[x].append('Subir nivel')
                        evo_object[x].append(ImageURL('https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/'+ party +'.png', 44,44))                
                    elif np.isfinite(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].location_id.values[0]):
                        evo_text[x].append('Ubicación')
                        evo_object[x].append(ImageLocal("resources/items/item_50.png", 44,44))
                elif a == 2:
                    evo_text[x].append('Intercambio')
                    if pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].held_item_id.notna().values[0]:
                        evo_item=str(int(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].held_item_id.values[0]))
                        evo_object[x].append(ImageLocal('resources/items/item_'+ evo_item +'.png', 44,44))
                    elif pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].trade_species_id.notna().values[0]:
                        evo_species=str(int(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].trade_species_id.values[0]))
                        evo_object[x].append(ImageURL('https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/'+ evo_species +'.png', 44,44))                     
                    else:
                        evo_object[x].append(ImageURL('https://cdn-icons-png.flaticon.com/512/103/103588.png',44,44))
                elif a == 3:
                    evo_text[x].append('Objeto')
                    evo_item=str(int(pokemon_evolutions[pokemon_evolutions["evolved_species_id"] == evo_matrix[x][y+1]].trigger_item_id.values[0]))
                    evo_object[x].append(ImageLocal('resources/items/item_'+ evo_item +'.png', 44,44))
                elif a == 4:
                    evo_text[y] = 'Espacio'
                    evo_object[x].append(ImageLocal('resources/items/item_4.png', 44,44))
                elif a == 5:
                    if evo_matrix[x][y+1] == 865:
                        evo_text[y] = '3 críticos'
                        evo_object[x].append(ImageLocal('resources/items/item_236.png', 44,44))
                    elif evo_matrix[x][y+1] == 867:
                        evo_text[y] = '-49 PS'
                        evo_object[x].append(ImageLocal('resources/items/item_252.png', 44,44))
                    elif evo_matrix[x][y+1] == 869:
                        evo_text[y] = 'Girar'
                        evo_object[x].append(ImageLocal('resources/items/item_1167.png', 44,44))
                    elif evo_matrix[x][y+1] == 892:
                        evo_text[y] = 'Torre DLC'
                        evo_object[x].append(ImageURL('https://cdn-icons-png.flaticon.com/512/463/463574.png', 44,44))             
                y+=1
    return evo_text, evo_object


def plot_EvoLine(evo_matrix, evo_image, evo_text, evo_append):
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
                    im.paste(evo_append[x][y], (485+(550*y), 325+int(580*len(evo_matrix)/2-290)),evo_append[x][y])
                else:
                    draw.rectangle((400+(550*y), 310+(580*x), 510+(550*y), 340+(580*x)), fill=types[evo_type]['color_light'])
                    draw.polygon([(550+(550*y),325+(580*x)), (510+(550*y), 290+(580*x)), (510+(550*y),360+(580*x))], fill = types[evo_type]['color_light'])
                    draw.text((425+(550*y),317+(580*x)), text, fill = "black", font = font_desc)
                    im.paste(evo_object[x][y], (444+(550*y),255+(580*x)))
                    im.paste(evo_append[x][y], (485+(550*y), 325+(580*x)),evo_append[x][y])
                y+=1
    return im




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
