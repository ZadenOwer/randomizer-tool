# randomizer/spawns.py
import math
from collections import defaultdict
from src.scripts.randomizer.base import BaseRandomizer
from src.scripts.frame import updateProgress

class SpawnsRandomizer(BaseRandomizer):

  addEventsProgress = 0
  staticEventsProgress = 0
  areaProgress = 0

  def __init__(self, data: dict) -> None:
    super().__init__(data)

  # ********* Add Pokemon Events Randomizer Start *********

  def generateSpawnPokemon(self, devName: str, options: dict, blacklist: list = []):
    randomPokemon = None
    loopCtrl = 0
    while (randomPokemon is None):
      randomPokemon = self.generateRandomPokemon(options, blacklist=blacklist)

      if options["similarStats"]:
        if not self.hasSimilarStats(oldPkmDevName=devName, newPkmId=randomPokemon["id"]):
          randomPkmPersonal = self.getPokemonPersonalData(dexId=randomPokemon["id"])
          oldPkmPersonal = self.getPokemonPersonalData(dexId=devName)              
          checkedPkm = self.checkEvoStats(oldPkmPersonalData=oldPkmPersonal, newPkmPersonalData=randomPkmPersonal)

          if checkedPkm is not None:
            randomPokemon = checkedPkm
            continue

          if loopCtrl < self.MAX_SIMILIAR_STATS_TRIES:
            # To avoid infinite loop
            randomPokemon = None
            loopCtrl += 1

    form, sex = self.getRandomForm(randomPokemon["id"], randomPokemon["forms"])
    self.logger.info(f'Random pokemon generated: ID: {randomPokemon["id"]} - NAME: {randomPokemon["devName"]} - FORM: {form}')

    return {
      **randomPokemon, # {devName, id}
      "form": form,
      "sex": sex
    }

  def getRandomizedAddPokemonEvents(self, options: dict = None):
    self.logger.info('Starting logs for Initials Randomizer')
    randomizedList = []
    alreadyUsed = []
    starters = defaultdict(int)
    totalItems = len(self.addPokemonEvents["values"])

    for event in self.addPokemonEvents["values"]:
      isStarter = True if "hono" in event["label"] or "kusa" in event["label"] or "mizu" in event["label"] else False

      if options["initials"] or options["areasSpawnRandomized"]:
        if isStarter and options["initials"]:
          randomPokemon = self.generateSpawnPokemon(devName=event["pokeData"]["devId"], options=options, blacklist=list(starters.values())+alreadyUsed)        
        elif not isStarter and options["areasSpawnRandomized"]:
          randomPokemon = self.generateSpawnPokemon(devName=event["pokeData"]["devId"], options=options, blacklist=alreadyUsed)
        else:
          randomPokemon = None

        if randomPokemon is not None:
          event["pokeData"]["devId"] = randomPokemon["devName"]
          event["pokeData"]["formId"] = randomPokemon["form"]
          event["pokeData"]["sex"] = randomPokemon["sex"]
          alreadyUsed.append(randomPokemon["id"])

      if isStarter and options["initials"]:
        starterId = self.getPokemonDev(devName=event["pokeData"]["devId"])["id"]

        if "hono" in event["label"]:
          # Fire starter
          starters["fire"] = starterId

        if "kusa" in event["label"]:
          # Plant starter
          starters["grass"] = starterId

        if "mizu" in event["label"]:
          # Water starter
          starters["water"] = starterId
        
      if options["abilities"]:
        event["pokeData"]["tokusei"] = "RANDOM_123"

      if options["items"]:
        event["pokeData"]["item"] = self.generateRandomItem()["devName"]

      event["pokeData"]["rareType"] = "DEFAULT"

      randomizedList.append(event)
      self.addEventsProgress = math.floor((len(randomizedList)/totalItems)*100)
      print(f'Processing: Trade Events Data {self.addEventsProgress}% / 100%', end='\r')
      updateProgress(value=self.addEventsProgress, title="Processing: Trade Events Data")

    self.logger.info('Closing logs for Initials Randomizer')
    return randomizedList, starters

  # ********* Add Pokemon Events Randomizer End *********

  # ********* Static Pokemon Events Randomizer Start *********
  def getRandomizedStaticPokemonEvents(self, options: dict = None):
    self.logger.info('Starting logs for Statics Randomizer')
    randomizedList = []
    totalItems = len(self.fixedPokemonEvents["values"])

    for event in self.fixedPokemonEvents["values"]:
      if options["areasSpawnRandomized"]:

        randomPokemon = self.generateSpawnPokemon(devName=event["pokeDataSymbol"]["devId"], options=options)

        event["pokeDataSymbol"]["devId"] = randomPokemon["devName"]
        event["pokeDataSymbol"]["formId"] = randomPokemon["form"]
        event["pokeDataSymbol"]["sex"] = randomPokemon["sex"]

      if options["abilities"]:
        event["pokeDataSymbol"]["tokuseiIndex"] = "RANDOM_123"
      
      event["pokeDataSymbol"]["rareType"] = "DEFAULT"

      randomizedList.append(event)
      self.staticEventsProgress = math.floor((len(randomizedList)/totalItems)*100)
      print(f'Processing: Statics Events Data {self.staticEventsProgress}% / 100%', end='\r')
      updateProgress(value=self.staticEventsProgress, title="Processing: Statics Events Data")

    self.logger.info('Closing logs for Statics Randomizer')
    return randomizedList

  # ********* Static Pokemon Events Randomizer End *********

  # ********* Areas Randomizer Start *********
  def getRandomizedArea(self, options: dict = None):
    self.logger.info('Starting logs for Areas Randomizer')
    randomizedAreaList = []
    totalItems = len(self.pokemonData["values"])

    for pokemon in self.pokemonData["values"]:
      if options["areasSpawnRandomized"]:
        randomPokemon = self.generateSpawnPokemon(devName=pokemon["devid"], options=options)

        pokemon["devid"] = randomPokemon["devName"]
        pokemon["formno"] = randomPokemon["form"]
        pokemon["sex"] = randomPokemon["sex"]
      
      if options["items"] == False:
        #  No randomized items
        randomizedAreaList.append(pokemon)
        continue

      randomItem = self.generateRandomItem()
      randomizedAreaList.append({
        **pokemon,
        "bringItem": {
          "itemID": randomItem["id"],
          "bringRate": 100
        }
      })
      self.areaProgress = math.floor((len(randomizedAreaList)/totalItems)*100)
      print(f'Processing: Area Spawns Data {self.areaProgress}% / 100%', end='\r')
      updateProgress(value=self.areaProgress, title="Processing: Area Spawns Data")

    self.logger.info('Closing logs for Areas Randomizer')
    return randomizedAreaList

  # ********* Areas Randomizer End *********