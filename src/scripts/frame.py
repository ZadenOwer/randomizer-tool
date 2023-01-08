# frame.py
import os

import PySimpleGUI as sg

LAYOUT_SIZE = (810, 800) # (WIDTH, HEIGHT)
COLUMN_SIZE = (810, 600) # (WIDTH, HEIGHT)

DEFAULT_FONT_FAMILY = ''

TITLE_FONT = ('Courier', 24, 'bold')
HEADER_FONT = ('', 18)
INPUT_FONT = (DEFAULT_FONT_FAMILY, 14, 'bold')
TEXT_FONT = (DEFAULT_FONT_FAMILY, 12)
COPYRIGHT_FONT = (DEFAULT_FONT_FAMILY, 12, 'italic')

BG_COLOR = "#7c8487"
WHITE_COLOR = "#FFFFFF"

DANGER_COLOR = "#894103"

ON_CLOSE = sg.WIN_CLOSED

window = sg.Window(f"Randomizer {os.environ.get('VERSION')}", size=LAYOUT_SIZE, background_color=BG_COLOR)

def getAreasLayout(optionsValues: dict):
  LAYOUT_HEADER = [[sg.Text("Areas/Spawn Options", font=HEADER_FONT, background_color=BG_COLOR)]]

  RANDOMIZE_CHECKBOX = [
    [
      # Input
      sg.Check("Randomize Spawns", key="areasSpawnRandomized", font=INPUT_FONT, background_color=BG_COLOR, default=optionsValues["areasSpawnRandomized"]),
    ],
    # Description
    [
      sg.Text("Randomize the spawns of each pokemon.", font=TEXT_FONT, background_color=BG_COLOR),
    ],
    # Sub Description
    [
      sg.Text("Note: There'r scripted pokemon that always spawn in certain locations, such as Lechonk of the catch tutorial.", font=TEXT_FONT, text_color=DANGER_COLOR, background_color=BG_COLOR),
    ],
    [
      sg.Text("or the pokemon from cinematics.", font=TEXT_FONT, text_color=DANGER_COLOR, background_color=BG_COLOR),
    ],
  ]
  
  SIMILAR_STATS_CHECKBOX = [
    [
      # Input
      sg.Check("Similar Base Stats", key="similarStats", font=INPUT_FONT, background_color=BG_COLOR, default=optionsValues["similarStats"]),
    ],
    [
      # Description
      sg.Text("The random pokemon will have similar base stats to the original pokemon,", font=TEXT_FONT, background_color=BG_COLOR),
    ],
    [
      # Sub description
      sg.Text("this will affect initials and the overworld pokemon, if they're randomized (trainers have they own option).", font=TEXT_FONT, background_color=BG_COLOR),
    ],
    [
      # Sub description
      sg.Text("Note: The tool will attempt 30 times to get one, if fails, will take the last random pokemon validated", font=TEXT_FONT, text_color=DANGER_COLOR, background_color=BG_COLOR, auto_size_text=True),
    ]
  ]

  INITIALS_CHECKBOX = [
    [
      # Input
      sg.Check("Initials", key="initials", font=INPUT_FONT, background_color=BG_COLOR, default=optionsValues["initials"]),
    ],
    # Description
    [
      sg.Text("The initials will be random.", font=TEXT_FONT, background_color=BG_COLOR),
    ],
    # Sub description
    [
      sg.Text("Note: You can't see the models neither the names of the randomized ones.", font=TEXT_FONT, text_color=DANGER_COLOR, background_color=BG_COLOR),
    ],
    [
      sg.Text("This because their names and models are scripted for the start of the game, until you put one on your team", font=TEXT_FONT, text_color=DANGER_COLOR, background_color=BG_COLOR)
    ],
    [
      sg.Text("If you check this option an additional file 'starters.json' will be generated with the Dex Ids of the real starters", font=TEXT_FONT, text_color=DANGER_COLOR, background_color=BG_COLOR)
    ],
  ]

  ITEMS_CHECKBOX = [
    [
      # Input
      sg.Check("Items", key="items", font=INPUT_FONT, background_color=BG_COLOR, default=optionsValues["items"]),
    ],
    # Description
    [
      sg.Text("Try to put an random item on every pokemon type.", font=TEXT_FONT, background_color=BG_COLOR),
    ],
    # Sub description
    [
      sg.Text("Note: Pokemon of the same type will hold the same item", font=TEXT_FONT, text_color=DANGER_COLOR, background_color=BG_COLOR),
    ],
    [
      sg.Text("Ex: All the Meowth with have a pokeball.", font=TEXT_FONT, text_color=DANGER_COLOR, background_color=BG_COLOR)
    ]
  ]

  FULL_POKEDEX_CHECKBOX = [
    [
      # Input
      sg.Check("Full Pokedex", key="fullPokeDex", font=INPUT_FONT, background_color=BG_COLOR, default=optionsValues["fullPokeDex"]),
    ],
    [
      # Description
      sg.Text("Use the whole pokedex instead of the Paldean Dex.", font=TEXT_FONT, background_color=BG_COLOR),
    ]
  ]

  LEGENDARIES_CHECKBOX = [
    [
      # Input
      sg.Check("Legendaries", key="legendaries", font=INPUT_FONT, background_color=BG_COLOR, default=optionsValues["legendaries"]),
    ],
    [
      # Description
      sg.Text("Legendary Pokemon can spawn at the overworld like normal pokemon.", font=TEXT_FONT, background_color=BG_COLOR),
    ],
    # Sub description
    [
      sg.Text("If similar stats is checked, will reduce the probably of powerful legendaries at low level too.", font=TEXT_FONT, text_color=DANGER_COLOR, background_color=BG_COLOR),
    ]
  ]

  PARADOX_CHECKBOX = [
    [
      # Input
      sg.Check("Paradox", key="paradox", font=INPUT_FONT, background_color=BG_COLOR, default=optionsValues["paradox"]),
    ],
    [
      # Description
      sg.Text("Paradox Pokemon can spawn at the overworld like normal pokemon.", font=TEXT_FONT, background_color=BG_COLOR),
    ],
    # Sub description
    [
      sg.Text("If similar stats is checked, will reduce the probably of powerful paradox at low level too.", font=TEXT_FONT, text_color=DANGER_COLOR, background_color=BG_COLOR),
    ]
  ]

  # layout = LAYOUT_HEADER + RANDOMIZE_CHECKBOX + FULL_POKEDEX_CHECKBOX + SIMILAR_STATS_CHECKBOX + INITIALS_CHECKBOX + ITEMS_CHECKBOX + LEGENDARIES_CHECKBOX + PARADOX_CHECKBOX
  layout = LAYOUT_HEADER + RANDOMIZE_CHECKBOX + SIMILAR_STATS_CHECKBOX + INITIALS_CHECKBOX + ITEMS_CHECKBOX + LEGENDARIES_CHECKBOX + PARADOX_CHECKBOX

  return layout

