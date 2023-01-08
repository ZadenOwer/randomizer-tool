# randomizer/pokemon.py

import random

from src.scripts.randomizer.base import BaseRandomizer

class PokemonRandomizer(BaseRandomizer):

  def __init__(self, data: dict) -> None:
    super().__init__(data)

  def getRandomBaseStats(self, pkmPersonalData: dict):
    baseStats = list(pkmPersonalData["base_stats"].values())
    random.shuffle(baseStats)
    return dict(zip(pkmPersonalData["base_stats"].keys(), baseStats))

  def getRandomizedAbility(self, blacklist: list = []):
    abilities = [ability for ability in self.abilityList if ability not in blacklist]
    return self.getRandomValue(items=abilities)

  def getRandomizedTMList(self, default: list):
    tmList = self.tmList.copy()
    moveList = self.moveList.copy()
    randomizedTMList = []

    while len(randomizedTMList) < len(default):
      if len(tmList) == 0:
        tmList = moveList

      randomizedTM = self.getRandomValue(items=tmList)
      tmList.remove(randomizedTM)
      randomizedTMList.append(randomizedTM["id"])

    return randomizedTMList

  def getRandomizedLearnset(self, defaultLearnset: list):
    moveIds = [move["id"] for move in self.moveList]
    randomizedLearnset = []

    for defaultMove in defaultLearnset:
      randomMoveId = None
      while randomMoveId is None or randomMoveId in moveIds:
        randomMoveId = self.getRandomValue(items=moveIds)
      moveIds.remove(randomMoveId)
      randomizedLearnset.append({**defaultMove, "move": randomMoveId})

    return randomizedLearnset

  def getRandomizedPokemonList(self, options: dict = None):
    self.logger.info('Starting logs for Pokemon Personal Data Randomizer')

    randomizedPokemonList = []
    for pokemon in self.personalData["entry"]:
      if not options["fullPokeDex"] and not pokemon["is_present"]:
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
        self.logger.info(f'New randomized Base Stats: {randomStats}')
        randomizedPokemon["base_stats"] = randomStats

      randomizedPokemonList.append(randomizedPokemon)
      continue

    self.logger.info('Closing logs for Pokemon Personal Data Randomizer')
    return randomizedPokemonList
