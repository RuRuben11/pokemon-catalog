exec(open('code/load.py').read())

#Generate individual figures for default Pokemons
plotPokemonCard(83, form = 'galar', output = 'results/pokemon/')

#Generate evolutionary line of a family of Pokemons
for chain in list(dict.fromkeys(pokemon_species.evolution_chain_id.values)):
    plotEvoLine(chain, output = 'results/evolutions/')
    print(chain)

#Let's see which starters does Professor Oak offers to you...
ProfessorOak()

#Congrats, you are the Pokemon Champions! Run this function and see which Pokemons have you used in your adventure
ChampionTeam()

