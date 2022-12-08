import subprocess
import os

def generateBinary(schemaPath:str, jsonPath:str):
  # command = "flatc.exe -b schema.bfbs data.json"
  flatcPath = "./src/flatc.exe"

  process = subprocess.run([
    os.path.abspath(flatcPath),
    "-b",
    os.path.abspath(schemaPath),
    os.path.abspath(jsonPath)
  ], capture_output=True)

  return process