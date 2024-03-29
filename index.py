# index.py
import os
import shutil
import json

# Env Vars
os.environ["VERSION"] = "1.1.8"

os.makedirs('./logs', exist_ok=True) # Logs folder created if not exists yet

from src.scripts.randomizer.pokemon import PokemonRandomizer
from src.scripts.randomizer.trainers import TrainersRandomizer
from src.scripts.randomizer.spawns import SpawnsRandomizer
from src.scripts.randomizer.items import ItemRandomizer

from src.scripts import flatc as FlatC
from src.scripts import frame as WindowFrame

from src.scripts.logger import setup_custom_logger

logger = setup_custom_logger(os.environ.get('VERSION'))
logger.info('STARTING LOGS')

staticData = {}

with (
  # Pokemon Data Imports
  open('./src/jsons/pokedata_array.json', 'r', encoding='utf-8-sig') as pokedata_array_file,
  open('./src/jsons/personal_array.json', 'r', encoding='utf-8-sig') as personal_array_file,
  open('./src/jsons/pokemon_list.json', 'r', encoding='utf-8-sig') as pokemon_list_file,
  open('./src/jsons/dex.json', 'r', encoding='utf-8-sig') as dex_file,
  open('./src/jsons/ability_list.json', 'r', encoding='utf-8-sig') as ability_list_file,
  open('./src/jsons/tm_list.json', 'r', encoding='utf-8-sig') as tm_list_file,
  open('./src/jsons/move_list.json', 'r', encoding='utf-8-sig') as move_list_file,
  open('./src/jsons/eventAddPokemon_array.json', 'r', encoding='utf-8-sig') as add_pokemon_events_file,
  open('./src/jsons/fixed_symbol_table_array.json', 'r', encoding='utf-8-sig') as fixed_pokemon_events_file,

  # Item Data Imports
  open('./src/jsons/itemdata_array.json', 'r', encoding='utf-8-sig') as itemdata_array_file,
  open('./src/jsons/hiddenItemDataTable_array.json', 'r', encoding='utf-8-sig') as hiddenitemdata_table_file,
  open('./src/jsons/item_list.json', 'r', encoding='utf-8-sig') as item_list_file,

  # Trainers Data Imports
  open('./src/jsons/trdata_array.json', 'r', encoding='utf-8-sig') as trainersdata_array_file
):
  staticData["pokedata_array_file"] = json.load(pokedata_array_file)
  staticData["personal_array_file"] = json.load(personal_array_file)
  staticData["pokemon_list_file"] = json.load(pokemon_list_file)
  staticData["ability_list_file"] = json.load(ability_list_file)
  staticData["tm_list_file"] = json.load(tm_list_file)
  staticData["move_list_file"] = json.load(move_list_file)
  dex = json.load(dex_file)
  staticData["pokeDex"] = dex["pokeDex"]
  staticData["paldeaDex"] = dex["paldeaDex"]
  staticData["legendaryDex"] = dex["legendaryDex"]
  staticData["paradoxDex"] = dex["paradoxDex"]
  staticData["add_pokemon_events_file"] = json.load(add_pokemon_events_file)
  staticData["fixed_pokemon_events_file"] = json.load(fixed_pokemon_events_file)
  
  staticData["itemdata_array_file"] = json.load(itemdata_array_file)
  staticData["item_list_file"] = json.load(item_list_file)
  staticData["hidden_item_list_file"] = json.load(hiddenitemdata_table_file)
  
  staticData["trainersdata_array_file"] = json.load(trainersdata_array_file)

