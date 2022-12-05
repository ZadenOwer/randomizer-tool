# randomizer.py
import json
import math
import random

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
paldeaDex = []
legendaryDex = []
paradoxDex = []

with (
  open('./src/jsons/pokedata_array.json', 'r', encoding='utf-8-sig') as pokedata_array_file,
  open('./src/jsons/personal_array.json', 'r', encoding='utf-8-sig') as personal_array_file,
  open('./src/jsons/pokemon_list.json', 'r', encoding='utf-8-sig') as pokemon_list_file,
  open('./src/jsons/dex.json', 'r', encoding='utf-8-sig') as dex_file,
  open('./src/jsons/ability_list.json', 'r', encoding='utf-8-sig') as ability_list_file,
  open('./src/jsons/tm_list.json', 'r', encoding='utf-8-sig') as tm_list_file,
  open('./src/jsons/move_list.json', 'r', encoding='utf-8-sig') as move_list_file,
):
  pokemonData = json.load(pokedata_array_file)
  personalData = json.load(personal_array_file)
  pokemonList = json.load(pokemon_list_file)
  abilityList = json.load(ability_list_file)
  tmList = json.load(tm_list_file)
  moveList = json.load(move_list_file)
  dex = json.load(dex_file)
  paldeaDex = dex["paldeaDex"]
  legendaryDex = dex["legendaryDex"]
  paradoxDex = dex["paradoxDex"]
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

# ********* Areas Randomizer Start *********

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

  try:
    generatedPokemon = next(pk for pk in pokemonList if pk["id"] == randomId)
    return generatedPokemon
  except:
    return None

def generateRandomItem():
  # itemTypesWeighted helps randomize the type of item that it will be used
  itemTypesWeighted = ['ITEMTYPE_NUTS', 'ITEMTYPE_NUTS', 'ITEMTYPE_NUTS', 'ITEMTYPE_NUTS', 'ITEMTYPE_NUTS', 'ITEMTYPE_NUTS', 'ITEMTYPE_NUTS', 'ITEMTYPE_NUTS', 'ITEMTYPE_NUTS', 'ITEMTYPE_NONE', 'ITEMTYPE_NONE', 'ITEMTYPE_NONE', 'ITEMTYPE_NONE', 'ITEMTYPE_NONE', 'ITEMTYPE_NONE', 'ITEMTYPE_NONE', 'ITEMTYPE_NONE', 'ITEMTYPE_NONE', 'ITEMTYPE_DRUG', 'ITEMTYPE_DRUG', 'ITEMTYPE_DRUG', 'ITEMTYPE_DRUG', 'ITEMTYPE_DRUG', 'ITEMTYPE_DRUG', 'ITEMTYPE_BALL', 'ITEMTYPE_BALL', 'ITEMTYPE_BALL', 'ITEMTYPE_BALL', 'ITEMTYPE_BALL', 'ITEMTYPE_BALL', 'ITEMTYPE_WAZA', 'ITEMTYPE_WAZA', 'ITEMTYPE_WAZA', 'ITEMTYPE_WAZA', 'ITEMTYPE_WAZA', 'ITEMTYPE_WAZA']
  bannedFieldPocket = [
    'FPOCKET_PICNIC' # Skip all the picnic items
  ]

  rngItemType = getRNG(maxValue=len(itemTypesWeighted))
  itemType = itemTypesWeighted[rngItemType]
  itemsByType = list(filter(
    lambda item: item["ItemType"] == itemType and item["FieldPocket"] not in bannedFieldPocket,
    itemData["values"]
  ))

  item = None
  while (item is None):
    rngItem = getRNG(maxValue=len(itemsByType))
    itemRaw = itemsByType[rngItem]
    item = next((item for item in itemList if item["id"] == itemRaw["Id"]), None)

  return item

def getRandomizedArea(options: dict = None):
  print('Randomizing Areas with options:', options)
  alreadyUsedId = []
  randomizedAreaList = []
  for pokemon in pokemonData["values"]:
    if (pokemon["bandtype"] == "BOSS"):
      randomizedAreaList.append(pokemon)
      continue

    randomPokemon = generateRandomPaldeaPokemon(options)

    try:
      while (randomPokemon is None or alreadyUsedId.index(randomPokemon["id"])):
        randomPokemon = generateRandomPaldeaPokemon(options)
    except:
      None

    alreadyUsedId.append(randomPokemon["id"])

    if (options is None or options["items"] is None or options["items"] == False):
      #  No randomized items
      randomizedAreaList.append({
        **pokemon,
        "devid": randomPokemon["devName"]
      })
      continue

    randomItem = generateRandomItem()
    randomizedAreaList.append({
      **pokemon,
      "devid": randomPokemon["devName"],
      "bringItem": {
        "itemID": randomItem["id"],
        "bringRate": 100
      }
    })
    continue

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
      "Move": moveId
    })

  return randomizedLearnset

