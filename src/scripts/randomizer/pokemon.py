
from src.scripts.randomizer.base import BaseRandomizer

class PokemonRandomizer(BaseRandomizer):

  def __init__(self, data: dict) -> None:
    super().__init__(data)

  def getRandomBaseStats(self, pkmPersonalData: dict):
    baseStats = pkmPersonalData["base_stats"]
    statsNames = list(baseStats.keys())
    newStats = {}

    for statName in baseStats.keys():
      randomStat = self.getRandomValue(statsNames)
      newStats[statName] = baseStats[randomStat]
      
      statsNames.remove(randomStat)
    
    return newStats

  # ********* Pokemon Randomizer End *********
  def getRandomizedAbility(self, blacklist: list = []):
    randomizedAbility = None

    while (randomizedAbility is None or randomizedAbility in blacklist):
      randomizedAbility = self.getRandomValue(items=self.abilityList)

    return randomizedAbility

  def getRandomizedTMList(self, default: list):
    maxTMList = len(default)
    randomizedTMList = []
    movesPool = self.tmList

    for item in range(0, maxTMList):
      randomizedTM = None

      if (len(randomizedTMList) == len(self.tmList)):
        movesPool = self.moveList

      while (randomizedTM is None or randomizedTM in randomizedTMList):
        randomizedTM = self.getRandomValue(items=movesPool)

      randomizedTMList.append(randomizedTM["id"])

    return randomizedTMList

  def getRandomizedLearnset(self, defaultLearnset: list):
    randomizedLearnset = []
    alreadyUsedIds = []

    for defaultMove in defaultLearnset:
      moveId = None

      while (moveId is None or moveId in alreadyUsedIds):
        randomMove = self.getRandomValue(items=self.moveList)

        moveId = randomMove["id"]

      randomizedLearnset.append({
        **defaultMove,
        "move": moveId
      })

    return randomizedLearnset

  def getRandomizedPokemonList(self, options: dict = None):
    self.logger.info('Starting logs for Pokemon Personal Data Randomizer')

    randomizedPokemonList = []
    for pokemon in self.personalData["entry"]:

      if options["fullPokeDex"]:
        pokemon["is_present"] = True

      if not pokemon["is_present"]:
        randomizedPokemonList.append(pokemon)
        continue

      devPkm = self.getPokemonDev(dexId=pokemon["species"]["model"])
      self.logger.info(f'Randomizing data for pokemon: {devPkm["id"]} - {devPkm["devName"]} - form {pokemon["species"]["form"]}')

      randomizedPokemon = {
        **pokemon
      }

      if (options["abilities"] == True):
        # Randomizing Abilities
        self.logger.info(f'Original Abilities: A:{randomizedPokemon["ability_1"]}, B:{randomizedPokemon["ability_2"]}, H: {randomizedPokemon["ability_3"]}')
        defaultAbilities = [randomizedPokemon["ability_1"], randomizedPokemon["ability_2"], randomizedPokemon["ability_3"]]
        randomizedPokemon["ability_1"] = self.getRandomizedAbility(blacklist=defaultAbilities)
        randomizedPokemon["ability_2"] = self.getRandomizedAbility(blacklist=defaultAbilities+[randomizedPokemon["ability_1"]])
        randomizedPokemon["ability_3"] = self.getRandomizedAbility(blacklist=defaultAbilities+[randomizedPokemon["ability_1"], randomizedPokemon["ability_2"]])
        self.logger.info(f'New Abilities: A:{randomizedPokemon["ability_1"]}, B:{randomizedPokemon["ability_2"]}, H: {randomizedPokemon["ability_3"]}')

      if (options["tm"]):
        # Randomizing TM compatibility
        randomizedPokemon["tm_moves"] = self.getRandomizedTMList(default=randomizedPokemon["tm_moves"])

      if (options["learnset"]):
        # Randomizing Pool of moves the pokemon will learn by level
        randomizedPokemon["levelup_moves"] = self.getRandomizedLearnset(randomizedPokemon["levelup_moves"])

      if options["randomBaseStats"]:
        randomStats = self.getRandomBaseStats(pkmPersonalData=randomizedPokemon)
        self.logger.info(f'Original Base Stats: {randomizedPokemon["base_stats"]}')
        self.logger.info(f'New Base Stats: {randomStats}')
        randomizedPokemon["base_stats"] = randomStats

      randomizedPokemonList.append(randomizedPokemon)
      continue

    self.logger.info('Closing logs for Pokemon Personal Data Randomizer')
    return randomizedPokemonList

  # ********* Pokemon Randomizer End *********
