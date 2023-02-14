# randomizer/spawns.py
import math
from src.scripts.randomizer.base import BaseRandomizer
from src.scripts.frame import updateProgress

class RaidsRandomizer(BaseRandomizer):

  raidsProgress = 0

  def __init__(self, data: dict, options: dict) -> None:
    super().__init__(data=data, options=options)

  # ********* Add Pokemon Events Randomizer Start *********

  def generateSpawnPokemon(self, oldPkmId:int, options: dict, blacklist: list = []):
    self.preparePokemonFilteredList(options=options, blacklist=blacklist, oldPkmId=oldPkmId)

    randomPokemon = self.getRandomPokemon(oldPkmId=oldPkmId, similarStats=options["raidSimilarStats"])

    form, sex = self.getRandomForm(randomPokemon["dexId"], randomPokemon["forms"])
    self.logger.info(f'Random pokemon generated: ID: {randomPokemon["dexId"]} - NAME: {randomPokemon["name"]} - FORM: {form}')

    return {
      **randomPokemon, # {devName, dexId}
      "form": form,
      "sex": sex
    }

  def getRaidsRandomizedList(self, raidLevelName: str, raidLevelLabel: str, options: dict = None):
    """
      raidLevelName: raid01Data | raid02Data | raid03Data | raid04Data | raid05Data | raid06Data
    """
    self.logger.info(f'Starting logs for {raidLevelLabel} Randomizer')
    raidRandomizedList = []
    raidOriginalData = self[raidLevelName]["values"]

    alreadyUsed = []
    totalItems = len(raidOriginalData)

    for item in raidOriginalData:
      pokemon = item["raidEnemyInfo"]

      if options["raidsRandomized"]:
        oldPkmDev = self.getPokemonDev(devName=pokemon["bossPokePara"]["devId"])

        randomPokemon = self.generateSpawnPokemon(oldPkmId=oldPkmDev["dexId"], options=options, blacklist=alreadyUsed)

        pokemon["bossPokePara"]["devId"] = randomPokemon["devName"]
        pokemon["bossPokePara"]["formId"] = randomPokemon["form"]
        pokemon["bossPokePara"]["sex"] = randomPokemon["sex"]
        alreadyUsed.append(randomPokemon["dexId"])

      raidRandomizedList.append(pokemon)

      self.raidsProgress = math.floor((len(raidRandomizedList)/totalItems)*100)
      print(f'Processing: {raidLevelLabel} Data {self.raidsProgress}% / 100%', end='\r')
      updateProgress(value=self.raidsProgress, title=f'Processing: {raidLevelLabel} Data')

    self.logger.info(f'Closing logs for {raidLevelLabel} Randomizer')
    return raidRandomizedList