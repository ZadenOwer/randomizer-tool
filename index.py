# index.py
import os
import shutil
import json

from src.scripts import randomizer as Randomizer
from src.scripts import flatc as FlatC
from src.scripts import frame as WindowFrame

# Env Vars
os.environ["VERSION"] = "1.0.6"

# Create the window
optionsValues = {
  "keepFiles": False,
  "fullPokeDex": False,
  "initials": False,
  "legendaries": True,
  "paradox": True,

  ### Areas Options Start ###
  "areasSpawnRandomized": True,
  "items": True,
  ### Areas Options End ###

  ### Pokemon Options Start ###
  "abilities": True,
  "tm": False,
  "learnset": False,
  ### Pokemon Options End ###

  ### Trainers Options Start ###
  "trainersRandomized": True,
  "trainerTeracristalize": True,
  "forceFullTeam": False,
  "keepGymType": False,
  "trainersItems": False,
  "competitivePkm": False,
  "trainerShiniesRate": 0,
  "forceFinalEvolution": False,
  "finalEvolutionCap": 35
  ### Trainers Options End ###
}

window = WindowFrame.getWindowFrame(optionsValues)

print('Opening window...')
# Create an event loop
while True:
  # Start the window of the program 
  event, values = window.read()

  if event == WindowFrame.ON_CLOSE:
    # End program if user closes window
    print('Closing window...')
    break

  if event == 'Step 1':
    WindowFrame.changeStep(window, 'step1')

  if event == 'Step 2':
    WindowFrame.changeStep(window, 'step2')

  if event == 'Step 3':
    WindowFrame.changeStep(window, 'step3')

  if event == 'Step 4':
    WindowFrame.changeStep(window, 'step4')

  if event == 'Randomize!':
    # Serializing options

    serializedGlobalOptions = {
      "keepFiles": False if ("keepFiles" not in values.keys() or values["keepFiles"] is None or values["keepFiles"] == False) else True,
      "fullPokeDex": False if ("fullPokeDex" not in values.keys() or values["fullPokeDex"] is None or values["fullPokeDex"] == False) else True,
      "initials": False if ("initials" not in values.keys() or values["initials"] is None or values["initials"] == False) else True,
      "abilities": False if ("abilities" not in values.keys() or values["abilities"] is None or values["abilities"] == False) else True,
      "legendaries": False if ("legendaries" not in values.keys() or values["legendaries"] is None or values["legendaries"] == False) else True,
      "paradox": False if ("paradox" not in values.keys() or values["paradox"] is None or values["paradox"] == False) else True,
    }

    serializedAreaOptions = {
      "areasSpawnRandomized": False if ("areasSpawnRandomized" not in values.keys() or values["areasSpawnRandomized"] is None or values["areasSpawnRandomized"] == False) else True,
      "items": False if ("items" not in values.keys() or values["items"] is None or values["items"] == False) else True,
      **serializedGlobalOptions
    }

    serializedPokemonOptions = {
      "tm": False if ("tm" not in values.keys() or values["tm"] is None or values["tm"] == False) else True,
      "learnset": False if ("learnset" not in values.keys() or values["learnset"] is None or values["learnset"] == False) else True,
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
      "trainerTeracristalize": False if ("trainerTeracristalize" not in values.keys() or values["trainerTeracristalize"] is None or values["trainerTeracristalize"] == False) else True,
      "forceFullTeam": False if ("forceFullTeam" not in values.keys() or values["forceFullTeam"] is None or values["forceFullTeam"] == False) else True,
      "keepGymType": False if ("keepGymType" not in values.keys() or values["keepGymType"] is None or values["keepGymType"] == False) else True,
      "trainersItems": False if ("trainersItems" not in values.keys() or values["trainersItems"] is None or values["trainersItems"] == False) else True,
      "competitivePkm": False if ("competitivePkm" not in values.keys() or values["competitivePkm"] is None or values["competitivePkm"] == False) else True,
      "trainerShiniesRate": trainerShiniesRate,
      "forceFinalEvolution": False if ("forceFinalEvolution" not in values.keys() or values["forceFinalEvolution"] is None or values["forceFinalEvolution"] == False) else True,
      "finalEvolutionCap": finalEvolutionCap,
      **serializedGlobalOptions
    }

    print('Area Options', serializedAreaOptions)
    print('Pokemon Options', serializedPokemonOptions)
    # Ending serializing options

    print('Starting randomizer...')

    # Files Names
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
      "trainers": trainersFileName
    }

    addEventsRandomized, starters = Randomizer.getRandomizedAddPokemonEvents(serializedAreaOptions) # Randomize the add pokemon events (such as initials)
    jsonArrayFile = open(f'{fileNames["addPokemonEvents"]}.json', 'w')
    jsonArrayFile.write(json.dumps({"values": addEventsRandomized}))
    jsonArrayFile.close()

    if serializedGlobalOptions["initials"]:
      jsonArrayFile = open('starters.json', 'w')
      jsonArrayFile.write(json.dumps(starters))
      jsonArrayFile.close()

    staticEventsRandomized = Randomizer.getRandomizedStaticPokemonEvents(serializedAreaOptions) # Randomize the static pokemon events
    jsonArrayFile = open(f'{fileNames["staticPokemonEvents"]}.json', 'w')
    jsonArrayFile.write(json.dumps({"values": staticEventsRandomized}))
    jsonArrayFile.close()

    areaRandomized = Randomizer.getRandomizedArea(serializedAreaOptions)  # Randomize the pokemon that spawns each areas
    jsonArrayFile = open(f'{fileNames["pokedata"]}.json', 'w')
    jsonArrayFile.write(json.dumps({"values": areaRandomized}))
    jsonArrayFile.close()

    pokemonRandomize = Randomizer.getRandomizedPokemonList(serializedPokemonOptions) # Randomize each pokemon individually
    jsonArrayFile = open(f'{fileNames["personal"]}.json', 'w')
    jsonArrayFile.write(json.dumps({"Table": pokemonRandomize}))
    jsonArrayFile.close()

    trainersRandomize = Randomizer.getRandomizedTrainersList(serializedTrainersOptions) # Randomize each trainer team and values
    jsonArrayFile = open(f'{fileNames["trainers"]}.json', 'w')
    jsonArrayFile.write(json.dumps({"values": trainersRandomize}))
    jsonArrayFile.close()

    print('Randomized!')

    print('Generating binaries..')
    addEventsResult = FlatC.generateBinary(schemaPath = f'./src/{fileNames["addPokemonEvents"]}.bfbs', jsonPath = f'./{fileNames["addPokemonEvents"]}.json')  # Generates the Randomized Add pokemon events binary
    if addEventsResult.stderr != b'':
      print('Error creating binary:', addEventsResult.stderr)
      continue

    staticEventsResult = FlatC.generateBinary(schemaPath = f'./src/{fileNames["staticPokemonEvents"]}.bfbs', jsonPath = f'./{fileNames["staticPokemonEvents"]}.json')  # Generates the Randomized Static pokemon events binary
    if staticEventsResult.stderr != b'':
      print('Error creating binary:', staticEventsResult.stderr)
      continue

    areaRandomizeResult = FlatC.generateBinary(schemaPath = f'./src/{fileNames["pokedata"]}.bfbs', jsonPath = f'./{fileNames["pokedata"]}.json')  # Generates the Randomized Areas binary
    if areaRandomizeResult.stderr != b'':
      print('Error creating binary:', areaRandomizeResult.stderr)
      continue

    # FlatC.serializeJson(jsonPath=f'./{fileNames["personal"]}.json', ouputName=f'{fileNames["personal"]}.bin') # Generates the Randomized Pokemon binary
    personalDataRandomizeResult = FlatC.generateBinary(schemaPath = f'./src/{fileNames["personal"]}.bfbs', jsonPath = f'./{fileNames["personal"]}.json')  # Generates the Randomized Areas binary
    if personalDataRandomizeResult.stderr != b'':
      print('Error creating binary:', personalDataRandomizeResult.stderr)
      continue

    trainerRandomizeResult = FlatC.generateBinary(schemaPath = f'./src/{fileNames["trainers"]}.bfbs', jsonPath = f'./{fileNames["trainers"]}.json')  # Generates the Randomized Trainers binary
    if trainerRandomizeResult.stderr != b'':
      print('Error creating binary:', trainerRandomizeResult.stderr)
      continue
    print('Binaries created!')

    # Files Paths
    addPokemonEventsPath = './static/world/data/event/event_add_pokemon/eventAddPokemon'
    staticPokemonEventsPath = './static/world/data/field/fixed_symbol/fixed_symbol_table'
    pokedataPath = './static/world/data/encount/pokedata/pokedata'
    personalDataPath = './static/avalon/data'
    trainerPath = './static/world/data/trainer/trdata'

    paths = {
      "addPokemonEvents": addPokemonEventsPath,
      "staticPokemonEvents": staticPokemonEventsPath,
      "pokedata": pokedataPath,
      "personal": personalDataPath,
      "trainers": trainerPath
    }

    for pathName in paths:
      os.makedirs(f'{paths[pathName]}/')

    for fileName in fileNames:
      print(f'{paths[fileName]}/{fileNames[fileName]}.bin')

      shutil.copy(f'./src/{fileNames[fileName]}.bfbs', f'{paths[fileName]}/{fileNames[fileName]}.bfbs')

      if serializedGlobalOptions["keepFiles"]:
        shutil.copy(f'./{fileNames[fileName]}.bin', f'{paths[fileName]}/{fileNames[fileName]}.bin')
      else:
        os.replace(f'./{fileNames[fileName]}.bin', f'{paths[fileName]}/{fileNames[fileName]}.bin')
        os.remove(f'./{fileNames[fileName]}.json')  
      
    print('Generating ZIP with the mod..')
    shutil.make_archive('randomized_pokemon', 'zip', './static')
    print('ZIP created!')
  
    shutil.rmtree('./static')

window.close()