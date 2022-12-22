# randomizer.py
import os
import json
import math
import random

import logging

logger = logging.getLogger(os.environ.get('VERSION'))

# Starting Pokemon Data Imports
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

MAX_SIMILIAR_STATS_TRIES = 50

with (
  open('./src/jsons/pokedata_array.json', 'r', encoding='utf-8-sig') as pokedata_array_file,
  open('./src/jsons/personal_array.json', 'r', encoding='utf-8-sig') as personal_array_file,
  open('./src/jsons/pokemon_list.json', 'r', encoding='utf-8-sig') as pokemon_list_file,
  open('./src/jsons/dex.json', 'r', encoding='utf-8-sig') as dex_file,
  open('./src/jsons/ability_list.json', 'r', encoding='utf-8-sig') as ability_list_file,
  open('./src/jsons/tm_list.json', 'r', encoding='utf-8-sig') as tm_list_file,
  open('./src/jsons/move_list.json', 'r', encoding='utf-8-sig') as move_list_file,
  open('./src/jsons/eventAddPokemon_array.json', 'r', encoding='utf-8-sig') as add_pokemon_events_file,
  open('./src/jsons/fixed_symbol_table_array.json', 'r', encoding='utf-8-sig') as fixed_pokemon_events_file,
):
  pokemonData = json.load(pokedata_array_file)
  personalData = json.load(personal_array_file)
  pokemonList = json.load(pokemon_list_file)
  abilityList = json.load(ability_list_file)
  tmList = json.load(tm_list_file)
  moveList = json.load(move_list_file)
  dex = json.load(dex_file)
  pokeDex = dex["pokeDex"]
  paldeaDex = dex["paldeaDex"]
  legendaryDex = dex["legendaryDex"]
  paradoxDex = dex["paradoxDex"]
  addPokemonEvents = json.load(add_pokemon_events_file)
  fixedPokemonEvents = json.load(fixed_pokemon_events_file)
# Ending Pokemon Data Imports

# Starting Item Data Imports
itemData = {
  "values": []
}
itemList = []

with (
  open('./src/jsons/itemdata_array.json', 'r', encoding='utf-8-sig') as itemdata_array_file,
  open('./src/jsons/item_list.json', 'r', encoding='utf-8-sig') as item_list_file
):
  itemData = json.load(itemdata_array_file)
  itemList = json.load(item_list_file)

# Ending Item Data Imports

# Starting Trainers Data Imports
trainersData = {
  "values": []
}

with (
  open('./src/jsons/trdata_array.json', 'r', encoding='utf-8-sig') as trainersdata_array_file,
):
  trainersData = json.load(trainersdata_array_file)
# Starting Trainers Data Imports

def getRNG(maxValue: int, minValue: int = 0):
  return random.randrange(start=minValue, stop=maxValue, step=1)

def generateRandomPaldeaPokemon(options: dict = None):
  rng = getRNG(maxValue=len(paldeaDex))
  randomId = paldeaDex[rng]

  if (options["legendaries"] == False):
    # No legendaries allowed
    if (randomId in legendaryDex):
      return None

  if (options["paradox"] == False):
    # No paradox allowed
    if (randomId in paradoxDex):
      return None

  generatedPokemon = next((pk for pk in pokemonList if pk["id"] == randomId), None)
  return generatedPokemon

def generateRandomPokemon(options: dict = None):
  rng = getRNG(maxValue=len(pokeDex))
  randomId = pokeDex[rng]

  if (options["legendaries"] == False):
    # No legendaries allowed
    if (randomId in legendaryDex):
      return None

  if (options["paradox"] == False):
    # No paradox allowed
    if (randomId in paradoxDex):
      return None

  generatedPokemon = next((pk for pk in pokemonList if pk["id"] == randomId), None)
  return generatedPokemon

