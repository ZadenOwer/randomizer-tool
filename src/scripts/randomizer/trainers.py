
import math
import json

from src.scripts.randomizer.base import BaseRandomizer

class TrainersRandomizer(BaseRandomizer):

  def __init__(self, data: dict) -> None:
    super().__init__(data)

  # ********* Trainers Randomizer Start *********
  def getPerfectIvs(self):
    stats = ["hp", "atk", "def", "spAtk", "spDef", "agi"]
    lowerStat = self.getRandomValue(items=stats)

    talentValue = {
      "hp": 31,
      "atk": 31,
      "def": 31,
      "spAtk": 31,
      "spDef": 31,
      "agi": 31
    }

    talentValue[lowerStat] = 30

    return talentValue

  def getCompetitiveEvs(self):
    stats = ["hp", "atk", "def", "spAtk", "spDef", "agi"]
    lowerStat = self.getRandomValue(items=stats)

    EVsTotalValue = 510
    EVsMaxValue = 255

    effortValue = {
      "hp": 0,
      "atk": 0,
      "def": 0,
      "spAtk": 0,
      "spDef": 0,
      "agi": 0
    }

    return effortValue

  def isShiny(self, rateValue: int):
    # rateValue based on 100
    # return 0 - Not Shiny
    # return 1 - Shiny

    rng = self.getRandomValue(items=range(0,101))

    if rng <= rateValue:
      return 1

    return 0

  def getTrainerTypeId(self, trainerTypeName: str):
    if "normal" in trainerTypeName: #Normal (duh)
      return 0

    if "kakutou" in trainerTypeName: #Fight
      return 1

    if "hikou" in trainerTypeName: #Fly
      return 2

    if "doku" in trainerTypeName: #Poison
      return 3

    if "jimen" in trainerTypeName: #Earth
      return 4

    if "iwa" in trainerTypeName: #Rock (still to confirm)
      return 5

    if "mushi" in trainerTypeName: #Bug
      return 6

    if "ghost" in trainerTypeName: #Ghost (duh x2)
      return 7

    if "hagane" in trainerTypeName: #Steel
      return 8

    if "hono" in trainerTypeName: #Fire
      return 9

    if "mizu" in trainerTypeName: #Water
      return 10

    if "kusa" in trainerTypeName: #Plant
      return 11

    if "denki" in trainerTypeName: #Electric
      return 12

    if "esper" in trainerTypeName: #Psiquic
      return 13

    if "koori" in trainerTypeName: #Ice
      return 14

    if "dragon" in trainerTypeName: #Dragon (duh x3)
      return 15

    if "aku" in trainerTypeName: #Dark
      return 16

    if "fairy" in trainerTypeName: #Fairy (duh x4)
      return 17

  def isMonotypeTrainer(self, trainerTypeName: str):
    if "leader" in trainerTypeName: # Gym Leader
      return True
      
    if "e4_" in trainerTypeName: #Elite 4
      return True
      
    if "star_" in trainerTypeName and "_boss" in trainerTypeName: #Team Star Boss
      return True

    return False

  def getMinMaxLv(self, trainerPokemon: dict):
    pokemonKeys = ["poke1","poke2","poke3","poke4","poke5","poke6"]

    maxLv = 0 # From min to max
    minLv = 100 # From max to min

    for pokeKey in pokemonKeys:
      pokeLv = trainerPokemon[pokeKey]["level"]

      if pokeLv != 0 and pokeLv < minLv:
        minLv = pokeLv

      if pokeLv > maxLv:
        maxLv = pokeLv

    return minLv, maxLv

  def trainerPokeTemplate(self):
    return {
      "ballId": "MONSUTAABOORU",
      "gemType": "DEFAULT",
      "tokusei": "RANDOM_12",
      "talentType": "RANDOM",
      "wazaType": "DEFAULT",
      "waza1": {
        "wazaId": "WAZA_NULL",
        "pointUp": 0
      },
      "waza2": {
        "wazaId": "WAZA_NULL",
        "pointUp": 0
      },
      "waza3": {
        "wazaId": "WAZA_NULL",
        "pointUp": 0
      },
      "waza4": {
        "wazaId": "WAZA_NULL",
        "pointUp": 0
      }
    }

  def getRandomizedTrainersList(self, options: dict = None):
    self.logger.info('Starting logs for Trainers Randomizer')

    randomizedTrainersList = []
    pokemonKeys = ["poke1","poke2","poke3","poke4","poke5","poke6"]
    originalStarters = ["DEV_NEKO", "DEV_WANI", "DEV_KAMO"]
    
    shinyValues = ["NO_RARE", "RARE"]
    rateValue = options["trainerShiniesRate"]
    shiny = self.isShiny(rateValue=rateValue)

    rivalInitialShiny = shinyValues[shiny]

    for trainer in self.trainersData["values"]:

      self.logger.info(f'Trainer: {trainer["trid"]} - Type: {trainer["trainerType"]}')

      randomizedTrainer = {
        **trainer
      }
      alreadyUsedId = []

      isRival = False
      rivalType = None
      rivalStage = None
      rivalStarterName = None
      rivalPokemon = None
      rivalParams = randomizedTrainer["trid"].split("_")

      if "rival_" in randomizedTrainer["trid"]:
        if len(rivalParams) == 3:
          isRival = True
          rivalType = self.getTrainerTypeId(rivalParams[2])
          if "multi" in rivalParams:
            rivalStage = rivalParams[1]
          else:
            rivalStage = int(rivalParams[1][1])

      if options["keepRivalInitial"] and isRival:
        if options["initials"]:
          # Get the initial from the json created
          with open('starters.json', 'r', encoding='utf-8-sig') as startersJson:
            randomStarters = json.load(startersJson)

            if rivalType == 9: #Fire
              rivalPokemon = self.getPokemonDev(dexId=randomStarters["grass"])

            if rivalType == 10: #Water
              rivalPokemon = self.getPokemonDev(dexId=randomStarters["fire"])

            if rivalType == 11: #Plant
              rivalPokemon = self.getPokemonDev(dexId=randomStarters["water"])
            
            rivalStarterName = rivalPokemon["devName"]
        else:
          if rivalType == 9: #Fire
            rivalStarterName = "DEV_NEKO1"

          if rivalType == 10: #Water
            rivalStarterName = "DEV_WANI1"

          if rivalType == 11: #Plant
            rivalStarterName = "DEV_KAMO1"

          rivalPokemon = self.getPokemonDev(devName=rivalStarterName)

        if rivalStage == 4:
          # Should evolve initial once
          rivalPokemon = self.getNextEvolution(devName=rivalStarterName)
          if rivalPokemon is None:
            rivalPokemon = self.getPokemonDev(devName=rivalStarterName)

        if (isinstance(rivalStage, int) and rivalStage >= 5) or rivalStage == "multi":
          # Initial should be on final evolution
          rivalPokemon = self.getFinalEvolution(devName=rivalStarterName)
          if rivalPokemon is None:
            rivalPokemon = self.getPokemonDev(devName=rivalStarterName)

      if options["trainerTeracristalize"]:
        randomizedTrainer["changeGem"] = True

      if options["forceFullTeam"]:
        minLv, maxLv = self.getMinMaxLv(trainerPokemon=randomizedTrainer)
        
        if minLv == maxLv:
          if (maxLv >= 5):
            lowLv = maxLv-2
            medLv = maxLv-1
          else:
            lowLv = maxLv
            medLv = maxLv
        else:
          lowLv = minLv
          medLv = math.floor((maxLv-minLv)/2)+lowLv

        pokemonLvl = {
          "poke1": {
            "level": lowLv
          },
          "poke2": {
            "level": lowLv
          },
          "poke3": {
            "level": lowLv
          },
          "poke4": {
            "level": medLv
          },
          "poke5": {
            "level": medLv
          },
          "poke6": {
            "level": maxLv
          }
        }

      for pokeKey in pokemonKeys:
        if (options["forceFullTeam"] == False and randomizedTrainer[pokeKey]["devId"] == "DEV_NULL"):
          continue

        if options["trainersRandomized"]:
          if options["keepRivalInitial"] and isRival:
            # Not randomize and get the starter instead
            if (randomizedTrainer[pokeKey]["devId"][:-1] in originalStarters):
              randomizedTrainer[pokeKey] = {
                **randomizedTrainer[pokeKey],
                "devId": rivalPokemon["devName"],
                "formId": 0,
                "sex": "DEFAULT",
                **self.trainerPokeTemplate()
              }

              self.logger.info(f'Rival starter type {rivalParams[2]} changed for: {rivalPokemon["id"]} - {rivalPokemon["devName"]}')
              alreadyUsedId.append(rivalPokemon["id"])
          else:              
            randomPokemon = None

            loopCtrl = 0
            while (randomPokemon is None or randomPokemon["id"] in alreadyUsedId):               
              randomPokemon = self.generateRandomPokemon(options)

              if (randomPokemon is None):
                continue

              if options["trainerSimilarStats"] == True:
                pokeDevName = randomizedTrainer[pokeKey]["devId"]
                if pokeDevName == "DEV_NULL":
                  previousKey = pokemonKeys[pokemonKeys.index(pokeKey) - 1]
                  pokeDevName = randomizedTrainer[previousKey]["devId"]

                if not self.hasSimilarStats(oldPkmDevName=pokeDevName, newPkmId=randomPokemon["id"]):
                  randomPkmPersonal = self.getPokemonPersonalData(dexId=randomPokemon["id"])
                  oldPkmPersonal = self.getPokemonPersonalData(dexId=pokeDevName)              
                  checkedPkm = self.checkEvoStats(oldPkmPersonalData=oldPkmPersonal, newPkmPersonalData=randomPkmPersonal)

                  if checkedPkm is not None:
                    randomPokemon = checkedPkm

                  elif loopCtrl < self.MAX_SIMILIAR_STATS_TRIES:
                    # To avoid infinite loop
                    randomPokemon = None
                    loopCtrl += 1
                    continue

              if options["keepGymType"]:
                if self.isMonotypeTrainer(trainerTypeName=randomizedTrainer["trainerType"]):
                  trainerTypeId = self.getTrainerTypeId(trainerTypeName=randomizedTrainer["trainerType"])
                  randomPokemonPersonal = self.getPokemonPersonalData(randomPokemon["id"])
                  
                  type1 = randomPokemonPersonal["type_1"]
                  type2 = randomPokemonPersonal["type_2"]

                  if (trainerTypeId not in [type1, type2]):
                    # Randomize again if any type not match with the trainerType
                    randomPokemon = None

            alreadyUsedId.append(randomPokemon["id"])

            form, sex = self.getRandomForm(randomPokemon["id"], randomPokemon["forms"])

            randomizedTrainer[pokeKey] = {
              **randomizedTrainer[pokeKey],
              "devId": randomPokemon["devName"],
              "formId": form,
              "sex": sex,
              **self.trainerPokeTemplate()
            }

            self.logger.info(f'Random pokemon generated: {randomPokemon["id"]} - {randomPokemon["devName"]} - form {randomizedTrainer[pokeKey]["formId"]}')

        if options["forceFullTeam"]:
          randomizedTrainer[pokeKey]["level"] = pokemonLvl[pokeKey]["level"]

        if options["abilities"]:
          randomizedTrainer[pokeKey]["tokusei"] = "RANDOM_123"

        if options["trainersItems"]:
          randomItem = self.generateRandomItem()
          randomizedTrainer[pokeKey] = {
            **randomizedTrainer[pokeKey],
            "item": randomItem["devName"],
          }

        if options["competitivePkm"]:
          perfectIvs = self.getPerfectIvs()
          randomizedTrainer[pokeKey] = {
            **randomizedTrainer[pokeKey],
            "talentType": "VALUE",
            "talentValue": perfectIvs
          }
          randomizedTrainer["isStrong"] = True

        if options["trainerShiniesRate"] >= 0 and options["trainerShiniesRate"] <= 100:
          if options["keepRivalInitial"] and isRival:
            randomizedTrainer[pokeKey] = {
              **randomizedTrainer[pokeKey],
              "rareType": rivalInitialShiny
            }
          else:
            shinyValues = ["NO_RARE", "RARE"]

            rateValue = options["trainerShiniesRate"]

            shiny = self.isShiny(rateValue=rateValue)

            randomizedTrainer[pokeKey] = {
              **randomizedTrainer[pokeKey],
              "rareType": shinyValues[shiny]
            }

        if options["forceFinalEvolution"]:
          if options["finalEvolutionCap"] > 0 or options["finalEvolutionCap"] < 100:
            if randomizedTrainer[pokeKey]["level"] >= options["finalEvolutionCap"]:          
              finalEvo = self.getFinalEvolution(dexId=randomPokemon["id"])

              if finalEvo is None:
                randomizedTrainer[pokeKey] = {
                  **randomizedTrainer[pokeKey],
                  "devId": randomPokemon["devName"]
                }
              else:
                randomizedTrainer[pokeKey] = {
                  **randomizedTrainer[pokeKey],
                  "devId": finalEvo["devName"]
                }

      randomizedTrainersList.append(randomizedTrainer)

    self.logger.info('Closing logs for Trainers Randomizer')
    return randomizedTrainersList

  # ********* Trainers Randomizer End *********