def getPokemonLayout(optionsValues: dict):
  LAYOUT_HEADER = [[sg.Text("Individual Pokemon Options", font=HEADER_FONT, background_color=BG_COLOR)]]

  ABILITIES_CHECKBOX = [
    [
      # Input
      sg.Check("Instant Hatch Eggs", key="instantHatchEgg", font=INPUT_FONT, background_color=BG_COLOR, default=optionsValues["instantHatchEgg"]),
    ],
    # Description
    [
      sg.Text("Just need 1 step to hatch any egg", font=TEXT_FONT, background_color=BG_COLOR),
    ]
  ]

  ABILITIES_CHECKBOX = [
    [
      # Input
      sg.Check("Abilities", key="abilities", font=INPUT_FONT, background_color=BG_COLOR, default=optionsValues["abilities"]),
    ],
    # Description
    [
      sg.Text("Every pokemon type will have a random ability.", font=TEXT_FONT, background_color=BG_COLOR),
    ],
    # Sub description
    [
      sg.Text("Note: Pokemon of the same type will have the same ability", font=TEXT_FONT, text_color=DANGER_COLOR, background_color=BG_COLOR),
    ],
    [
      sg.Text("Ex: All the Pikachu with have Overgrowth.", font=TEXT_FONT, text_color=DANGER_COLOR, background_color=BG_COLOR)
    ]
  ]

  TM_CHECKBOX = [
    [
      # Input
      sg.Check("TMs", key="tm", font=INPUT_FONT, background_color=BG_COLOR, default=optionsValues["tm"]),
    ],
    # Description
    [
      sg.Text("Change the compatibility of TMs for each pokemon type", font=TEXT_FONT, background_color=BG_COLOR),
    ],
    # Sub description
    [
      sg.Text("Note: Pokemon of the same type will have the same TM compatibility", font=TEXT_FONT, text_color=DANGER_COLOR, background_color=BG_COLOR),
    ]
  ]

  MOVES_CHECKBOX = [
    [
      # Input
      sg.Check("Learnset", key="learnset", font=INPUT_FONT, background_color=BG_COLOR, default=optionsValues["learnset"]),
    ],
    # Description
    [
      sg.Text("Randomize the moves that every pokemon type will learn at their respective levels", font=TEXT_FONT, background_color=BG_COLOR),
    ],
    # Sub description
    [
      sg.Text("Ex: All the Fuecoco will learn Thunderbolt at level 12.", font=TEXT_FONT, text_color=DANGER_COLOR, background_color=BG_COLOR),
    ]
  ]

  BASE_STATS_CHECKBOX = [
    [
      # Input
      sg.Check("Random Base Stats", key="randomBaseStats", font=INPUT_FONT, background_color=BG_COLOR, default=optionsValues["randomBaseStats"]),
    ],
    # Description
    [
      sg.Text("Randomize the base stats of every pokemon", font=TEXT_FONT, background_color=BG_COLOR),
    ],
    # Sub description
    [
      sg.Text("The total base stats will remain, but the distribution of each value will change", font=TEXT_FONT, text_color=DANGER_COLOR, background_color=BG_COLOR),
    ]
  ]

  layout = LAYOUT_HEADER + ABILITIES_CHECKBOX + TM_CHECKBOX + MOVES_CHECKBOX + BASE_STATS_CHECKBOX

  return layout