def generateRandomItem():
  # itemTypesWeighted helps randomize the type of item that it will be used
  itemTypesWeighted = ['ITEMTYPE_NUTS', 'ITEMTYPE_NUTS', 'ITEMTYPE_NUTS', 'ITEMTYPE_NUTS', 'ITEMTYPE_NUTS', 'ITEMTYPE_NUTS', 'ITEMTYPE_NUTS', 'ITEMTYPE_NUTS', 'ITEMTYPE_NUTS', 'ITEMTYPE_NONE', 'ITEMTYPE_NONE', 'ITEMTYPE_NONE', 'ITEMTYPE_NONE', 'ITEMTYPE_NONE', 'ITEMTYPE_NONE', 'ITEMTYPE_NONE', 'ITEMTYPE_NONE', 'ITEMTYPE_NONE', 'ITEMTYPE_DRUG', 'ITEMTYPE_DRUG', 'ITEMTYPE_DRUG', 'ITEMTYPE_DRUG', 'ITEMTYPE_DRUG', 'ITEMTYPE_DRUG', 'ITEMTYPE_BALL', 'ITEMTYPE_BALL', 'ITEMTYPE_BALL', 'ITEMTYPE_BALL', 'ITEMTYPE_BALL', 'ITEMTYPE_BALL', 'ITEMTYPE_WAZA', 'ITEMTYPE_WAZA', 'ITEMTYPE_WAZA', 'ITEMTYPE_WAZA', 'ITEMTYPE_WAZA', 'ITEMTYPE_WAZA']
  bannedFieldPocket = [
    'FPOCKET_PICNIC' # Skip all the picnic items
  ]

  rngItemType = getRNG(maxValue=len(itemTypesWeighted))
  itemType = itemTypesWeighted[rngItemType]
  itemsByType = list(filter(
    lambda item: item["SetToPoke"] == True and item["ItemType"] == itemType and item["FieldPocket"] not in bannedFieldPocket,
    itemData["values"]
  ))

  item = None
  while (item is None):
    rngItem = getRNG(maxValue=len(itemsByType))
    itemRaw = itemsByType[rngItem]
    item = next((item for item in itemList if item["id"] == itemRaw["Id"]), None)    

  return item

def getPokemonPersonalData(dexId: int):
  return next((pokemon for pokemon in personalData["entry"] if pokemon["species"]["model"] == dexId), None)

def getPokemonDev(dexId: int = None, devName: str = None):
  if dexId is not None:
    return next((pokemon for pokemon in pokemonList if pokemon["id"] == dexId), None)
  
  return next((pokemon for pokemon in pokemonList if pokemon["devName"] == devName), None)

def getRandomForm(dexId: int, forms: int):
  # Randomize the forms of the pokemon
  if forms == 1:
    return 0, "DEFAULT"

  randomForm = getRNG(forms)
  
  if dexId in [876, 902, 916]: # 	Indeedee(876), Basculegion(902), Oinkologne(916)
    if randomForm == 0:
      return randomForm, "MALE"
    if randomForm == 1:
      return randomForm, "FEMALE"

  return randomForm, "DEFAULT"

def getBaseStatsTotal(pkmPersonalData: dict):
  statsKey = ["HP", "ATK", "DEF", "SPA", "SPD", "SPE"]
  stats = pkmPersonalData["base_stats"]
  total = 0
  for key in statsKey:
    total += stats[key]

  return total

def hasSimilarStats(newPkmId: int, oldPkmId: int = None, oldPkmDevName: str = None):
  if oldPkmId is None and oldPkmDevName is None:
    return True

  newPkm = getPokemonPersonalData(dexId=newPkmId)

  if newPkm is None:
    return True

  oldPkm = None

  if oldPkmId is not None:
    oldPkm = getPokemonPersonalData(oldPkmId)

  if oldPkmDevName is not None:
    pkmDev = getPokemonDev(devName=oldPkmDevName)
    oldPkm = getPokemonPersonalData(pkmDev["id"])

  if oldPkm is None:
    return True

  oldPkmBST = getBaseStatsTotal(oldPkm)
  newPkmBST = getBaseStatsTotal(newPkm)

  lowValue = (oldPkmBST * 10) / 11
  highValue = (oldPkmBST * 11) / 10

  logger.info(f'Old Pokemon {oldPkm["species"]["model"]} Stats: {oldPkmBST}')
  logger.info(f'New Pokemon {newPkm["species"]["model"]} Stats: {newPkmBST}')
  logger.info(f'lowValue {lowValue}')
  logger.info(f'highValue {highValue}')

  result = lowValue <= newPkmBST and highValue >= newPkmBST 
  logger.info(f'hasSimilarStats {result}')

  return result 

