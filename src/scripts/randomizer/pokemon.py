# randomizer/pokemon.py
import math
import random

from src.scripts.randomizer.base import BaseRandomizer
from src.scripts.frame import updateProgress

class PokemonRandomizer(BaseRandomizer):

  pokemonProgress = 0
  STATUS_MOVE = "STATUS"

  def __init__(self, data: dict, options: dict) -> None:
    super().__init__(data=data, options=options)

  def getRandomBaseStats(self, pkmPersonalData: dict):
    baseStats = list(pkmPersonalData["base_stats"].values())
    random.shuffle(baseStats)
    return dict(zip(pkmPersonalData["base_stats"].keys(), baseStats))

  def getRandomizedAbility(self, blacklist: list = []):
    abilities = [ability for ability in self.abilityList if ability not in blacklist]
    return self.getRandomValue(items=abilities)

  def getRandomizedTMList(self, default: list):
    tmList = self.tmList.copy()
    randomizedTMList = []

    while True:
      if len(tmList) == 0:
        break

      if len(randomizedTMList) == len(default):
        break

      randomizedTM = self.getRandomValue(items=tmList)
      tmList.remove(randomizedTM)
      randomizedTMList.append(randomizedTM["id"])

    return randomizedTMList

  def hasSimilarPower(self, oldMovePower: int, newMovePower: int | str, atLevel: int):
    if newMovePower == self.STATUS_MOVE:
      if (atLevel < 20):
        # Avoid learning status moves at lower levels for a better experience and progression
        return False

      # All the status move are possible choices for the random move
      return True

    if oldMovePower >= 200:
      return (oldMovePower - 50 < newMovePower) and (newMovePower < oldMovePower + 50)
    
    if oldMovePower >= 100:
      return (oldMovePower - 20 < newMovePower) and (newMovePower < oldMovePower + 20)

    return (oldMovePower - 10 < newMovePower) and (newMovePower < oldMovePower + 10)

  def hasSimilarType(self, oldMoveType: int, newMoveType: int):
    if oldMoveType == newMoveType:
      return True

    return False
  
  def getRandomMove(self, defaultMove: dict, options: dict, blacklist: list = []):
    moveList = {id: move for id, move in self.moveList.items() if move["id"] not in blacklist}
    moveData = None
    try:
      moveData = self.moveList[str(defaultMove["move"])]
    except:
      # The old move isn't valid for the 9th gen, putting a default move based on the level
      if defaultMove["level"] <= 10:
        moveData = self.moveList["364"] # Feint - Normal - Power 30
      elif defaultMove["level"] <= 30:
        moveData = self.moveList["229"] # Rapid Spin - Normal - Power 50:
      else:
        moveData = self.moveList["5"] # Mega Punch - Normal - Power 100:

    if options["movePower"]:
      isStatus = True if moveData["power"] == self.STATUS_MOVE else False
      
      if isStatus:
        # If the old move is a status one, a fake power will be calculated based on the level this move is learned
        if defaultMove["level"] <= 10:
          fakePower = 30
        elif defaultMove["level"] <= 30:
          fakePower = 50
        else:
          fakePower = 100

        moveList = {id: move for id, move in moveList.items() if self.hasSimilarPower(oldMovePower=fakePower, newMovePower=move["power"], atLevel=defaultMove["level"])}

      if not isStatus:
        moveList = {id: move for id, move in moveList.items() if self.hasSimilarPower(oldMovePower=moveData["power"], newMovePower=move["power"], atLevel=defaultMove["level"])}

    if options["moveType"]:
      moveList = {id: move for id, move in moveList.items() if self.hasSimilarType(oldMoveType=moveData["type"], newMoveType=move["type"])}

    if len(moveList) == 0:
      # If for some reason all the filters clear the array, will ignore all the filters applied
      moveList = self.moveList

    randomMove = self.getRandomValue(items=list(moveList.values()))
    return randomMove

  def getRandomizedLearnset(self, defaultLearnset: list, options: dict):
    randomizedLearnset = []
    alreadyUsed = []

    for defaultMove in defaultLearnset:
      randomMove = self.getRandomMove(defaultMove=defaultMove, options=options, blacklist=alreadyUsed)
      self.logger.info(f'Old move: ID {defaultMove["move"]} - AT LEVEL {defaultMove["level"]}')
      self.logger.info(f'New move: ID {randomMove["id"]}')
      randomizedLearnset.append({**defaultMove, "move": randomMove["id"]})
      alreadyUsed.append(randomMove["id"])

    return randomizedLearnset

  def getRandomType(self, blacklist: list = []):
    typesIds = [typeId for typeId in list(range(18)) if typeId not in blacklist]
    return self.getRandomValue(items=typesIds)

  def getRandomEvolutions(self, evoStage: int, defaultEvolutions: list, options: dict):
    randomizedEvolutions = []
    
    evolutionOptions = options.copy()
    nextEvoStage = None

    if options["keepEvoStage"]:
      if evoStage == 1:
        nextEvoStage = 2
      else:
        nextEvoStage = 3

    if options["legendaryEvo"]:
      evolutionOptions["legendary"] = True

    if options["paradoxEvo"]:
      evolutionOptions["paradox"] = True

    for evolution in defaultEvolutions:
      evolutionData = self.getPokemonPersonalData(devId=evolution["species"])
      similarStats = False
      growthRate = None
      typesIds = None

      if options["evoSameStats"]:
        similarStats = True

      if options["evoGrowthRate"]:
        growthRate= evolutionData["xp_growth"]

      if options["evoType"]:
        typesIds = [evolutionData["type_1"], evolutionData["type_2"]]

      self.preparePokemonFilteredList(options=options, typesIds=typesIds, growthRate=growthRate, evoStage=nextEvoStage)
      randomEvolution = self.getRandomPokemon(oldPkmId=evolutionData["species"]["model"], similarStats=similarStats)

      randomizedEvolutions.append({
        **evolution,
        "species": randomEvolution["dexId"]
      })

      self.logger.info(f'Old Evolution ID {evolutionData["species"]["model"]}')
      self.logger.info(f'New Evolution ID {randomEvolution["dexId"]}')

    return randomizedEvolutions

  def getEqualizedCatchRateValue(self, options: dict):
    maxCatchRate = 255 # 100% catch rate
    minCatchRate = 3 # Beldum family

    rateValue = options["equalizedCatchRateValue"]

    if (rateValue > 100):
      rateValue = 100
    if (rateValue < 0):
      rateValue = 0

    generalCatchRate = math.floor(maxCatchRate * (rateValue/100))

    if (generalCatchRate < minCatchRate):
      generalCatchRate = minCatchRate

    return generalCatchRate

  def getRandomizedPokemonList(self, options: dict = None):
    self.logger.info('Starting logs for Pokemon Personal Data Randomizer')

    randomizedPokemonList = []
    totalItems = len(self.personalData["entry"])
    equalizedCatchRate = 0

    if options["equalizedCatchRate"]:
      if not isinstance(options["equalizedCatchRateValue"], int):
        options["equalizedCatchRate"] = False
      else:
        equalizedCatchRate = self.getEqualizedCatchRateValue(options=options)

    for pokemon in self.personalData["entry"]:
      if not options["fullPokeDex"] and not pokemon["is_present"]:
        randomizedPokemonList.append(pokemon)
        continue

      devPkm = self.getPokemonDev(dexId=pokemon["species"]["model"])
      self.logger.info(f'Randomizing data for pokemon: ID: {devPkm["dexId"]} - NAME: {devPkm["name"]} - FORM: {pokemon["species"]["form"]}')

      randomizedPokemon = {
        **pokemon
      }

      if options["abilities"]:
        # Randomizing Abilities
        self.logger.info(f'Original Abilities: A:{randomizedPokemon["ability_1"]}, B:{randomizedPokemon["ability_2"]}, H: {randomizedPokemon["ability_3"]}')
        defaultAbilities = [randomizedPokemon["ability_1"], randomizedPokemon["ability_2"], randomizedPokemon["ability_3"]]
        randomizedPokemon["ability_1"] = self.getRandomizedAbility(blacklist=defaultAbilities)
        randomizedPokemon["ability_2"] = self.getRandomizedAbility(blacklist=defaultAbilities+[randomizedPokemon["ability_1"]])
        randomizedPokemon["ability_3"] = self.getRandomizedAbility(blacklist=defaultAbilities+[randomizedPokemon["ability_1"], randomizedPokemon["ability_2"]])
        self.logger.info(f'New Abilities: A:{randomizedPokemon["ability_1"]}, B:{randomizedPokemon["ability_2"]}, H: {randomizedPokemon["ability_3"]}')

      if options["tm"]:
        # Randomizing TM compatibility
        randomizedPokemon["tm_moves"] = self.getRandomizedTMList(default=randomizedPokemon["tm_moves"])

      if options["learnset"]:
        # Randomizing Pool of moves the pokemon will learn by level
        self.logger.info(f'Randomizing Learnset')
        randomizedPokemon["levelup_moves"] = self.getRandomizedLearnset(defaultLearnset=randomizedPokemon["levelup_moves"], options=options)
        self.logger.info(f'Learnset randomized')

      if options["instantHatchEgg"]:
        # Egg Hatching just need 1 cycle
        randomizedPokemon["egg_hatch_steps"] = 1

      if options["randomBaseStats"]:
        # Randomize the distribution of baseStats
        randomStats = self.getRandomBaseStats(pkmPersonalData=randomizedPokemon)
        self.logger.info(f'Original Base Stats: {randomizedPokemon["base_stats"]}')
        self.logger.info(f'New randomized Base Stats: {randomStats}')
        randomizedPokemon["base_stats"] = randomStats

      if options["types"]:
        # Randomize the types of the pokemon
        isMonotype = randomizedPokemon["type_1"] == randomizedPokemon["type_2"]
        randomType = self.getRandomType()
        randomizedPokemon["type_1"] = randomType

        if isMonotype:
          randomizedPokemon["type_2"] = randomType
        else:
          randomType = self.getRandomType(blacklist=[randomizedPokemon["type_1"]])
          randomizedPokemon["type_2"] = randomType

      if options["evolutions"]:
        randomEvolution = self.getRandomEvolutions(evoStage=randomizedPokemon["evo_stage"], defaultEvolutions=randomizedPokemon["evo_data"], options=options)
        randomizedPokemon["evo_data"] = randomEvolution

      if options["equalizedCatchRate"]:
        randomizedPokemon["catch_rate"] = equalizedCatchRate

      randomizedPokemonList.append(randomizedPokemon)
      self.pokemonProgress = math.floor((len(randomizedPokemonList)/totalItems)*100)
      print(f'Processing: Pokemon Data {self.pokemonProgress}% / 100%', end='\r')
      updateProgress(value=self.pokemonProgress, title="Processing: Pokemon Data")

    self.logger.info('Closing logs for Pokemon Personal Data Randomizer')
    return randomizedPokemonList
