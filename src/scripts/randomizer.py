# randomizer.py
import json
import random

# Starting Pokemon Data Imports
pokemonData = {
  "values": []
}
pokemonList = []
paldeaDex = []
legendaryDex = []
paradoxDex = []

with (
  open('./src/jsons/pokedata_array.json', 'r', encoding='utf-8-sig') as pokedata_array_file,
  open('./src/jsons/pokemon_list.json', 'r', encoding='utf-8-sig') as pokemon_list_file,
  open('./src/jsons/dex.json', 'r', encoding='utf-8-sig') as dex_file,
):

  pokemonData = json.load(pokedata_array_file)
  pokemonList = json.load(pokemon_list_file)
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
  itemsByType = filter(
    lambda item: item["ItemType"] == itemType and item["FieldPocket"] not in bannedFieldPocket,
    itemData["values"]
  )

  try:
    item = None
    while (item is None):
      rngItem = random.randrange(start=0, stop=len(itemsByType), step=1)
      itemRaw = itemsByType[rngItem]
      item = next(item for item in itemList if item["id"] == itemRaw["id"])

  except:
    return "ITEMID_NONE"

def getRandomizedList(options: dict = None):
  print('Randomizing with options:', options)
  alreadyUsedId = []
  randomizedList = []
  for pokemon in pokemonData["values"]:
    if (pokemon["bandtype"] == "BOSS"):
      randomizedList.append(pokemon)
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
      randomizedList.append({
        **pokemon,
        "devid": randomPokemon["devName"]
      })
      continue

    randomItem = generateRandomItem()
    randomizedList.append({
      **pokemon,
      "devid": randomPokemon["devName"],
      "bringItem": {
        "itemID": randomItem,
        "bringRate": 100
      }
    })
    continue

  return randomizedList