def getTrainersLayout(optionsValues: dict):
  LAYOUT_HEADER = [[sg.Text("Trainers Options", font=HEADER_FONT, background_color=BG_COLOR)]]

  RANDOMIZE_CHECKBOX = [
    [
      # Input
      sg.Check("Randomize Team", key="trainersRandomized", font=INPUT_FONT, background_color=BG_COLOR, default=optionsValues["trainersRandomized"]),
    ],
    # Description
    [
      sg.Text("Randomize the team of each trainer.", font=TEXT_FONT, background_color=BG_COLOR),
    ],
    # Sub Description
    [
      sg.Text("Note: The rival will have a random team each time you battle.", font=TEXT_FONT, text_color=DANGER_COLOR, background_color=BG_COLOR),
    ],
  ]

  SIMILAR_STATS_CHECKBOX = [
    [
      # Input
      sg.Check("Similar Stats", key="trainerSimilarStats", font=INPUT_FONT, background_color=BG_COLOR, default=optionsValues["trainerSimilarStats"]),
    ],
    [
      # Description
      sg.Text("Each pokemon on the team will have similar base stats to the original one.", font=TEXT_FONT, background_color=BG_COLOR),
    ],
    [
      # Sub description
      sg.Text("If force full team is checked, the new added pokemon will have similar stats to the previous one", font=TEXT_FONT, background_color=BG_COLOR),
    ],
    [
      # Sub description
      sg.Text("Note: If the pokemon fails to get a random pokemon with similar stats, the pokemon will be completly random (be aware)", font=TEXT_FONT, text_color=DANGER_COLOR, background_color=BG_COLOR, auto_size_text=True),
    ]
  ]

  TERACRISTALIZE_CHECKBOX = [
    [
      # Input
      sg.Check("Teracristalize", key="trainerTeracristalize", font=INPUT_FONT, background_color=BG_COLOR, default=optionsValues["trainerTeracristalize"]),
    ],
    # Description
    [
      sg.Text("Every trainer will attempt to teracristalize.", font=TEXT_FONT, background_color=BG_COLOR),
    ]
  ]

  LEGENDARIES_CHECKBOX = [
    [
      # Input
      sg.Check("Legendaries", key="trainerLegendaries", font=INPUT_FONT, background_color=BG_COLOR, default=optionsValues["trainerLegendaries"]),
    ],
    # Description
    [
      sg.Text("Trainers can have legendaries pokemon.", font=TEXT_FONT, background_color=BG_COLOR),
    ],
    # Sub description
    [
      sg.Text("If similar stats is checked, will reduce the probably of powerful legendaries at low level too.", font=TEXT_FONT, text_color=DANGER_COLOR, background_color=BG_COLOR),
    ]
  ]

  PARADOX_CHECKBOX = [
    [
      # Input
      sg.Check("Paradox", key="trainerParadox", font=INPUT_FONT, background_color=BG_COLOR, default=optionsValues["trainerParadox"]),
    ],
    # Description
    [
      sg.Text("Trainers can have paradox pokemon.", font=TEXT_FONT, background_color=BG_COLOR),
    ],
    # Sub description
    [
      sg.Text("If similar stats is checked, will reduce the probably of powerful paradox at low level too.", font=TEXT_FONT, text_color=DANGER_COLOR, background_color=BG_COLOR),
    ]
  ]

  FULL_TEAM_CHECKBOX = [
    [
      # Input
      sg.Check("Force Full Team", key="forceFullTeam", font=INPUT_FONT, background_color=BG_COLOR, default=optionsValues["forceFullTeam"]),
    ],
    # Description
    [
      sg.Text("Every trainer will have 6 pokemon on his team", font=TEXT_FONT, background_color=BG_COLOR),
    ],
    [
      sg.Text("The new added pokemon will have levels based on a calculation, 3 will have the lowest level, 2 an intermediate level and 1 the highest level", font=TEXT_FONT, background_color=BG_COLOR),
    ],
    # Sub description
    [
      sg.Text("If the trainer team is not randomized, this option will be ignored", font=TEXT_FONT, text_color=DANGER_COLOR, background_color=BG_COLOR),
    ]
  ]

  KEEP_RIVAL_INITIAL_CHECKBOX = [
    [
      # Input
      sg.Check("Keep Rival Initial", key="keepRivalInitial", font=INPUT_FONT, background_color=BG_COLOR, default=optionsValues["keepRivalInitial"]),
    ],
    # Description
    [
      sg.Text("If the initials were randomized, the rival will have the designed initial based on your choice", font=TEXT_FONT, background_color=BG_COLOR),
    ]
  ]

  KEEP_TYPE_CHECKBOX = [
    [
      # Input
      sg.Check("Keep Themed Trainers", key="keepGymType", font=INPUT_FONT, background_color=BG_COLOR, default=optionsValues["keepGymType"]),
    ],
    # Description
    [
      sg.Text("Randomize the pokemon of themed trainers (such as gym leaders) for others with same type", font=TEXT_FONT, background_color=BG_COLOR),
    ]
  ]

  ITEMS_CHECKBOX = [
    [
      # Input
      sg.Check("Trainers' Pokemon Items", key="trainersItems", font=INPUT_FONT, background_color=BG_COLOR, default=optionsValues["trainersItems"]),
    ],
    # Description
    [
      sg.Text("Try to put an item on every pokemon of every trainer", font=TEXT_FONT, background_color=BG_COLOR),
    ]
  ]

  COMPETITIVE_CHECKBOX = [
    [
      # Input
      sg.Check("Perfect IVs", key="competitivePkm", font=INPUT_FONT, background_color=BG_COLOR, default=optionsValues["competitivePkm"]),
    ],
    # Description
    [
      sg.Text("Every pokemon of every trainer will have perfect IVs on each stat (keeping the 30 IVs on a random stat)", font=TEXT_FONT, background_color=BG_COLOR),
    ]
  ]

  SHINY_INPUT = [
    [
      # Input
      sg.Input("", key="trainerShiniesRate", background_color=WHITE_COLOR, size=(12,1)),
      sg.Text("Shiny Rate (Value [0-100])", font=INPUT_FONT, background_color=BG_COLOR),
    ],
    # Description
    [
      sg.Text("Shiny rate for every pokemon of every trainer", font=TEXT_FONT, background_color=BG_COLOR),
    ],
    # Sub description
    [
      sg.Text("Note: If the value is lesser than 0 will be treated as 0, if the value is greater than 100, will be treated as 100,", font=TEXT_FONT, text_color=DANGER_COLOR, background_color=BG_COLOR, auto_size_text=True),
    ],
    [
      sg.Text("or if the value is not a number, will be ignored", font=TEXT_FONT, text_color=DANGER_COLOR, background_color=BG_COLOR, auto_size_text=True),
    ]
  ]

  FORCE_EVOLUTION_CHECKBOX = [
    [
      # Input
      sg.Check("Force Final Evolution", key="forceFinalEvolution", font=INPUT_FONT, background_color=BG_COLOR, default=optionsValues["forceFinalEvolution"]),
    ],
    # Description
    [
      sg.Text("Force every pokemon of every trainer be on they final evolution (if have) based on a value as a threshold", font=TEXT_FONT, background_color=BG_COLOR),
    ]
  ]

  EVOLUTION_CAP_INPUT = [
    [
      # Input
      sg.Input("", key="finalEvolutionCap", background_color=WHITE_COLOR, size=(12,1)),
      sg.Text("Force Evolution Threshold (Value [1-99])", font=INPUT_FONT, background_color=BG_COLOR),
    ],
    # Description
    [
      sg.Text("Pokemon with this level and above will be forced to swap for they final evolution", font=TEXT_FONT, background_color=BG_COLOR),
    ],
    # Sub description
    [
      sg.Text("Note: If the value is less than or equal to 0 or greather than or equal to 100, or if the value is not a number,", font=TEXT_FONT, text_color=DANGER_COLOR, background_color=BG_COLOR),
    ],
    [
      sg.Text("will be ignored", font=TEXT_FONT, text_color=DANGER_COLOR, background_color=BG_COLOR),
    ]
  ]

  layout = LAYOUT_HEADER + RANDOMIZE_CHECKBOX + SIMILAR_STATS_CHECKBOX + TERACRISTALIZE_CHECKBOX + LEGENDARIES_CHECKBOX + PARADOX_CHECKBOX + FULL_TEAM_CHECKBOX + KEEP_RIVAL_INITIAL_CHECKBOX + KEEP_TYPE_CHECKBOX + ITEMS_CHECKBOX + COMPETITIVE_CHECKBOX + SHINY_INPUT + FORCE_EVOLUTION_CHECKBOX + EVOLUTION_CAP_INPUT

  return layout

