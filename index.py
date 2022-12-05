# index.py
import os
import shutil
import json

from src.scripts import randomizer as Randomizer
from src.scripts import flatc as FlatC
from src.scripts import frame as WindowFrame

# Env Vars
os.environ["VERSION"] = "1.0.4"

# Create the window
optionsValues = {
  "keepFiles": False,

  ### Areas Options Start ###
  "items": True,
  "legendaries": True,
  "paradox": True,
  ### Areas Options End ###

  ### Pokemon Options Start ###
  "abilities": True,
  "tm": False,
  "learnset": False,
  ### Pokemon Options End ###

  ### Trainers Options Start ###
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
    }

    serializedAreaOptions = {
      "items": False if ("items" not in values.keys() or values["items"] is None or values["items"] == False) else True,
      "legendaries": False if ("legendaries" not in values.keys() or values["legendaries"] is None or values["legendaries"] == False) else True,
      "paradox": False if ("paradox" not in values.keys() or values["paradox"] is None or values["paradox"] == False) else True
    }

    serializedPokemonOptions = {
      "abilities": False if ("abilities" not in values.keys() or values["abilities"] is None or values["abilities"] == False) else True,
      "tm": False if ("tm" not in values.keys() or values["tm"] is None or values["tm"] == False) else True,
      "learnset": False if ("learnset" not in values.keys() or values["learnset"] is None or values["learnset"] == False) else True
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
      "abilities": False if ("abilities" not in values.keys() or values["abilities"] is None or values["abilities"] == False) else True,
      "legendaries": False if ("legendaries" not in values.keys() or values["legendaries"] is None or values["legendaries"] == False) else True,
      "paradox": False if ("paradox" not in values.keys() or values["paradox"] is None or values["paradox"] == False) else True,
      "trainerTeracristalize": False if ("trainerTeracristalize" not in values.keys() or values["trainerTeracristalize"] is None or values["trainerTeracristalize"] == False) else True,
      "forceFullTeam": False if ("forceFullTeam" not in values.keys() or values["forceFullTeam"] is None or values["forceFullTeam"] == False) else True,
      "keepGymType": False if ("keepGymType" not in values.keys() or values["keepGymType"] is None or values["keepGymType"] == False) else True,
      "trainersItems": False if ("trainersItems" not in values.keys() or values["trainersItems"] is None or values["trainersItems"] == False) else True,
      "competitivePkm": False if ("competitivePkm" not in values.keys() or values["competitivePkm"] is None or values["competitivePkm"] == False) else True,
      "trainerShiniesRate": trainerShiniesRate,
      "forceFinalEvolution": False if ("forceFinalEvolution" not in values.keys() or values["forceFinalEvolution"] is None or values["forceFinalEvolution"] == False) else True,
      "finalEvolutionCap": finalEvolutionCap
    }

    print('Area Options', serializedAreaOptions)
    print('Pokemon Options', serializedPokemonOptions)
    # Ending serializing options

    print('Starting randomizer...')
    areaRandomized = Randomizer.getRandomizedArea(serializedAreaOptions)  # Randomize the pokemon that spawns each areas
    jsonArrayFile = open('pokedata_array.json', 'w')
    jsonArrayFile.write(json.dumps({"values": areaRandomized}))
    jsonArrayFile.close()

    pokemonRandomize = Randomizer.getRandomizedPokemonList(serializedPokemonOptions) # Randomize each pokemon individually
    jsonArrayFile = open('personal_array.json', 'w')
    jsonArrayFile.write(json.dumps({"Table": pokemonRandomize}))
    jsonArrayFile.close()

    trainersRandomize = Randomizer.getRandomizedTrainersList(serializedTrainersOptions) # Randomize each trainer team and values
    jsonArrayFile = open('trdata_array.json', 'w')
    jsonArrayFile.write(json.dumps({"values": trainersRandomize}))
    jsonArrayFile.close()

    print('Randomized!')

    print('Generating binaries..')
    areaRandomizeResult = FlatC.generateBinary(schemaPath = "./src/pokedata_array.bfbs", jsonPath = "./pokedata_array.json")  # Generates the Randomized Areas binary
    if areaRandomizeResult.stderr != b'':
      print('Error creating binary:', areaRandomizeResult.stderr)
      continue

    FlatC.serializeJson(jsonPath='./personal_array.json', ouputName='personal_array.bin') # Generates the Randomized Pokemon binary

    trainerRandomizeResult = FlatC.generateBinary(schemaPath = "./src/trdata_array.bfbs", jsonPath = "./trdata_array.json")  # Generates the Randomized Trainers binary
    if trainerRandomizeResult.stderr != b'':
      print('Error creating binary:', trainerRandomizeResult.stderr)
      continue
    print('Binaries created!')

    pokedataPath = './static/world/data/encount/pokedata/pokedata'
    personalDataPath = './static/avalon/data'
    trainerPath = './static/world/data/trainer/trdata'

    os.makedirs(f'{pokedataPath}/')
    os.makedirs(f'{personalDataPath}/')
    os.makedirs(f'{trainerPath}/')

    shutil.copy('./src/pokedata_array.bfbs', pokedataPath)
    shutil.copy('./src/trdata_array.bfbs', trainerPath)

    if serializedGlobalOptions["keepFiles"]:
      shutil.copy('./pokedata_array.bin', f'{pokedataPath}/pokedata_array.bin')
      shutil.copy('./personal_array.bin', f'{personalDataPath}/personal_array.bin')
      shutil.copy('./trdata_array.bin', f'{trainerPath}/trdata_array.bin')
    else:
      os.replace('./pokedata_array.bin', f'{pokedataPath}/pokedata_array.bin')
      os.replace('./personal_array.bin', f'{personalDataPath}/personal_array.bin')
      os.replace('./trdata_array.bin', f'{trainerPath}/trdata_array.bin')
      
    print('Generating ZIP with the mod..')
    shutil.make_archive('randomized_pokemon', 'zip', './static')
    print('ZIP created!')

    if not serializedGlobalOptions["keepFiles"]:
    # Clean up
      os.remove('./pokedata_array.json')  
      os.remove('./personal_array.json')
      os.remove('./trdata_array.json')
  
    shutil.rmtree('./static')

window.close()