def checkEvoStats(oldPkmPersonalData: dict, newPkmPersonalData: dict):
  logger.info(f'Checking evos stats for {newPkmPersonalData["species"]["model"]}')

  if oldPkmPersonalData is None or newPkmPersonalData is None:
    logger.info('Some of the personal data is None')
    return None

  if oldPkmPersonalData["evo_stage"] == newPkmPersonalData["evo_stage"]:
    logger.info('The same evo stage an different base stat, this random pkm is ignored atm')
    return None

  if newPkmPersonalData["egg_hatch"]["species"] == newPkmPersonalData["species"]["model"]:
    logger.info('Is a pokemon without evolutions, ignored atm')
    return None

  # Checks if any evolution match
  if oldPkmPersonalData["evo_stage"] == 1:
    #First Evolution
    if hasSimilarStats(oldPkmDevName=oldPkmPersonalData["species"]["model"], newPkmId=newPkmPersonalData["egg_hatch"]["species"]):
      logger.info('The first evo from the random pkm match')
      return getPokemonDev(dexId=newPkmPersonalData["egg_hatch"]["species"])

  if oldPkmPersonalData["evo_stage"] == 2:
    #Second Evolution (or final for some species)
    randomSecondEvo = getNextEvolution(dexId=newPkmPersonalData["egg_hatch"]["species"])
    if hasSimilarStats(oldPkmDevName=oldPkmPersonalData["species"]["model"], newPkmId=randomSecondEvo["id"]):
      logger.info('The second evo from the random pkm match')
      return randomSecondEvo

  if oldPkmPersonalData["evo_stage"] == 3:
    #Third Evolution
    randomFinalEvo = getFinalEvolution(dexId=newPkmPersonalData["id"])
    if hasSimilarStats(oldPkmDevName=oldPkmPersonalData["species"]["model"], newPkmId=randomFinalEvo["id"]):
      logger.info('The third evo from the random pkm match')
      return randomFinalEvo

  logger.info('Not evo match was found')
  return None

# ********* Add Pokemon Events Randomizer Start *********
def getRandomizedAddPokemonEvents(options: dict = None):
  logger.info('Starting logs for Initials Randomizer')
  randomizedList = []
  starters = {
    "fire": 0,
    "water": 0,
    "grass": 0,
  }

  for event in addPokemonEvents["values"]:
    isStarter = True if "hono" in event["label"] or "kusa" in event["label"] or "mizu" in event["label"] else False

    generator = generateRandomPaldeaPokemon

    if options["fullPokeDex"]:
      generator = generateRandomPokemon

    randomPokemon = None

    if isStarter and options["initials"]:
      loopCtrl = 0
      while (randomPokemon is None):
        randomPokemon = generator(options)

        if (randomPokemon["id"] in list(starters.values())):
          randomPokemon = None

        if (randomPokemon is None):
          continue

        if options["similarStats"] == True:
          if not hasSimilarStats(oldPkmDevName=event["pokeData"]["devId"], newPkmId=randomPokemon["id"]):
            randomPkmPersonal = getPokemonPersonalData(dexId=randomPokemon["id"])
            oldPkmPersonal = getPokemonPersonalData(dexId=event["pokeData"]["devId"])              
            checkedPkm = checkEvoStats(oldPkmPersonalData=oldPkmPersonal, newPkmPersonalData=randomPkmPersonal)

            if checkedPkm is not None:
              randomPokemon = checkedPkm
              continue

            if loopCtrl < MAX_SIMILIAR_STATS_TRIES:
              # To avoid infinite loop
              randomPokemon = None
              loopCtrl += 1

      event["pokeData"]["devId"] = randomPokemon["devName"]
      form, sex = getRandomForm(randomPokemon["id"], randomPokemon["forms"])
      event["pokeData"]["formId"] = form
      event["pokeData"]["sex"] = sex
      logger.info(f'Random pokemon generated: {randomPokemon["id"]} - {randomPokemon["devName"]} - {event["pokeData"]["formId"]}')

    if not isStarter and options["areasSpawnRandomized"]:
      loopCtrl = 0
      while (randomPokemon is None):
        randomPokemon = generator(options)

        if (randomPokemon is None):
          continue

        if options["similarStats"] == True:
          if not hasSimilarStats(oldPkmDevName=event["pokeData"]["devId"], newPkmId=randomPokemon["id"]):
            randomPkmPersonal = getPokemonPersonalData(dexId=randomPokemon["id"])
            oldPkmPersonal = getPokemonPersonalData(dexId=event["pokeData"]["devId"])              
            checkedPkm = checkEvoStats(oldPkmPersonalData=oldPkmPersonal, newPkmPersonalData=randomPkmPersonal)

            if checkedPkm is not None:
              randomPokemon = checkedPkm
              continue

            if loopCtrl < MAX_SIMILIAR_STATS_TRIES:
              # To avoid infinite loop
              randomPokemon = None
              loopCtrl += 1

      event["pokeData"]["devId"] = randomPokemon["devName"]
      form, sex = getRandomForm(randomPokemon["id"], randomPokemon["forms"])
      event["pokeData"]["formId"] = form
      event["pokeData"]["sex"] = sex
      logger.info(f'Random pokemon generated: {randomPokemon["id"]} - {randomPokemon["devName"]} - {event["pokeData"]["formId"]}')

    if isStarter:
      starterId = randomPokemon["id"] if randomPokemon is not None else event["pokeData"]["devId"]

      if "hono" in event["label"]:
        # Fire starter
        starters["fire"] = starterId

      if "kusa" in event["label"]:
        # Plant starter
        starters["grass"] = starterId

      if "mizu" in event["label"]:
        # Water starter
        starters["water"] = starterId
      
    if options["abilities"]:
      event["pokeData"]["tokusei"] = "RANDOM_123"

    if options["items"]:
      event["pokeData"]["item"] = generateRandomItem()["devName"]

    event["pokeData"]["rareType"] = "DEFAULT"

    randomizedList.append(event)

  logger.info('Closing logs for Initials Randomizer')
  return randomizedList, starters