# Create the window
optionsValues = {
  "keepFiles": False,
  "fullPokeDex": False,
  "initials": False,
  "legendaries": False,
  "paradox": True,
  "similarStats": True,

  ### Areas Options Start ###
  "areasSpawnRandomized": True,
  "items": True,
  ### Areas Options End ###

  ### Pokemon Options Start ###
  "abilities": True,
  "keepAbilities": True,
  "equalizedCatchRate": False,
  "equalizedCatchRateValue": 0,
  "tm": False,
  "keepTM": False,
  "learnset": False,
  "keepLearnset": False,
  "movePower": False,
  "moveType": False,
  "instantHatchEgg": False,
  "types": False,
  "keepTypes": False,
  "randomBaseStats": False,
  "evolutions": False,
  "keepEvoStage": False,
  "evoSameStats": False,
  "legendaryEvo": False,
  "paradoxEvo": False,
  "evoGrowthRate": False,
  "evoType": False,
  ### Pokemon Options End ###

  ### Items Options End ###
  "hiddenItems": True,
  ### Items Options End ###

  ### Trainers Options Start ###
  "trainersRandomized": False,
  "trainerSimilarStats": True,
  "trainerTeracristalize": False,
  "trainerLegendaries": False,
  "trainerParadox": True,
  "forceFullTeam": False,
  "keepRivalInitial": True,
  "keepGymType": False,
  "trainersItems": False,
  "competitivePkm": False,
  "trainerShiniesRate": 0,
  "forceFinalEvolution": False,
  "finalEvolutionCap": 35
  ### Trainers Options End ###
}

window = WindowFrame.getWindowFrame(optionsValues)

