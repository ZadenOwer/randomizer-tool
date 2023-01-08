import os
import random
import logging

class BaseRandomizer:
  logger = logging.getLogger(os.environ.get('VERSION'))
  MAX_SIMILIAR_STATS_TRIES = 50

  pokemonData = {
    "values": []
  }
  personalData = {
    "Table": []
  }
  pokemonList = []
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
  itemList = []

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

  def generateRandomPaldeaPokemon(self, options: dict = None):
    randomId = self.getRandomValue(self.paldeaDex)

    if (options["legendaries"] == False):
      # No legendaries allowed
      if (randomId in self.legendaryDex):
        return None

    if (options["paradox"] == False):
      # No paradox allowed
      if (randomId in self.paradoxDex):
        return None

    generatedPokemon = next((pk for pk in self.pokemonList if pk["id"] == randomId), None)
    return generatedPokemon

  def generateRandomPokemon(self, options: dict = None):
    randomId = self.getRandomValue(self.pokeDex)

    if (options["legendaries"] == False):
      # No legendaries allowed
      if (randomId in self.legendaryDex):
        return None

    if (options["paradox"] == False):
      # No paradox allowed
      if (randomId in self.paradoxDex):
        return None

    generatedPokemon = next((pk for pk in self.pokemonList if pk["id"] == randomId), None)
    return generatedPokemon

  def generateRandomItem(self, ):
    # itemTypesWeighted helps randomize the type of item that it will be used
    itemTypesWeighted = ['ITEMTYPE_NUTS', 'ITEMTYPE_NUTS', 'ITEMTYPE_NUTS', 'ITEMTYPE_NUTS', 'ITEMTYPE_NUTS', 'ITEMTYPE_NUTS', 'ITEMTYPE_NUTS', 'ITEMTYPE_NUTS', 'ITEMTYPE_NUTS', 'ITEMTYPE_NONE', 'ITEMTYPE_NONE', 'ITEMTYPE_NONE', 'ITEMTYPE_NONE', 'ITEMTYPE_NONE', 'ITEMTYPE_NONE', 'ITEMTYPE_NONE', 'ITEMTYPE_NONE', 'ITEMTYPE_NONE', 'ITEMTYPE_DRUG', 'ITEMTYPE_DRUG', 'ITEMTYPE_DRUG', 'ITEMTYPE_DRUG', 'ITEMTYPE_DRUG', 'ITEMTYPE_DRUG', 'ITEMTYPE_BALL', 'ITEMTYPE_BALL', 'ITEMTYPE_BALL', 'ITEMTYPE_BALL', 'ITEMTYPE_BALL', 'ITEMTYPE_BALL', 'ITEMTYPE_WAZA', 'ITEMTYPE_WAZA', 'ITEMTYPE_WAZA', 'ITEMTYPE_WAZA', 'ITEMTYPE_WAZA', 'ITEMTYPE_WAZA']
    bannedFieldPocket = [
      'FPOCKET_PICNIC' # Skip all the picnic items
    ]

    itemType = self.getRandomValue(items=itemTypesWeighted)

    itemsByType = list(filter(
      lambda item: item["SetToPoke"] == True and item["ItemType"] == itemType and item["FieldPocket"] not in bannedFieldPocket,
      self.itemData["values"]
    ))

    item = None
    while (item is None):
      itemRaw = self.getRandomValue(items=itemsByType)
      item = next((item for item in self.itemList if item["id"] == itemRaw["Id"]), None)    

    return item

  def getPokemonPersonalData(self, dexId: int):
    return next((pokemon for pokemon in self.personalData["entry"] if pokemon["species"]["model"] == dexId), None)

  def getPokemonDev(self, dexId: int = None, devName: str = None):
    if dexId is not None:
      return next((pokemon for pokemon in self.pokemonList if pokemon["id"] == dexId), None)
    
    return next((pokemon for pokemon in self.pokemonList if pokemon["devName"] == devName), None)

  def getRandomForm(self, dexId: int, forms: int):
    # Randomize the forms of the pokemon
    if forms == 1:
      return 0, "DEFAULT"

    randomForm = self.getRandomValue(items=range(0,forms))
    
    if dexId in [876, 902, 916]: # 	Indeedee(876), Basculegion(902), Oinkologne(916)
      if randomForm == 0:
        return randomForm, "MALE"
      if randomForm == 1:
        return randomForm, "FEMALE"

    return randomForm, "DEFAULT"

  def getBaseStatsTotal(self, pkmPersonalData: dict):
    statsKey = ["HP", "ATK", "DEF", "SPA", "SPD", "SPE"]
    stats = pkmPersonalData["base_stats"]
    total = 0
    for key in statsKey:
      total += stats[key]

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

    if oldPkmDevName is not None:
      pkmDev = self.getPokemonDev(devName=oldPkmDevName)
      oldPkm = self.getPokemonPersonalData(pkmDev["id"])

    if oldPkm is None:
      return True

    oldPkmBST = self.getBaseStatsTotal(oldPkm)
    newPkmBST = self.getBaseStatsTotal(newPkm)

    lowValue = (oldPkmBST * 10) / 11
    highValue = (oldPkmBST * 11) / 10

    self.logger.info(f'Old Pokemon {oldPkm["species"]["model"]} Stats: {oldPkmBST}')
    self.logger.info(f'New Pokemon {newPkm["species"]["model"]} Stats: {newPkmBST}')
    self.logger.info(f'lowValue {lowValue}')
    self.logger.info(f'highValue {highValue}')

    result = lowValue <= newPkmBST and highValue >= newPkmBST 
    self.logger.info(f'hasSimilarStats {result}')

    return result 

  def checkEvoStats(self, oldPkmPersonalData: dict, newPkmPersonalData: dict):
    self.logger.info(f'Checking evos stats for {newPkmPersonalData["species"]["model"]}')

    if oldPkmPersonalData is None or newPkmPersonalData is None:
      self.logger.info('Some of the personal data is None')
      return None

    if oldPkmPersonalData["evo_stage"] == newPkmPersonalData["evo_stage"]:
      self.logger.info('The same evo stage an different base stat, this random pkm is ignored atm')
      return None

    if newPkmPersonalData["egg_hatch"]["species"] == newPkmPersonalData["species"]["model"]:
      self.logger.info('Is a pokemon without evolutions, ignored atm')
      return None

    # Checks if any evolution match
    if oldPkmPersonalData["evo_stage"] == 1:
      #First Evolution
      if self.hasSimilarStats(oldPkmDevName=oldPkmPersonalData["species"]["model"], newPkmId=newPkmPersonalData["egg_hatch"]["species"]):
        self.logger.info('The first evo from the random pkm match')
        return self.getPokemonDev(dexId=newPkmPersonalData["egg_hatch"]["species"])

    if oldPkmPersonalData["evo_stage"] == 2:
      #Second Evolution (or final for some species)
      randomSecondEvo = self.getNextEvolution(dexId=newPkmPersonalData["egg_hatch"]["species"])
      if self.hasSimilarStats(oldPkmDevName=oldPkmPersonalData["species"]["model"], newPkmId=randomSecondEvo["id"]):
        self.logger.info('The second evo from the random pkm match')
        return randomSecondEvo

    if oldPkmPersonalData["evo_stage"] == 3:
      #Third Evolution
      randomFinalEvo = self.getFinalEvolution(dexId=newPkmPersonalData["id"])
      if self.hasSimilarStats(oldPkmDevName=oldPkmPersonalData["species"]["model"], newPkmId=randomFinalEvo["id"]):
        self.logger.info('The third evo from the random pkm match')
        return randomFinalEvo

    self.logger.info('Not evo match was found')
    return None