# ********* Add Pokemon Events Randomizer End *********

# ********* Static Pokemon Events Randomizer Start *********
def getRandomizedStaticPokemonEvents(options: dict = None):
  logger.info('Starting logs for Statics Randomizer')
  randomizedList = []

  for event in fixedPokemonEvents["values"]:
    if options["areasSpawnRandomized"]:
      generator = generateRandomPaldeaPokemon

      if options["fullPokeDex"]:
        generator = generateRandomPokemon

      randomPokemon = None

      loopCtrl = 0
      while (randomPokemon is None):
        randomPokemon = generator(options)

        if (randomPokemon is None):
          continue

        if options["similarStats"] == True:
          if not hasSimilarStats(oldPkmDevName=event["pokeDataSymbol"]["devId"], newPkmId=randomPokemon["id"]):
            randomPkmPersonal = getPokemonPersonalData(dexId=randomPokemon["id"])
            oldPkmPersonal = getPokemonPersonalData(dexId=event["pokeDataSymbol"]["devId"])              
            checkedPkm = checkEvoStats(oldPkmPersonalData=oldPkmPersonal, newPkmPersonalData=randomPkmPersonal)

            if checkedPkm is not None:
              randomPokemon = checkedPkm
              continue

            if loopCtrl < MAX_SIMILIAR_STATS_TRIES:
              # To avoid infinite loop
              randomPokemon = None
              loopCtrl += 1

      event["pokeDataSymbol"]["devId"] = randomPokemon["devName"]
      form, sex = getRandomForm(randomPokemon["id"], randomPokemon["forms"])
      event["pokeDataSymbol"]["formId"] = form
      event["pokeDataSymbol"]["sex"] = sex
      logger.info(f'Random pokemon generated: {randomPokemon["id"]} - {randomPokemon["devName"]} - {event["pokeDataSymbol"]["formId"]}')

    if options["abilities"]:
      event["pokeDataSymbol"]["tokuseiIndex"] = "RANDOM_123"
    
    event["pokeDataSymbol"]["rareType"] = "DEFAULT"

    randomizedList.append(event)

  logger.info('Closing logs for Statics Randomizer')
  return randomizedList

# ********* Static Pokemon Events Randomizer End *********

# ********* Areas Randomizer Start *********
def getRandomizedArea(options: dict = None):
  logger.info('Starting logs for Areas Randomizer')
  randomizedAreaList = []

  for pokemon in pokemonData["values"]:
    if options["areasSpawnRandomized"]:
      pokemonGenerator = generateRandomPaldeaPokemon

      if options["fullPokeDex"] == True:
        pokemonGenerator = generateRandomPokemon

      randomPokemon = None

      loopCtrl = 0
      while (randomPokemon is None):
        randomPokemon = pokemonGenerator(options)

        if randomPokemon is None:
          continue

        if options["similarStats"] == True:
          if not hasSimilarStats(oldPkmDevName=pokemon["devid"], newPkmId=randomPokemon["id"]):
            randomPkmPersonal = getPokemonPersonalData(dexId=randomPokemon["id"])
            oldPkmPersonal = getPokemonPersonalData(dexId=pokemon["devid"])              
            checkedPkm = checkEvoStats(oldPkmPersonalData=oldPkmPersonal, newPkmPersonalData=randomPkmPersonal)

            if checkedPkm is not None:
              randomPokemon = checkedPkm
              continue

            if loopCtrl < MAX_SIMILIAR_STATS_TRIES:
              # To avoid infinite loop
              randomPokemon = None
              loopCtrl += 1

      pokemon["devid"] = randomPokemon["devName"]
      form, sex = getRandomForm(randomPokemon["id"], randomPokemon["forms"])
      pokemon["formno"] = form
      pokemon["sex"] = sex
      logger.info(f'Random pokemon generated: {randomPokemon["id"]} - {randomPokemon["devName"]} - {pokemon["formno"]}')
    
    if options["items"] == False:
      #  No randomized items
      randomizedAreaList.append(pokemon)
      continue

    randomItem = generateRandomItem()
    randomizedAreaList.append({
      **pokemon,
      "bringItem": {
        "itemID": randomItem["id"],
        "bringRate": 100
      }
    })
    logger.info(f'Random item: {randomItem["id"]} - {randomItem["devName"]}')

  logger.info('Closing logs for Areas Randomizer')
  return randomizedAreaList