def changeStep(window: sg.Window, stepId: str):
  for itemKey in window.key_dict:
    item = window[itemKey]

    if not isinstance(item, sg.Column):
      continue
    
    if item.key == stepId:
      window[item.key].update(visible=True)
    else:
      window[item.key].update(visible=False)

def toggleLayoutButtons():
  window["spawnsStepButton"].update(disabled=(not window["spawnsStepButton"].Disabled))
  window["pokemonStepButton"].update(disabled=(not window["pokemonStepButton"].Disabled))
  window["trainerStepButton"].update(disabled=(not window["trainerStepButton"].Disabled))
  window["finalStepButton"].update(disabled=(not window["finalStepButton"].Disabled))
  window["randomizeButton"].update(disabled=(not window["randomizeButton"].Disabled))

def updateProgress(value = 0, key='-PROGRESS_BAR-', title: str=""):
  window["progressTitle"].update(title)
  window[key].update(value)

def getWindowFrame(optionsValues: dict):
  HEADER_TEXT = [sg.Text("Pokemon S/V Randomizer", font=TITLE_FONT, background_color=BG_COLOR)]

  LAYOUTS_BUTTONS = [
    sg.Button("Spawns", key='spawnsStepButton'),
    sg.Button("Pokemon", key='pokemonStepButton'),
    sg.Button("Trainers", key='trainerStepButton'),
    sg.Button("Final Step", key='finalStepButton'),
  ]

  DEVS_HELP = [
    [sg.Checkbox("Keep files generated (such as binaries and jsons)", key="keepFiles", default=optionsValues["keepFiles"], text_color=DANGER_COLOR, background_color=BG_COLOR)]
  ]

  RANDOMIZE_BUTTON = [[sg.Button("Randomize!", key="randomizeButton")]]

  NOTES = [
    [sg.Text("You should consider:", font=TEXT_FONT, background_color=BG_COLOR, text_color=DANGER_COLOR)],
    [sg.Text("* This only had been tested on Ryujinx Emulator with version 1.0.1 of the game", font=TEXT_FONT, background_color=BG_COLOR)],
    [sg.Text("* Pokemon from both version can spawn", font=TEXT_FONT, background_color=BG_COLOR)],
    [sg.Text("* Can spawn eggs (Shiny Lv. 0) on the overworld, but you can't do anything with them (as far I know)", font=TEXT_FONT, background_color=BG_COLOR)],
    [sg.Text("* Maybe the randomizer try to put an invalid item, so you may encounter pokemon without item", font=TEXT_FONT, background_color=BG_COLOR)],
    [sg.Text("* The raids still remain the same", font=TEXT_FONT, background_color=BG_COLOR)],
  ]

  PROGRESS_BAR = [
    [sg.Text("", key='progressTitle', font=TEXT_FONT, background_color=BG_COLOR, text_color=("Green"))],
    [sg.ProgressBar(100, orientation='h', size=(35, 20), border_width=4, key='-PROGRESS_BAR-', bar_color=("Blue", "White"))]
  ]

  COPYRIGHT = [
    [sg.Text("Author: ZadenOwer", font=COPYRIGHT_FONT, background_color=BG_COLOR)],
    [sg.Text(f"Version: {os.environ.get('VERSION')}", font=COPYRIGHT_FONT, background_color=BG_COLOR)]
  ]

  areasLayout = getAreasLayout(optionsValues)
  pokemonLayout = getPokemonLayout(optionsValues)
  trainersLayout = getTrainersLayout(optionsValues)

  finalLayout = [
    HEADER_TEXT,

    [
      sg.Column(areasLayout, key="spawns", background_color=BG_COLOR, size=COLUMN_SIZE, scrollable=True, vertical_scroll_only=True),
      sg.Column(pokemonLayout, key="pokemon", visible=False, background_color=BG_COLOR, size=COLUMN_SIZE),
      sg.Column(trainersLayout, key="trainers", visible=False, background_color=BG_COLOR, size=COLUMN_SIZE, scrollable=True, vertical_scroll_only=True),
      sg.Column(DEVS_HELP + RANDOMIZE_BUTTON + NOTES + PROGRESS_BAR, key="finalStep", visible=False, background_color=BG_COLOR, size=COLUMN_SIZE)
    ],
    
    LAYOUTS_BUTTONS,
    COPYRIGHT
  ]

  window.layout(finalLayout)

  return window