def getRandomizedPokemonList(options: dict = None):
  print('Randomizing Pokemon with options:', options)
  randomizedPokemonList = []
  for pokemon in personalData["Table"]:

    if not pokemon["IsPresentInGame"]:
      randomizedPokemonList.append(pokemon)
      continue

    randomizedPokemon = {
      **pokemon
    }

    if (options["abilities"] == True):
      # Randomizing Abilities
      defaultAbilities = [randomizedPokemon["Ability1"], randomizedPokemon["Ability2"], randomizedPokemon["AbilityH"]]
      randomizedPokemon["Ability1"] = getRandomizedAbility(blacklist=defaultAbilities)
      randomizedPokemon["Ability2"] = getRandomizedAbility(blacklist=defaultAbilities+[randomizedPokemon["Ability1"]])
      randomizedPokemon["AbilityH"] = getRandomizedAbility(blacklist=defaultAbilities+[randomizedPokemon["Ability1"], randomizedPokemon["Ability2"]])

    if (options["tm"]):
      # Randomizing TM compatibility
      randomizedPokemon["TechnicalMachine"] = getRandomizedTMList(default=randomizedPokemon["TechnicalMachine"])

    if (options["learnset"]):
      # Randomizing Pool of moves the pokemon will learn by level
      randomizedPokemon["Learnset"] = getRandomizedLearnset(randomizedPokemon["Learnset"])

    randomizedPokemonList.append(randomizedPokemon)
    continue

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

def getPokemonPersonalData(dexId: int):
  return next(pokemon for pokemon in personalData["Table"] if pokemon["Info"]["DexIndexNational"] == dexId)

def getPokemonDevName(dexId: int):
  return next(pokemon for pokemon in pokemonList if pokemon["id"] == dexId)["devName"]

def getFinalEvolution(dexId: int):
  if dexId == 0:
    return "DEV_NULL"

  try:
    pokemon = getPokemonPersonalData(dexId)
    
    while len(pokemon["Evolutions"]) != 0:
      evoDexId = 0
      if len(pokemon["Evolutions"]) > 1:
        evoDexId = getRNG(maxValue=len(pokemon["Evolutions"]))

      pokemon = getPokemonPersonalData(dexId=pokemon["Evolutions"][evoDexId]["Species"])

    return getPokemonDevName(pokemon["Info"]["DexIndexNational"])
  except:
    return "DEV_NULL"

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
  print('Randomizing Trainers with options:', options)
  randomizedTrainersList = []
  alreadyUsedId = []
  pokemonKeys = ["poke1","poke2","poke3","poke4","poke5","poke6"]

  for trainer in trainersData["values"]:
    randomizedTrainer = {
      **trainer
    }

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
      if (not options["forceFullTeam"] and randomizedTrainer[pokeKey] == "DEV_NULL"):
        continue

      randomPokemon = generateRandomPaldeaPokemon(options)
      randomPokemonPersonal = getPokemonPersonalData(randomPokemon["id"])

      try:
        while (randomPokemon is None or alreadyUsedId.index(randomPokemon["id"])):
          randomPokemon = generateRandomPaldeaPokemon(options)

          if options["keepGymType"]:
            if isMonotypeTrainer(trainerTypeName=randomizedTrainer["trainerType"]):
              trainerTypeId = getTrainerTypeId(trainerTypeName=randomizedTrainer["trainerType"])
              type1 = randomPokemonPersonal["Type1"]
              type2 = randomPokemonPersonal["Type2"]

              if (trainerTypeId not in [type1, type2]):
                # Randomize again if any type not match with the trainerType
                randomPokemon = generateRandomPaldeaPokemon(options)
      except:
        None

      randomizedTrainer[pokeKey] = {
        **randomizedTrainer[pokeKey],
        "devId": randomPokemon["devName"],
        "formId": 0,
        "ballId": "MONSUTAABOORU",
      }

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
        shinyValues = ["NO_RARE", "RARE"]

        rateValue = options["trainerShiniesRate"]

        shiny = isShiny(rateValue=rateValue)

        randomizedTrainer[pokeKey] = {
          **randomizedTrainer[pokeKey],
          "rareType": shinyValues[shiny]
        }

      if options["forceFinalEvolution"]:
        if options["finalEvolutionCap"] > 0 or options["finalEvolutionCap"] < 100:
          if randomizedTrainer[pokeKey]["level"] < options["finalEvolutionCap"]:          
            finalEvoName = getFinalEvolution(dexId=randomPokemon["id"])

            randomizedTrainer[pokeKey] = {
              **randomizedTrainer[pokeKey],
              "devId": finalEvoName
            }

    randomizedTrainersList.append(randomizedTrainer)

  return randomizedTrainersList

# ********* Trainers Randomizer End *********