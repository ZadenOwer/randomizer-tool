# index.py
import os
import shutil
import json

from src.scripts import randomizer as Randomizer
from src.scripts import flatc as FlatC
from src.scripts import frame as WindowFrame

# Env Vars
os.environ["VERSION"] = "1.0.2"

# Create the window
optionsValues = {
  "items": True,
  "legendaries": True,
  "paradox": True,
  "abilities": True,
  "tm": False,
  "learnset": False
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

  if event == 'Randomize!':
    # Serializing options
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

    print('Randomized!')

    print('Generating binaries..')
    areaRandomizeResult = FlatC.generateBinary(schemaPath = "./src/pokedata_array.bfbs", jsonPath = "./pokedata_array.json")  # Generates the Randomized Areas binary
    if areaRandomizeResult.stderr != b'':
      print('Error creating binary:', areaRandomizeResult.stderr)
      continue

    FlatC.serializeJson(jsonPath='./personal_array.json', ouputName='personal_array.bin') # Generates the Randomized Pokemon binary

    print('Binaries created!')

    pokedataPath = './static/world/data/encount/pokedata/pokedata'
    personalDataPath = './static/avalon/data'

    os.makedirs(f'{pokedataPath}/')
    os.makedirs(f'{personalDataPath}/')

    shutil.copy('./src/pokedata_array.bfbs', pokedataPath)

    os.replace('./pokedata_array.bin', f'{pokedataPath}/pokedata_array.bin')
    os.replace('./personal_array.bin', f'{personalDataPath}/personal_array.bin')

    print('Generating ZIP with the mod..')
    shutil.make_archive('randomized_pokemon', 'zip', './static')
    print('ZIP created!')

    # Clean up
    os.remove('./pokedata_array.json')
    os.remove('./personal_array.json')
    shutil.rmtree('./static')
  

window.close()