import subprocess

def generateBinary():
  # command = "flatc.exe -b ./src/world/data/encount/pokedata/pokedata/pokedata_array.bfbs ./pokedata_array.json"
  flatcPath = "./src/flatc.exe"
  schemaPath = "./src/pokedata_array.bfbs"
  jsonPath = "./pokedata_array.json"

  process = subprocess.run([
    flatcPath,
    "-b",
    schemaPath,
    jsonPath
  ], capture_output=True)

  return process