# Create an event loop
while True:
  # Start the window of the program 
  event, values = window.read()

  if event == WindowFrame.ON_CLOSE:
    # End program if user closes window
    logger.info('CLOSING LOGS')
    break

  if event == 'spawnsStepButton':
    WindowFrame.changeStep(window, 'spawns')

  if event == 'pokemonStepButton':
    WindowFrame.changeStep(window, 'pokemon')

  if event == 'itemsStepButton':
    WindowFrame.changeStep(window, 'fieldItems')

  if event == 'trainerStepButton':
    WindowFrame.changeStep(window, 'trainers')

  if event == 'finalStepButton':
    WindowFrame.changeStep(window, 'finalStep')

  if event == 'randomizeButton':
    # Serializing options
    WindowFrame.toggleLayoutButtons()
    serializedGlobalOptions = {
      "keepFiles": False if ("keepFiles" not in values.keys() or values["keepFiles"] is None or values["keepFiles"] == False) else True,
      "fullPokeDex": False if ("fullPokeDex" not in values.keys() or values["fullPokeDex"] is None or values["fullPokeDex"] == False) else True,
      "initials": False if ("initials" not in values.keys() or values["initials"] is None or values["initials"] == False) else True,
      "abilities": False if ("abilities" not in values.keys() or values["abilities"] is None or values["abilities"] == False) else True,
      "legendaries": False if ("legendaries" not in values.keys() or values["legendaries"] is None or values["legendaries"] == False) else True,
      "paradox": False if ("paradox" not in values.keys() or values["paradox"] is None or values["paradox"] == False) else True,
      "similarStats": False if ("similarStats" not in values.keys() or values["similarStats"] is None or values["similarStats"] == False) else True,
      "hiddenItems": False if ("hiddenItems" not in values.keys() or values["hiddenItems"] is None or values["hiddenItems"] == False) else True,
    }

    serializedAreaOptions = {
      "areasSpawnRandomized": False if ("areasSpawnRandomized" not in values.keys() or values["areasSpawnRandomized"] is None or values["areasSpawnRandomized"] == False) else True,
      "items": False if ("items" not in values.keys() or values["items"] is None or values["items"] == False) else True,
      **serializedGlobalOptions
    }

    try:
      equalizedCatchRateValue = int(values["equalizedCatchRateValue"])
    except:
      equalizedCatchRateValue = "NOT VALID"

    serializedPokemonOptions = {
      "keepAbilities": False if ("keepAbilities" not in values.keys() or values["keepAbilities"] is None or values["keepAbilities"] == False) else True,
      "equalizedCatchRate": False if ("equalizedCatchRate" not in values.keys() or values["equalizedCatchRate"] is None or values["equalizedCatchRate"] == False) else True,
      "equalizedCatchRateValue": equalizedCatchRateValue,
      "tm": False if ("tm" not in values.keys() or values["tm"] is None or values["tm"] == False) else True,
      "keepTM": False if ("keepTM" not in values.keys() or values["keepTM"] is None or values["keepTM"] == False) else True,
      "learnset": False if ("learnset" not in values.keys() or values["learnset"] is None or values["learnset"] == False) else True,
      "keepLearnset": False if ("keepLearnset" not in values.keys() or values["keepLearnset"] is None or values["keepLearnset"] == False) else True,
      "movePower": False if ("movePower" not in values.keys() or values["movePower"] is None or values["movePower"] == False) else True,
      "moveType": False if ("moveType" not in values.keys() or values["moveType"] is None or values["moveType"] == False) else True,
      "instantHatchEgg": False if ("instantHatchEgg" not in values.keys() or values["instantHatchEgg"] is None or values["instantHatchEgg"] == False) else True,
      "types": False if ("types" not in values.keys() or values["types"] is None or values["types"] == False) else True,
      "keepTypes": False if ("keepTypes" not in values.keys() or values["keepTypes"] is None or values["keepTypes"] == False) else True,
      "randomBaseStats": False if ("randomBaseStats" not in values.keys() or values["randomBaseStats"] is None or values["randomBaseStats"] == False) else True,
      "evolutions": False if ("evolutions" not in values.keys() or values["evolutions"] is None or values["evolutions"] == False) else True,
      "keepEvoStage": False if ("keepEvoStage" not in values.keys() or values["keepEvoStage"] is None or values["keepEvoStage"] == False) else True,
      "evoSameStats": False if ("evoSameStats" not in values.keys() or values["evoSameStats"] is None or values["evoSameStats"] == False) else True,
      "evoGrowthRate": False if ("evoGrowthRate" not in values.keys() or values["evoGrowthRate"] is None or values["evoGrowthRate"] == False) else True,
      "evoType": False if ("evoType" not in values.keys() or values["evoType"] is None or values["evoType"] == False) else True,
      "legendaryEvo": False if ("legendaryEvo" not in values.keys() or values["legendaryEvo"] is None or values["legendaryEvo"] == False) else True,
      "paradoxEvo": False if ("paradoxEvo" not in values.keys() or values["paradoxEvo"] is None or values["paradoxEvo"] == False) else True,
      **serializedGlobalOptions
    }

    try:
      trainerShiniesRate = int(values["trainerShiniesRate"])
    except:
      trainerShiniesRate = 0

    try:
      finalEvolutionCap = int(values["finalEvolutionCap"])
    except:
      finalEvolutionCap = 0

    serializedTrainersOptions = {
      "trainersRandomized": False if ("trainersRandomized" not in values.keys() or values["trainersRandomized"] is None or values["trainersRandomized"] == False) else True,
      "trainerSimilarStats": False if ("trainerSimilarStats" not in values.keys() or values["trainerSimilarStats"] is None or values["trainerSimilarStats"] == False) else True,
      "trainerTeracristalize": False if ("trainerTeracristalize" not in values.keys() or values["trainerTeracristalize"] is None or values["trainerTeracristalize"] == False) else True,
      "trainerLegendaries": False if ("trainerLegendaries" not in values.keys() or values["trainerLegendaries"] is None or values["trainerLegendaries"] == False) else True,
      "trainerParadox": False if ("trainerParadox" not in values.keys() or values["trainerParadox"] is None or values["trainerParadox"] == False) else True,
      "forceFullTeam": False if ("forceFullTeam" not in values.keys() or values["forceFullTeam"] is None or values["forceFullTeam"] == False) else True,
      "keepRivalInitial": False if ("keepRivalInitial" not in values.keys() or values["keepRivalInitial"] is None or values["keepRivalInitial"] == False) else True,
      "keepGymType": False if ("keepGymType" not in values.keys() or values["keepGymType"] is None or values["keepGymType"] == False) else True,
      "trainersItems": False if ("trainersItems" not in values.keys() or values["trainersItems"] is None or values["trainersItems"] == False) else True,
      "competitivePkm": False if ("competitivePkm" not in values.keys() or values["competitivePkm"] is None or values["competitivePkm"] == False) else True,
      "trainerShiniesRate": trainerShiniesRate,
      "forceFinalEvolution": False if ("forceFinalEvolution" not in values.keys() or values["forceFinalEvolution"] is None or values["forceFinalEvolution"] == False) else True,
      "finalEvolutionCap": finalEvolutionCap,
      **serializedGlobalOptions
    }

    logger.info(f'Areas Options: {serializedAreaOptions}')
    logger.info(f'Pokemon Options: {serializedPokemonOptions}')
    logger.info(f'Trainers Options: {serializedTrainersOptions}')
    # Ending serializing options

    logger.info('Starting randomizer...')

    # Files Names
    hiddenItemDataFileName = 'hiddenItemDataTable_array'
    addPokemonEventsFileName = 'eventAddPokemon_array'
    staticPokemonEventsFileName = 'fixed_symbol_table_array'
    personalFileName = 'personal_array'
    pokedataFileName = 'pokedata_array'
    trainersFileName = 'trdata_array'

    fileNames = {
      "addPokemonEvents": addPokemonEventsFileName,
      "staticPokemonEvents": staticPokemonEventsFileName,
      "pokedata": pokedataFileName,
      "personal": personalFileName,
      "trainers": trainersFileName,
      "hiddenItemData": hiddenItemDataFileName
    }

    spawnsRandomizer = SpawnsRandomizer(data=staticData, options=serializedAreaOptions)
    pokemonRandomizer = PokemonRandomizer(data=staticData, options=serializedPokemonOptions)
    trainersRandomizer = TrainersRandomizer(data=staticData, options=serializedTrainersOptions)
    itemsRandomizer = ItemRandomizer(data=staticData)

    spawnsRandomizer.addEventsProgress = 0
    spawnsRandomizer.staticEventsProgress = 0
    spawnsRandomizer.areaProgress = 0

    pokemonRandomizer.pokemonProgress = 0
    
    trainersRandomizer.trainerProgress = 0

    itemsRandomizer.fieldItemsProgress = 0

    logger.info('Randomizing Field Items...')
    hiddenItemDataRandomized = itemsRandomizer.getRandomizedHiddenItemData(options=serializedGlobalOptions) # Randomize the hidden items data
    jsonArrayFile = open(f'{fileNames["hiddenItemData"]}.json', 'w')
    jsonArrayFile.write(json.dumps({"values": hiddenItemDataRandomized}))
    jsonArrayFile.close()
    logger.info('Field Items randomized!')

    logger.info('Randomizing Trade Events...')
    addEventsRandomized, starters = spawnsRandomizer.getRandomizedAddPokemonEvents(options=serializedAreaOptions) # Randomize the add pokemon events (such as initials)
    jsonArrayFile = open(f'{fileNames["addPokemonEvents"]}.json', 'w')
    jsonArrayFile.write(json.dumps({"values": addEventsRandomized}))
    jsonArrayFile.close()
    logger.info('Trade Events randomized!')

    if serializedGlobalOptions["initials"]:
      logger.info('Randomizing Starters...')
      jsonArrayFile = open('starters.json', 'w')
      jsonArrayFile.write(json.dumps(starters))
      jsonArrayFile.close()
      logger.info('Starters randomized!')

    logger.info('Randomizing Static Events...')
    staticEventsRandomized = spawnsRandomizer.getRandomizedStaticPokemonEvents(options=serializedAreaOptions) # Randomize the static pokemon events
    jsonArrayFile = open(f'{fileNames["staticPokemonEvents"]}.json', 'w')
    jsonArrayFile.write(json.dumps({"values": staticEventsRandomized}))
    jsonArrayFile.close()
    logger.info('Static Events randomized!')

    logger.info('Randomizing Spawning Areas...')
    areaRandomized = spawnsRandomizer.getRandomizedArea(options=serializedAreaOptions)  # Randomize the pokemon that spawns each areas
    jsonArrayFile = open(f'{fileNames["pokedata"]}.json', 'w')
    jsonArrayFile.write(json.dumps({"values": areaRandomized}))
    jsonArrayFile.close()
    logger.info('Spawning Areas randomized!')

    logger.info('Randomizing Pokemon Personal Data...')
    pokemonRandomize = pokemonRandomizer.getRandomizedPokemonList(options=serializedPokemonOptions) # Randomize each pokemon individually
    jsonArrayFile = open(f'{fileNames["personal"]}.json', 'w')
    jsonArrayFile.write(json.dumps({"entry": pokemonRandomize}))
    jsonArrayFile.close()
    logger.info('Personal Data randomized!')

    logger.info('Randomizing Trainers...')
    trainersRandomize = trainersRandomizer.getRandomizedTrainersList(options=serializedTrainersOptions) # Randomize each trainer team and values
    jsonArrayFile = open(f'{fileNames["trainers"]}.json', 'w')
    jsonArrayFile.write(json.dumps({"values": trainersRandomize}))
    jsonArrayFile.close()
    logger.info('Trainers randomized!')

    logger.info('Generating binaries...')
    
    hiddenItemsDataResult = FlatC.generateBinary(schemaPath = f'./src/statics/{fileNames["hiddenItemData"]}.bfbs', jsonPath = f'./{fileNames["hiddenItemData"]}.json')  # Generates the Randomized Hidden Items Data binary
    if hiddenItemsDataResult.stderr != b'':
      logger.error(f'Error creating binary for Add Events: {hiddenItemsDataResult.stderr}')
      continue

    addEventsResult = FlatC.generateBinary(schemaPath = f'./src/statics/{fileNames["addPokemonEvents"]}.bfbs', jsonPath = f'./{fileNames["addPokemonEvents"]}.json')  # Generates the Randomized Add pokemon events binary
    if addEventsResult.stderr != b'':
      logger.error(f'Error creating binary for Add Events: {addEventsResult.stderr}')
      continue

    staticEventsResult = FlatC.generateBinary(schemaPath = f'./src/statics/{fileNames["staticPokemonEvents"]}.bfbs', jsonPath = f'./{fileNames["staticPokemonEvents"]}.json')  # Generates the Randomized Static pokemon events binary
    if staticEventsResult.stderr != b'':
      logger.error(f'Error creating binary for Static Events: {addEventsResult.stderr}')
      continue

    areaRandomizeResult = FlatC.generateBinary(schemaPath = f'./src/statics/{fileNames["pokedata"]}.bfbs', jsonPath = f'./{fileNames["pokedata"]}.json')  # Generates the Randomized Areas binary
    if areaRandomizeResult.stderr != b'':
      logger.error(f'Error creating binary for Areas: {addEventsResult.stderr}')
      continue

    personalDataRandomizeResult = FlatC.generateBinary(schemaPath = f'./src/statics/{fileNames["personal"]}.bfbs', jsonPath = f'./{fileNames["personal"]}.json')  # Generates the Randomized Areas binary
    if personalDataRandomizeResult.stderr != b'':
      logger.error(f'Error creating binary for Personal Data: {addEventsResult.stderr}')
      continue

    trainerRandomizeResult = FlatC.generateBinary(schemaPath = f'./src/statics/{fileNames["trainers"]}.bfbs', jsonPath = f'./{fileNames["trainers"]}.json')  # Generates the Randomized Trainers binary
    if trainerRandomizeResult.stderr != b'':
      logger.error(f'Error creating binary for Trainers: {addEventsResult.stderr}')
      continue

    logger.info('Binaries created!')

    # Files Paths
    addPokemonEventsPath = './static/world/data/event/event_add_pokemon/eventAddPokemon'
    staticPokemonEventsPath = './static/world/data/field/fixed_symbol/fixed_symbol_table'
    pokedataPath = './static/world/data/encount/pokedata/pokedata'
    personalDataPath = './static/avalon/data'
    trainerPath = './static/world/data/trainer/trdata'
    hiddenItemDataPath = './static/world/data/item/hiddenItemDataTable'

    paths = {
      "addPokemonEvents": addPokemonEventsPath,
      "staticPokemonEvents": staticPokemonEventsPath,
      "pokedata": pokedataPath,
      "personal": personalDataPath,
      "trainers": trainerPath,
      "hiddenItemData": hiddenItemDataPath
    }

    for pathName in paths:
      os.makedirs(f'{paths[pathName]}/')

    for fileName in fileNames:
      shutil.copy(f'./src/statics/{fileNames[fileName]}.bfbs', f'{paths[fileName]}/{fileNames[fileName]}.bfbs')

      if serializedGlobalOptions["keepFiles"]:
        shutil.copy(f'./{fileNames[fileName]}.bin', f'{paths[fileName]}/{fileNames[fileName]}.bin')
      else:
        os.replace(f'./{fileNames[fileName]}.bin', f'{paths[fileName]}/{fileNames[fileName]}.bin')
        os.remove(f'./{fileNames[fileName]}.json')  
      
    shutil.make_archive('randomized_pokemon', 'zip', './static')
    logger.info('ZIP created!')
    logger.info('Randomizing finished!')
    WindowFrame.updateProgress(100, title='COMPLETED')
    WindowFrame.toggleLayoutButtons()
    shutil.rmtree('./static')

window.close()