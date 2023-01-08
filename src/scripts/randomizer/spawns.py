
from src.scripts.randomizer.base import BaseRandomizer

class SpawnsRandomizer(BaseRandomizer):

  def __init__(self, data: dict) -> None:
    super().__init__(data)

  # ********* Add Pokemon Events Randomizer Start *********

  def getRandomizedAddPokemonEvents(self, options: dict = None):
    self.logger.info('Starting logs for Initials Randomizer')
    randomizedList = []
    starters = {
      "fire": 0,
      "water": 0,
      "grass": 0,
    }

    for event in self.addPokemonEvents["values"]:
      isStarter = True if "hono" in event["label"] or "kusa" in event["label"] or "mizu" in event["label"] else False

      generator = self.generateRandomPaldeaPokemon

      if options["fullPokeDex"]:
        generator = self.generateRandomPokemon

      randomPokemon = None

      if isStarter and options["initials"]:
        loopCtrl = 0
        while (randomPokemon is None):
          randomPokemon = generator(options)

          if (randomPokemon["id"] in list(starters.values())):
            randomPokemon = None

          if (randomPokemon is None):
            continue

          if options["similarStats"]:
            if not self.hasSimilarStats(oldPkmDevName=event["pokeData"]["devId"], newPkmId=randomPokemon["id"]):
              randomPkmPersonal = self.getPokemonPersonalData(dexId=randomPokemon["id"])
              oldPkmPersonal = self.getPokemonPersonalData(dexId=event["pokeData"]["devId"])              
              checkedPkm = self.checkEvoStats(oldPkmPersonalData=oldPkmPersonal, newPkmPersonalData=randomPkmPersonal)

              if checkedPkm is not None:
                randomPokemon = checkedPkm
                continue

              if loopCtrl < self.MAX_SIMILIAR_STATS_TRIES:
                # To avoid infinite loop
                randomPokemon = None
                loopCtrl += 1

        event["pokeData"]["devId"] = randomPokemon["devName"]
        form, sex = self.getRandomForm(randomPokemon["id"], randomPokemon["forms"])
        event["pokeData"]["formId"] = form
        event["pokeData"]["sex"] = sex
        self.logger.info(f'Random pokemon generated: {randomPokemon["id"]} - {randomPokemon["devName"]} - {event["pokeData"]["formId"]}')

      if not isStarter and options["areasSpawnRandomized"]:
        loopCtrl = 0
        while (randomPokemon is None):
          randomPokemon = generator(options)

          if (randomPokemon is None):
            continue

          if options["similarStats"] == True:
            if not self.hasSimilarStats(oldPkmDevName=event["pokeData"]["devId"], newPkmId=randomPokemon["id"]):
              randomPkmPersonal = self.getPokemonPersonalData(dexId=randomPokemon["id"])
              oldPkmPersonal = self.getPokemonPersonalData(dexId=event["pokeData"]["devId"])              
              checkedPkm = self.checkEvoStats(oldPkmPersonalData=oldPkmPersonal, newPkmPersonalData=randomPkmPersonal)

              if checkedPkm is not None:
                randomPokemon = checkedPkm
                continue

              if loopCtrl < self.MAX_SIMILIAR_STATS_TRIES:
                # To avoid infinite loop
                randomPokemon = None
                loopCtrl += 1

        event["pokeData"]["devId"] = randomPokemon["devName"]
        form, sex = self.getRandomForm(randomPokemon["id"], randomPokemon["forms"])
        event["pokeData"]["formId"] = form
        event["pokeData"]["sex"] = sex
        self.logger.info(f'Random pokemon generated: {randomPokemon["id"]} - {randomPokemon["devName"]} - {event["pokeData"]["formId"]}')

      if isStarter:
        starterId = randomPokemon["id"] if randomPokemon is not None else event["pokeData"]["devId"]

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

    self.logger.info('Closing logs for Initials Randomizer')
    return randomizedList, starters

  # ********* Add Pokemon Events Randomizer End *********

  # ********* Static Pokemon Events Randomizer Start *********
  def getRandomizedStaticPokemonEvents(self, options: dict = None):
    self.logger.info('Starting logs for Statics Randomizer')
    randomizedList = []

    for event in self.fixedPokemonEvents["values"]:
      if options["areasSpawnRandomized"]:
        generator = self.generateRandomPaldeaPokemon

        if options["fullPokeDex"]:
          generator = self.generateRandomPokemon

        randomPokemon = None

        loopCtrl = 0
        while (randomPokemon is None):
          randomPokemon = generator(options)

          if (randomPokemon is None):
            continue

          if options["similarStats"] == True:
            if not self.hasSimilarStats(oldPkmDevName=event["pokeDataSymbol"]["devId"], newPkmId=randomPokemon["id"]):
              randomPkmPersonal = self.getPokemonPersonalData(dexId=randomPokemon["id"])
              oldPkmPersonal = self.getPokemonPersonalData(dexId=event["pokeDataSymbol"]["devId"])              
              checkedPkm = self.checkEvoStats(oldPkmPersonalData=oldPkmPersonal, newPkmPersonalData=randomPkmPersonal)

              if checkedPkm is not None:
                randomPokemon = checkedPkm
                continue

              if loopCtrl < self.MAX_SIMILIAR_STATS_TRIES:
                # To avoid infinite loop
                randomPokemon = None
                loopCtrl += 1

        event["pokeDataSymbol"]["devId"] = randomPokemon["devName"]
        form, sex = self.getRandomForm(randomPokemon["id"], randomPokemon["forms"])
        event["pokeDataSymbol"]["formId"] = form
        event["pokeDataSymbol"]["sex"] = sex
        self.logger.info(f'Random pokemon generated: {randomPokemon["id"]} - {randomPokemon["devName"]} - {event["pokeDataSymbol"]["formId"]}')

      if options["abilities"]:
        event["pokeDataSymbol"]["tokuseiIndex"] = "RANDOM_123"
      
      event["pokeDataSymbol"]["rareType"] = "DEFAULT"

      randomizedList.append(event)

    self.logger.info('Closing logs for Statics Randomizer')
    return randomizedList

  # ********* Static Pokemon Events Randomizer End *********

  # ********* Areas Randomizer Start *********
  def getRandomizedArea(self, options: dict = None):
    self.logger.info('Starting logs for Areas Randomizer')
    randomizedAreaList = []

    for pokemon in self.pokemonData["values"]:
      if options["areasSpawnRandomized"]:
        pokemonGenerator = self.generateRandomPaldeaPokemon

        if options["fullPokeDex"] == True:
          pokemonGenerator = self.generateRandomPokemon

        randomPokemon = None

        loopCtrl = 0
        while (randomPokemon is None):
          randomPokemon = pokemonGenerator(options)

          if randomPokemon is None:
            continue

          if options["similarStats"] == True:
            if not self.hasSimilarStats(oldPkmDevName=pokemon["devid"], newPkmId=randomPokemon["id"]):
              randomPkmPersonal = self.getPokemonPersonalData(dexId=randomPokemon["id"])
              oldPkmPersonal = self.getPokemonPersonalData(dexId=pokemon["devid"])              
              checkedPkm = self.checkEvoStats(oldPkmPersonalData=oldPkmPersonal, newPkmPersonalData=randomPkmPersonal)

              if checkedPkm is not None:
                randomPokemon = checkedPkm
                continue

              if loopCtrl < self.MAX_SIMILIAR_STATS_TRIES:
                # To avoid infinite loop
                randomPokemon = None
                loopCtrl += 1

        pokemon["devid"] = randomPokemon["devName"]
        form, sex = self.getRandomForm(randomPokemon["id"], randomPokemon["forms"])
        pokemon["formno"] = form
        pokemon["sex"] = sex

        self.logger.info(f'Random pokemon generated: {randomPokemon["id"]} - {randomPokemon["devName"]} - form {pokemon["formno"]}')
      
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
      self.logger.info(f'Random item: {randomItem["id"]} - {randomItem["devName"]}')

    self.logger.info('Closing logs for Areas Randomizer')
    return randomizedAreaList

  # ********* Areas Randomizer End *********