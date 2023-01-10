# randomizer/base.py

import os
import random
import logging

from src.scripts.randomizer.items import ItemRandomizer

class BaseRandomizer:
  logger = logging.getLogger(f'DEBUG{os.environ.get("VERSION")}')

  POKEMON_WITH_STATIC_FORM_BY_GENDER = {
    876: ['MALE', 'FEMALE'], # Indeedee
    902: ['MALE', 'FEMALE'], # Basculegion
    916: ['MALE', 'FEMALE']  # Oinkologne
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

  pokemonFilteredList = {}

  def __init__(self, data: dict, options: dict) -> None:
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

    self.preparePokemonFilteredList(options=options)

  def preparePokemonFilteredList(self, options: dict, blacklist: list = [], oldPkmId: int = None, typesIds: list = None, growthRate: int = None, evoStage: int = None):
    if options["fullPokeDex"]:
      pokemonList = self.pokemonList.copy()
    else:
      # Just Paldean Dex
      pokemonList = {id: pokemon for id, pokemon in self.pokemonList.items() if int(id) in self.paldeaDex}

    filtered = {}

    for id, pokemon in pokemonList.items():
      if int(id) in blacklist:
        continue

      if oldPkmId is not None and int(id) == oldPkmId:
        continue

      if not options["legendaries"] and int(id) in self.legendaryDex:
        # No legendaries allowed
        continue

      if not options["paradox"] and int(id) in self.paradoxDex:
        # No paradox allowed
        continue

      if growthRate is not None and evoStage is not None and typesIds is not None:
        pkmData = self.getPokemonPersonalData(dexId=int(id))
        if growthRate is not None and pkmData["xp_growth"] != growthRate:
          # Not same growth rate
          continue
        
        if evoStage is not None and pkmData["evo_stage"] != evoStage:
          # Not same evo stage
          continue

        if typesIds is not None and not self.shareAType(newPkmId=int(id), oldPkmId=oldPkmId, typesIds=typesIds):
          # Not the same type needed
          continue

      filtered[id] = pokemon

    self.pokemonFilteredList = pokemonList

  def getRandomPokemon(self, oldPkmId:int = None, similarStats = False):
    randomPokemon = None

    if similarStats:
      randomOptions = [self.getRandomValue(list(self.pokemonFilteredList.values())) for _ in range(30)]

      for rate in self.STATS_RATES:
        filteredByStatsRate = [pokemon for pokemon in randomOptions if self.hasSimilarStats(newPkmId=pokemon["id"], oldPkmId=oldPkmId, rate=rate)]

        if len(filteredByStatsRate) > 0:
          randomPokemon = self.getRandomValue(items=filteredByStatsRate)
          break

    if randomPokemon is None:
      randomPokemon = self.getRandomValue(list(self.pokemonFilteredList.values()))

    return randomPokemon

  def getRandomValue(self, items: list):
    return random.choice(items)

  def generateRandomItem(self):
    itemRandomizer = ItemRandomizer(data={"itemData": self.itemData, "itemList": self.itemList})

    return itemRandomizer.getRandomItem()

  def getPokemonPersonalData(self, dexId: int):
    return next((pokemon for pokemon in self.personalData["entry"] if pokemon["species"]["species"] == dexId), None)

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

    return self.getPokemonDev(pokemon["species"]["species"])

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

    return self.getPokemonDev(pokemon["species"]["species"])

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

  def hasSimilarStats(self, newPkmId: int, oldPkmId: int, rate: int):
    oldPkm = self.getPokemonPersonalData(dexId=oldPkmId)
    newPkm = self.getPokemonPersonalData(dexId=newPkmId)

    oldPkmBST = self.getBaseStatsTotal(pkmPersonalData=oldPkm)
    newPkmBST = self.getBaseStatsTotal(pkmPersonalData=newPkm)
        
    percentageRate = rate / 100
    diffRate = oldPkmBST * percentageRate

    lowValue = oldPkmBST - diffRate
    highValue = oldPkmBST + diffRate

    result = lowValue <= newPkmBST and highValue >= newPkmBST 

    return result

  def shareAType(self, typesIds: list = None, oldPkmData: dict = None, newPkmdata: dict = None, oldPkmId: int = None, newPkmId: int = None):

    if oldPkmId is not None:
      oldPkmData = self.getPokemonPersonalData(dexId=oldPkmId)
      
    if newPkmId is not None:
      newPkmdata = self.getPokemonPersonalData(dexId=newPkmId)
    
    if typesIds is not None:
      originalTypes = typesIds
    else:
      originalTypes = [oldPkmData["type_1"], oldPkmData["type_2"]]

    if (newPkmdata["type_1"] in originalTypes):
      return True
    if (newPkmdata["type_2"] in originalTypes):
      return True

    return False

  