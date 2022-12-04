import subprocess
import json

from pythonnet import load
load("coreclr")

import clr

clr.AddReference('./src/dlls/FlatSharp')
clr.AddReference('./src/dlls/FlatBufferConverter')
from FlatBufferConverter import FlatSerializer, PersonalTable9SVfb

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

def serializeJson(jsonPath: str, ouputName: str):
  with open(jsonPath, 'r') as jsonData:
    strJson = jsonData.read()
    my_instance = FlatSerializer()
    my_instance.SerializeFrom(strJson, ouputName)