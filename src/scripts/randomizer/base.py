# randomizer/base.py

import os
import random
import logging

from src.scripts.randomizer.items import ItemRandomizer

class BaseRandomizer:
  logger = logging.getLogger(f'DEBUG{os.environ.get("VERSION")}')
  MAX_SIMILIAR_STATS_TRIES = 30

  POKEMON_WITH_STATIC_FORM_BY_GENDER = {
    876: ['MALE', 'FEMALE'], # Indeedee(876)
    902: ['MALE', 'FEMALE'], # Basculegion(902)
    916: ['MALE', 'FEMALE']  # Oinkologne(916)
  }

  STATS_RATES = [10,15,20,25]

  pokemonData = {
    "values": []
  }
  personalData = {
    "Table": []
  }
  pokemonList = {}
  abilityList = []
  tmList = []
  moveList = {}
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

  def generateRandomPokemon(self, oldPkmId: dict, options: dict = None, blacklist: list = [], similarStats = False, keepType = False, typeId = None):
    if options["fullPokeDex"]:
      pokemonList = self.pokemonList
    else:
      # Just Paldean Dex
      pokemonList = {id: pokemon for id, pokemon in self.pokemonList.items() if int(id) in self.paldeaDex}

    if not options["legendaries"]:
      # No legendaries allowed
      pokemonList = {id: pokemon for id, pokemon in pokemonList.items() if int(id) not in self.legendaryDex}

    if not options["paradox"]:
      # No paradox allowed
      pokemonList = {id: pokemon for id, pokemon in pokemonList.items() if int(id) not in self.paradoxDex}

    if keepType:
      pokemonList = {id: pokemon for id, pokemon in pokemonList.items() if self.shareAType(newPkmId=int(id), oldPkmId=oldPkmId, typeId=typeId)}

    if similarStats:
      pokemonList = self.listWithSimilarStats(pkmIdToCompare=oldPkmId, pokemonList=pokemonList)

    if len(blacklist) > 0:
      pokemonList = {id: pokemon for id, pokemon in pokemonList.items() if int(id) not in blacklist}

    generatedPokemon = self.getRandomValue(items=list(pokemonList.values()))
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

  def listWithSimilarStats(self, pkmIdToCompare: int, pokemonList: dict = None, pokemonData: list = None):
    filtered = None

    for rate in self.STATS_RATES:
      self.logger.info(f'Testing SimilarStats with Rate {rate}%')
      
      if pokemonList:
        filtered = {id: pokemon for id, pokemon in pokemonList.items() if self.hasSimilarStats(oldPkmId=pkmIdToCompare, newPkmId=int(id), rate=rate)}
      else:
        filtered = [pokemon for pokemon in pokemonData if self.hasSimilarStats(oldPkmId=pkmIdToCompare, newPkmId=int(id), rate=rate)]

      if (len(filtered) > 0):
        break
    
    if filtered is not None and len(filtered) > 0:
      return filtered

    if pokemonList is not None:
      return pokemonList
    else:
      return pokemonData

  def hasSimilarStats(self, rate: int, newPkmId: int, oldPkmId: int = None, oldPkmDevName: str = None):
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

    percentageRate = rate / 100
    diffRate = oldPkmBST * percentageRate

    lowValue = oldPkmBST - diffRate
    highValue = oldPkmBST + diffRate

    result = lowValue <= newPkmBST and highValue >= newPkmBST 

    self.logger.info(f'Old Pokemon {oldPkm["species"]["model"]} Stats: {oldPkmBST}')
    self.logger.info(f'New Pokemon {newPkm["species"]["model"]} Stats: {newPkmBST}')
    self.logger.info(f'lowValue {lowValue}')
    self.logger.info(f'highValue {highValue}')
    self.logger.info(f'hasSimilarStats {result}')

    return result 

  def shareAType(self, typeId: int = None, oldPkmData: dict = None, newPkmdata: dict = None, oldPkmId: int = None, newPkmId: int = None):

    if oldPkmId is not None:
      oldPkmData = self.getPokemonPersonalData(dexId=oldPkmId)
      
    if newPkmId is not None:
      newPkmdata = self.getPokemonPersonalData(dexId=newPkmId)
    
    if typeId is not None:
      originalTypes = [typeId]
    else:
      originalTypes = [oldPkmData["type_1"], oldPkmData["type_2"]]

    if (newPkmdata["type_1"] in originalTypes):
      return True
    if (newPkmdata["type_2"] in originalTypes):
      return True

    return False

  