# ********* Areas Randomizer End *********

# ********* Pokemon Randomizer End *********
def getRandomizedAbility(blacklist: list = []):
  randomizedAbility = None

  while (randomizedAbility is None or randomizedAbility in blacklist):
    rng = getRNG(maxValue=len(abilityList))
    randomizedAbility = abilityList[rng]

  return randomizedAbility

def getRandomizedTMList(default: list):
  maxTMList = len(default)
  randomizedTMList = []
  movesPool = tmList

  for item in range(0, maxTMList):
    randomizedTM = None

    if (len(randomizedTMList) == len(tmList)):
      movesPool = moveList

    while (randomizedTM is None or randomizedTM in randomizedTMList):
      rng = getRNG(maxValue=len(movesPool))
      randomizedTM = movesPool[rng]

    randomizedTMList.append(randomizedTM["id"])

  return randomizedTMList

def getRandomizedLearnset(defaultLearnset: list):
  randomizedLearnset = []
  alreadyUsedIds = []

  for defaultMove in defaultLearnset:
    moveId = None

    while (moveId is None or moveId in alreadyUsedIds):
      rngMoveId = getRNG(maxValue=len(moveList))
      randomMove = moveList[rngMoveId]

      moveId = randomMove["id"]

    randomizedLearnset.append({
      **defaultMove,
      "move": moveId
    })

  return randomizedLearnset

def getRandomizedPokemonList(options: dict = None):
  logger.info('Starting logs for Pokemon Personal Data Randomizer')

  randomizedPokemonList = []
  for pokemon in personalData["entry"]:

    if options["fullPokeDex"]:
      pokemon["is_present"] = True

    if not pokemon["is_present"]:
      randomizedPokemonList.append(pokemon)
      continue

    randomizedPokemon = {
      **pokemon
    }

    if (options["abilities"] == True):
      # Randomizing Abilities
      defaultAbilities = [randomizedPokemon["ability_1"], randomizedPokemon["ability_2"], randomizedPokemon["ability_3"]]
      randomizedPokemon["ability_1"] = getRandomizedAbility(blacklist=defaultAbilities)
      randomizedPokemon["ability_2"] = getRandomizedAbility(blacklist=defaultAbilities+[randomizedPokemon["ability_1"]])
      randomizedPokemon["ability_3"] = getRandomizedAbility(blacklist=defaultAbilities+[randomizedPokemon["ability_1"], randomizedPokemon["ability_2"]])

    if (options["tm"]):
      # Randomizing TM compatibility
      randomizedPokemon["tm_moves"] = getRandomizedTMList(default=randomizedPokemon["tm_moves"])

    if (options["learnset"]):
      # Randomizing Pool of moves the pokemon will learn by level
      randomizedPokemon["levelup_moves"] = getRandomizedLearnset(randomizedPokemon["levelup_moves"])

    randomizedPokemonList.append(randomizedPokemon)
    continue

  logger.info('Closing logs for Pokemon Personal Data Randomizer')
  return randomizedPokemonList

# ********* Pokemon Randomizer End *********

# ********* Trainers Randomizer Start *********
def getPerfectIvs():
  stats = ["hp", "atk", "def", "spAtk", "spDef", "agi"]
  rngLowerStat = getRNG(maxValue=len(stats))
  lowerStat = stats[rngLowerStat]

  talentValue = {
    "hp": 31,
    "atk": 31,
    "def": 31,
    "spAtk": 31,
    "spDef": 31,
    "agi": 31
  }

  talentValue[lowerStat] = 30

  return talentValue

def getCompetitiveEvs():
  stats = ["hp", "atk", "def", "spAtk", "spDef", "agi"]
  rngLowerStat = getRNG(maxValue=len(stats))

  EVsTotalValue = 510
  EVsMaxValue = 255

  effortValue = {
    "hp": 0,
    "atk": 0,
    "def": 0,
    "spAtk": 0,
    "spDef": 0,
    "agi": 0
  }

  return effortValue

