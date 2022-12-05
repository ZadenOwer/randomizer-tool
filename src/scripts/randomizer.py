# randomizer.py
import json
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

# ********* Areas Randomizer Start *********

def generateRandomPaldeaPokemon(options: dict = None):
  rng = random.randrange(start=0, stop=len(paldeaDex), step=1)
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

  rngItemType = random.randrange(start=0, stop=len(itemTypesWeighted), step=1)
  itemType = itemTypesWeighted[rngItemType]
  itemsByType = list(filter(
    lambda item: item["ItemType"] == itemType and item["FieldPocket"] not in bannedFieldPocket,
    itemData["values"]
  ))

  item = None
  while (item is None):
    rngItem = random.randrange(start=0, stop=len(itemsByType), step=1)
    itemRaw = itemsByType[rngItem]
    item = next((item for item in itemList if item["id"] == itemRaw["Id"]), None)

  return item["id"]

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
        "itemID": randomItem,
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
    rng = random.randrange(start=0, stop=len(abilityList), step=1)
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
      rng = random.randrange(start=0, stop=len(movesPool), step=1)
      randomizedTM = movesPool[rng]

    randomizedTMList.append(randomizedTM["id"])

  return randomizedTMList

def getRandomizedLearnset(defaultLearnset: list):
  randomizedLearnset = []
  alreadyUsedIds = []

  for defaultMove in defaultLearnset:
    moveId = None

    while (moveId is None or moveId in alreadyUsedIds):
      rngMoveId = random.randrange(start=0, stop=len(moveList), step=1)
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
