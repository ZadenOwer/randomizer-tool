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
window = WindowFrame.getWindowFrame()

print('Opening window...')
# Create an event loop
while True:
  # Start the window of the program 
  event, values = window.read()

  if event == WindowFrame.ON_CLOSE:
    # End program if user closes window
    print('Closing window...')
    break


  # Serializing options
  serializedOptions = {
    "items": False if ("items" not in values.keys() or values["items"] is None or values["items"] == False) else True,
    "legendaries": False if ("legendaries" not in values.keys() or values["legendaries"] is None or values["legendaries"] == False) else True,
    "paradox": False if ("paradox" not in values.keys() or values["paradox"] is None or values["paradox"] == False) else True
  }

  print('Window values', serializedOptions)
  # Ending serializing options

  print('Starting randomizer...')
  pokemonRandomized = Randomizer.getRandomizedList(serializedOptions)
  jsonArrayFile = open('pokedata_array.json', 'w')
  jsonArrayFile.write(json.dumps({"values": pokemonRandomized}))
  jsonArrayFile.close()
  print('Randomized!')

  print('Generating binary..')
  result = FlatC.generateBinary()  
  if result.stderr != b'':
    print('Error creating binary:', result.stderr)
    continue
  print('Binary created!')

  os.makedirs('./static/world/data/encount/pokedata/pokedata/')

  shutil.copy('./src/pokedata_array.bfbs', './static/world/data/encount/pokedata/pokedata/')
  os.replace('./pokedata_array.bin', './static/world/data/encount/pokedata/pokedata/pokedata_array.bin')
  os.remove('./pokedata_array.json')

  print('Generating ZIP with the mod..')
  shutil.make_archive('randomized_pokemon', 'zip', './static')
  print('ZIP created!')

  shutil.rmtree('./static')
  

window.close()