def isShiny(rateValue: int):
  # rateValue based on 100
  # return 0 - Not Shiny
  # return 1 - Shiny

  rng = getRNG(maxValue=100, minValue=1)
  if rng <= rateValue:
    return 1

  return 0

def getNextEvolution(dexId: int = None, devName: str = None):
  if dexId == 0 or (dexId is None and devName is None) or devName == "DEV_NULL":
    return None

  pokemon = None

  if dexId is not None:
    pokemon = getPokemonPersonalData(dexId)

  if devName is not None:
    fromList = getPokemonDev(devName=devName)
    pokemon = getPokemonPersonalData(fromList["id"])
  
  if pokemon == None:
    return None

  if len(pokemon["evo_data"]) >= 1:
    evoDexId = getRNG(maxValue=len(pokemon["evo_data"]))
    pokemon = getPokemonPersonalData(dexId=pokemon["evo_data"][evoDexId]["species"])
  
  if pokemon == None:
    return None

  return getPokemonDev(pokemon["species"]["model"])

def getFinalEvolution(dexId: int = None, devName: str = None):
  if dexId == 0 or (dexId is None and devName is None) or devName == "DEV_NULL":
    return {"devName": "DEV_NULL", "id": 0}

  pokemon = None

  if dexId is not None:
    pokemon = getPokemonPersonalData(dexId)

  if devName is not None:
    fromList = getPokemonDev(devName=devName)
    pokemon = getPokemonPersonalData(fromList["id"])
  
  if pokemon == None:
    return None
  
  while len(pokemon["evo_data"]) != 0:
    evoDexId = 0
    if len(pokemon["evo_data"]) > 1:
      evoDexId = getRNG(maxValue=len(pokemon["evo_data"]))

    pokemon = getPokemonPersonalData(dexId=pokemon["evo_data"][evoDexId]["species"])
  
  if pokemon == None:
    return None

  return getPokemonDev(pokemon["species"]["model"])

def getTrainerTypeId(trainerTypeName: str):
  if "normal" in trainerTypeName: #Normal (duh)
    return 0

  if "kakutou" in trainerTypeName: #Fight
    return 1

  if "hikou" in trainerTypeName: #Fly
    return 2

  if "doku" in trainerTypeName: #Poison
    return 3

  if "jimen" in trainerTypeName: #Earth
    return 4

  if "iwa" in trainerTypeName: #Rock (still to confirm)
    return 5

  if "mushi" in trainerTypeName: #Bug
    return 6

  if "ghost" in trainerTypeName: #Ghost (duh x2)
    return 7

  if "hagane" in trainerTypeName: #Steel
    return 8

  if "hono" in trainerTypeName: #Fire
    return 9

  if "mizu" in trainerTypeName: #Water
    return 10

  if "kusa" in trainerTypeName: #Plant
    return 11

  if "denki" in trainerTypeName: #Electric
    return 12

  if "esper" in trainerTypeName: #Psiquic
    return 13

  if "koori" in trainerTypeName: #Ice
    return 14

  if "dragon" in trainerTypeName: #Dragon (duh x3)
    return 15

  if "aku" in trainerTypeName: #Dark
    return 16

  if "fairy" in trainerTypeName: #Fairy (duh x4)
    return 17

def isMonotypeTrainer(trainerTypeName: str):
  if "leader" in trainerTypeName: # Gym Leader
    return True
    
  if "e4_" in trainerTypeName: #Elite 4
    return True
    
  if "star_" in trainerTypeName and "_boss" in trainerTypeName: #Team Star Boss
    return True

  return False

def getMinMaxLv(trainerPokemon: dict):
  pokemonKeys = ["poke1","poke2","poke3","poke4","poke5","poke6"]

  maxLv = 0 # From min to max
  minLv = 100 # From max to min

  for pokeKey in pokemonKeys:
    pokeLv = trainerPokemon[pokeKey]["level"]

    if pokeLv != 0 and pokeLv < minLv:
      minLv = pokeLv

    if pokeLv > maxLv:
      maxLv = pokeLv

  return minLv, maxLv

