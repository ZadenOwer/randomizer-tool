# randomizer/base.py

import os
import random
import logging

from src.scripts.randomizer.items import ItemRandomizer

class BaseRandomizer:
  logger = logging.getLogger(os.environ.get('VERSION'))
  MAX_SIMILIAR_STATS_TRIES = 30

  POKEMON_WITH_STATIC_FORM_BY_GENDER = {
    876: ['MALE', 'FEMALE'], # Indeedee(876)
    902: ['MALE', 'FEMALE'], # Basculegion(902)
    916: ['MALE', 'FEMALE']  # Oinkologne(916)
  }

  pokemonData = {
    "values": []
  }
  personalData = {
    "Table": []
  }
  pokemonList = {}
  abilityList = []
  tmList = []
  moveList = []
  pokeDex = []
  paldeaDex = []
  legendaryDex = []
  paradoxDex = []
  addPokemonEvents = []
  fixedPokemonEvents = []

  itemData = {
    "values": []
  }
  itemList = {}

  trainersData = {
    "values": []
  }

  def __init__(self, data: dict) -> None:
    self.pokemonData = data["pokedata_array_file"]
    self.personalData = data["personal_array_file"]
    self.pokemonList = data["pokemon_list_file"]
    self.abilityList = data["ability_list_file"]
    self.tmList = data["tm_list_file"]
    self.moveList = data["move_list_file"]
    self.pokeDex = data["pokeDex"]
    self.paldeaDex = data["paldeaDex"]
    self.legendaryDex = data["legendaryDex"]
    self.paradoxDex = data["paradoxDex"]
    self.addPokemonEvents = data["add_pokemon_events_file"]
    self.fixedPokemonEvents = data["fixed_pokemon_events_file"]
    
    self.itemData = data["itemdata_array_file"]
    self.itemList = data["item_list_file"]
    
    self.trainersData = data["trainersdata_array_file"]

  def getRandomValue(self, items: list):
    return random.choice(items)

  def generateRandomPokemon(self, options: dict = None, blacklist: list = []):
    if options["fullPokeDex"]:
      filteredList = self.pokemonList
    else:
      # Just Paldean Dex
      filteredList = {id: pokemon for id, pokemon in self.pokemonList.items() if int(id) in self.paldeaDex}

    if not options["legendaries"]:
      # No legendaries allowed
      filteredList = {id: pokemon for id, pokemon in filteredList.items() if int(id) not in self.legendaryDex}

    if not options["paradox"]:
      # No paradox allowed
      filteredList = {id: pokemon for id, pokemon in filteredList.items() if int(id) not in self.paradoxDex}

    if len(blacklist) > 0:
      filteredList = {id: pokemon for id, pokemon in filteredList.items() if int(id) not in blacklist}

    generatedPokemon = self.getRandomValue(items=list(filteredList.values()))
    return generatedPokemon

  def generateRandomItem(self):
    itemRandomizer = ItemRandomizer(data={"itemData": self.itemData, "itemList": self.itemList})

    return itemRandomizer.getRandomItem()

  def getPokemonPersonalData(self, dexId: int):
    return next((pokemon for pokemon in self.personalData["entry"] if pokemon["species"]["model"] == dexId), None)

  def getPokemonDev(self, dexId: int = None, devName: str = None):
    if dexId is not None:
      return self.pokemonList[str(dexId)]
    
    return next((pokemon for pokemon in list(self.pokemonList.values()) if pokemon["devName"] == devName), None)

  def getNextEvolution(self, dexId: int = None, devName: str = None):
    if dexId == 0 or (dexId is None and devName is None) or devName == "DEV_NULL":
      return None

    pokemon = None

    if dexId is not None:
      pokemon = self.getPokemonPersonalData(dexId)

    if devName is not None:
      pkmDev = self.getPokemonDev(devName=devName)
      pokemon = self.getPokemonPersonalData(pkmDev["id"])
    
    if pokemon == None:
      return None

    if len(pokemon["evo_data"]) == 0:
      return None
    
    randomPossibleEvo = self.getRandomValue(items=pokemon["evo_data"])
    pokemon = self.getPokemonPersonalData(dexId=randomPossibleEvo["species"])
    
    if pokemon == None:
      return None

    return self.getPokemonDev(pokemon["species"]["model"])

  def getFinalEvolution(self, dexId: int = None, devName: str = None):
    if dexId == 0 or (dexId is None and devName is None) or devName == "DEV_NULL":
      return {"devName": "DEV_NULL", "id": 0}

    if devName is not None:
      pkmDev = self.getPokemonDev(devName=devName)
      if pkmDev is None:
        return None

      dexId = pkmDev["id"]
    
    pokemon = self.getPokemonPersonalData(dexId=dexId)

    if pokemon is None:
      return None
    
    while len(pokemon["evo_data"]) != 0:
      evoData = pokemon["evo_data"][0]
      if len(pokemon["evo_data"]) > 1:
        evoData = self.getRandomValue(items=pokemon["evo_data"])

      pokemon = self.getPokemonPersonalData(dexId=evoData["species"])
    
    if pokemon is None:
      return None

    return self.getPokemonDev(pokemon["species"]["model"])

  def getRandomForm(self, dexId: int, forms: int):
    # Randomize the forms of the pokemon
    if forms == 1:
      return 0, "DEFAULT"

    randomForm = random.randint(0, forms - 1)
    genderNames = self.POKEMON_WITH_STATIC_FORM_BY_GENDER.get(dexId, ['DEFAULT'])

    if genderNames == ['DEFAULT']:
      return randomForm, 'DEFAULT'

    return randomForm, genderNames[randomForm]

  def getBaseStatsTotal(self, pkmPersonalData: dict):
    statsKey = ["HP", "ATK", "DEF", "SPA", "SPD", "SPE"]
    stats = pkmPersonalData["base_stats"]
    total = sum(stats[key] for key in statsKey)

    return total

  def hasSimilarStats(self, newPkmId: int, oldPkmId: int = None, oldPkmDevName: str = None):
    if oldPkmId is None and oldPkmDevName is None:
      return True

    newPkm = self.getPokemonPersonalData(dexId=newPkmId)

    if newPkm is None:
      return True

    oldPkm = None

    if oldPkmId is not None:
      oldPkm = self.getPokemonPersonalData(oldPkmId)
    elif oldPkmDevName is not None:
      pkmDev = self.getPokemonDev(devName=oldPkmDevName)
      oldPkm = self.getPokemonPersonalData(pkmDev["id"])

    if oldPkm is None:
      return True

    oldPkmBST = self.getBaseStatsTotal(oldPkm)
    newPkmBST = self.getBaseStatsTotal(newPkm)

    lowValue = (oldPkmBST * 10) / 11
    highValue = (oldPkmBST * 11) / 10

    result = lowValue <= newPkmBST and highValue >= newPkmBST 

    self.logger.info(f'Old Pokemon {oldPkm["species"]["model"]} Stats: {oldPkmBST}')
    self.logger.info(f'New Pokemon {newPkm["species"]["model"]} Stats: {newPkmBST}')
    self.logger.info(f'lowValue {lowValue}')
    self.logger.info(f'highValue {highValue}')
    self.logger.info(f'hasSimilarStats {result}')

    return result 

  def checkEvoStats(self, oldPkmPersonalData: dict, newPkmPersonalData: dict):
    self.logger.info(f'Checking evos stats for {newPkmPersonalData["species"]["model"]}')

    if oldPkmPersonalData is None or newPkmPersonalData is None:
      return None

    if len(newPkmPersonalData["evo_data"]) == 0:
      self.logger.info('Is a pokemon without evolutions, ignored atm')
      return None

    evoStages = {
      1: self.getPokemonDev(dexId=newPkmPersonalData["egg_hatch"]["species"]),
      2: self.getNextEvolution(dexId=newPkmPersonalData["egg_hatch"]["species"]),
      3: self.getFinalEvolution(dexId=newPkmPersonalData["egg_hatch"]["species"])
    }

    for evoStage, evolution in evoStages.items():
      if oldPkmPersonalData["evo_stage"] == evoStage:
        if self.hasSimilarStats(oldPkmDevName=oldPkmPersonalData["species"]["model"], newPkmId=evolution["id"]):
          self.logger.info(f'The {evoStage} evo from the random pkm match')
          return evolution

    self.logger.info('Not evo match was found')
    return None

