import subprocess

def generateBinary(schemaPath:str, jsonPath:str):
  # command = "flatc.exe -b schema.bfbs data.json"
  flatcPath = "./src/flatc.exe"

  process = subprocess.run([
    flatcPath,
    "-b",
    schemaPath,
    jsonPath
  ], capture_output=True)

  return process