def getRandomizedTrainersList(options: dict = None):
  logger.info('Starting logs for Trainers Randomizer')

  randomizedTrainersList = []
  pokemonKeys = ["poke1","poke2","poke3","poke4","poke5","poke6"]
  originalStarters = ["DEV_NEKO", "DEV_WANI", "DEV_KAMO"]
  
  shinyValues = ["NO_RARE", "RARE"]
  rateValue = options["trainerShiniesRate"]
  shiny = isShiny(rateValue=rateValue)

  rivalInitialShiny = shinyValues[shiny]

  for trainer in trainersData["values"]:
    randomizedTrainer = {
      **trainer
    }
    alreadyUsedId = []

    isRival = False
    rivalType = None
    rivalStage = None
    rivalStarterName = None
    rivalPokemon = None
    rivalParams = randomizedTrainer["trid"].split("_")

    if "rival_" in randomizedTrainer["trid"]:
      if len(rivalParams) == 3:
        isRival = True
        rivalType = getTrainerTypeId(rivalParams[2])
        if "multi" in rivalParams:
          rivalStage = rivalParams[1]
        else:
          rivalStage = int(rivalParams[1][1])

    if options["keepRivalInitial"] and isRival:
      if options["initials"]:
        # Get the initial from the json created
        with open('starters.json', 'r', encoding='utf-8-sig') as startersJson:
          randomStarters = json.load(startersJson)

          if rivalType == 9: #Fire
            rivalPokemon = getPokemonDev(dexId=randomStarters["grass"])

          if rivalType == 10: #Water
            rivalPokemon = getPokemonDev(dexId=randomStarters["fire"])

          if rivalType == 11: #Plant
            rivalPokemon = getPokemonDev(dexId=randomStarters["water"])
          
          rivalStarterName = rivalPokemon["devName"]
      else:
        if rivalType == 9: #Fire
          rivalStarterName = "DEV_NEKO1"

        if rivalType == 10: #Water
          rivalStarterName = "DEV_WANI1"

        if rivalType == 11: #Plant
          rivalStarterName = "DEV_KAMO1"

        rivalPokemon = getPokemonDev(devName=rivalStarterName)

      if rivalStage == 4:
        # Should evolve initial once
        rivalPokemon = getNextEvolution(devName=rivalStarterName)
        if rivalPokemon is None:
          rivalPokemon = getPokemonDev(devName=rivalStarterName)

      if (isinstance(rivalStage, int) and rivalStage >= 5) or rivalStage == "multi":
        # Initial should be on final evolution
        rivalPokemon = getFinalEvolution(devName=rivalStarterName)
        if rivalPokemon is None:
          rivalPokemon = getPokemonDev(devName=rivalStarterName)

    if options["trainerTeracristalize"]:
      randomizedTrainer["changeGem"] = True

    if options["forceFullTeam"]:
      minLv, maxLv = getMinMaxLv(trainerPokemon=randomizedTrainer)
      
      if minLv == maxLv:
        if (maxLv >= 5):
          lowLv = maxLv-2
          medLv = maxLv-1
        else:
          lowLv = maxLv
          medLv = maxLv
      else:
        lowLv = minLv
        medLv = math.floor((maxLv-minLv)/2)+lowLv

      pokemonLvl = {
        "poke1": {
          "level": lowLv
        },
        "poke2": {
          "level": lowLv
        },
        "poke3": {
          "level": lowLv
        },
        "poke4": {
          "level": medLv
        },
        "poke5": {
          "level": medLv
        },
        "poke6": {
          "level": maxLv
        }
      }

    for pokeKey in pokemonKeys:
      if (options["forceFullTeam"] == False and randomizedTrainer[pokeKey]["devId"] == "DEV_NULL"):
        continue

      if options["trainersRandomized"]:
        if options["keepRivalInitial"] and isRival:
          # Not randomize and get the starter instead
          if (randomizedTrainer[pokeKey]["devId"][:-1] in originalStarters):
            randomizedTrainer[pokeKey] = {
              **randomizedTrainer[pokeKey],
              "devId": rivalPokemon["devName"],
              "formId": 0,
              "ballId": "MONSUTAABOORU",
              "sex": "DEFAULT",
            }

            logger.info(f'Rival starter type {rivalParams[2]} changed for: {rivalPokemon["id"]} - {rivalPokemon["devName"]}')
            alreadyUsedId.append(rivalPokemon["id"])
        else:              
          pokemonGenerator = generateRandomPaldeaPokemon
          if options["fullPokeDex"]:
            pokemonGenerator = generateRandomPokemon

          randomPokemon = None

          loopCtrl = 0
          while (randomPokemon is None or randomPokemon["id"] in alreadyUsedId):               
            randomPokemon = pokemonGenerator(options)

            if (randomPokemon is None):
              continue

            if options["trainerSimilarStats"] == True:
              pokeDevName = randomizedTrainer[pokeKey]["devId"]
              if pokeDevName == "DEV_NULL":
                previousKey = pokemonKeys[pokemonKeys.index(pokeKey) - 1]
                pokeDevName = randomizedTrainer[previousKey]["devId"]

              if not hasSimilarStats(oldPkmDevName=pokeDevName, newPkmId=randomPokemon["id"]):
                randomPkmPersonal = getPokemonPersonalData(dexId=randomPokemon["id"])
                oldPkmPersonal = getPokemonPersonalData(dexId=pokeDevName)              
                checkedPkm = checkEvoStats(oldPkmPersonalData=oldPkmPersonal, newPkmPersonalData=randomPkmPersonal)

                if checkedPkm is not None:
                  randomPokemon = checkedPkm

                elif loopCtrl < MAX_SIMILIAR_STATS_TRIES:
                  # To avoid infinite loop
                  randomPokemon = None
                  loopCtrl += 1
                  continue

            if options["keepGymType"]:
              if isMonotypeTrainer(trainerTypeName=randomizedTrainer["trainerType"]):
                trainerTypeId = getTrainerTypeId(trainerTypeName=randomizedTrainer["trainerType"])
                randomPokemonPersonal = getPokemonPersonalData(randomPokemon["id"])
                
                type1 = randomPokemonPersonal["type_1"]
                type2 = randomPokemonPersonal["type_2"]

                if (trainerTypeId not in [type1, type2]):
                  # Randomize again if any type not match with the trainerType
                  randomPokemon = None

          alreadyUsedId.append(randomPokemon["id"])

          form, sex = getRandomForm(randomPokemon["id"], randomPokemon["forms"])

          randomizedTrainer[pokeKey] = {
            **randomizedTrainer[pokeKey],
            "devId": randomPokemon["devName"],
            "formId": form,
            "ballId": "MONSUTAABOORU",
            "sex": sex,
            "wazaType": "DEFAULT",
            "waza1": {
              "wazaId": "WAZA_NULL",
              "pointUp": 0
            },
            "waza2": {
              "wazaId": "WAZA_NULL",
              "pointUp": 0
            },
            "waza3": {
              "wazaId": "WAZA_NULL",
              "pointUp": 0
            },
            "waza4": {
              "wazaId": "WAZA_NULL",
              "pointUp": 0
            }
          }

          logger.info(f'Random pokemon generated: {randomPokemon["id"]} - {randomPokemon["devName"]} - {randomizedTrainer[pokeKey]["formId"]}')

      if options["forceFullTeam"]:
        randomizedTrainer[pokeKey]["level"] = pokemonLvl[pokeKey]["level"]

      if options["abilities"]:
        randomizedTrainer[pokeKey]["tokusei"] = "RANDOM_123"

      if options["trainersItems"]:
        randomItem = generateRandomItem()
        randomizedTrainer[pokeKey] = {
          **randomizedTrainer[pokeKey],
          "item": randomItem["devName"],
        }

      if options["competitivePkm"]:
        perfectIvs = getPerfectIvs()
        randomizedTrainer[pokeKey] = {
          **randomizedTrainer[pokeKey],
          "talentType": "VALUE",
          "talentValue": perfectIvs
        }
        randomizedTrainer["isStrong"] = True

      if options["trainerShiniesRate"] >= 0 and options["trainerShiniesRate"] <= 100:
        if options["keepRivalInitial"] and isRival:
          randomizedTrainer[pokeKey] = {
            **randomizedTrainer[pokeKey],
            "rareType": rivalInitialShiny
          }
        else:
          shinyValues = ["NO_RARE", "RARE"]

          rateValue = options["trainerShiniesRate"]

          shiny = isShiny(rateValue=rateValue)

          randomizedTrainer[pokeKey] = {
            **randomizedTrainer[pokeKey],
            "rareType": shinyValues[shiny]
          }

      if options["forceFinalEvolution"]:
        if options["finalEvolutionCap"] > 0 or options["finalEvolutionCap"] < 100:
          if randomizedTrainer[pokeKey]["level"] >= options["finalEvolutionCap"]:          
            finalEvo = getFinalEvolution(dexId=randomPokemon["id"])

            if finalEvo is None:
              randomizedTrainer[pokeKey] = {
                **randomizedTrainer[pokeKey],
                "devId": randomPokemon["devName"]
              }
            else:
              randomizedTrainer[pokeKey] = {
                **randomizedTrainer[pokeKey],
                "devId": finalEvo["devName"]
              }

    randomizedTrainersList.append(randomizedTrainer)

  logger.info('Closing logs for Trainers Randomizer')
  return randomizedTrainersList

# ********* Trainers Randomizer End *********