import os

import PySimpleGUI as sg

LAYOUT_SIZE = (800, 800) # (WIDTH, HEIGHT)

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
      sg.Text("Note: There'r scripted pokemon that always spawn of certain locations, such as the Lechonk of the catch tutorial.", font=TEXT_FONT, text_color=DANGER_COLOR, background_color=BG_COLOR),
    ],
    [
      sg.Text("or the pokemon from cinematics.", font=TEXT_FONT, text_color=DANGER_COLOR, background_color=BG_COLOR),
    ],
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
      sg.Text("This because their names and models are scripted for the initial part of the game until you put one on your team", font=TEXT_FONT, text_color=DANGER_COLOR, background_color=BG_COLOR)
    ],
    [
      sg.Text("If you check this option an additional file 'starts.json' will be generated with the names of the real starters", font=TEXT_FONT, background_color=BG_COLOR)
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
    ]
  ]

  # layout = LAYOUT_HEADER + FULL_POKEDEX_CHECKBOX + ITEMS_CHECKBOX + LEGENDARIES_CHECKBOX + PARADOX_CHECKBOX
  layout = LAYOUT_HEADER + RANDOMIZE_CHECKBOX + INITIALS_CHECKBOX + ITEMS_CHECKBOX + LEGENDARIES_CHECKBOX + PARADOX_CHECKBOX

  return layout

def getPokemonLayout(optionsValues: dict):
  LAYOUT_HEADER = [[sg.Text("Pokemon Options", font=HEADER_FONT, background_color=BG_COLOR)]]

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

  layout = LAYOUT_HEADER + ABILITIES_CHECKBOX + TM_CHECKBOX + MOVES_CHECKBOX

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

  FULL_TEAM_CHECKBOX = [
    [
      # Input
      sg.Check("Force Full Team", key="forceFullTeam", font=INPUT_FONT, background_color=BG_COLOR, default=optionsValues["forceFullTeam"]),
    ],
    # Description
    [
      sg.Text("Every trainer will have 6 pokemon on his team", font=TEXT_FONT, background_color=BG_COLOR),
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

  layout = LAYOUT_HEADER + RANDOMIZE_CHECKBOX + TERACRISTALIZE_CHECKBOX + FULL_TEAM_CHECKBOX + KEEP_TYPE_CHECKBOX + ITEMS_CHECKBOX + COMPETITIVE_CHECKBOX + SHINY_INPUT + FORCE_EVOLUTION_CHECKBOX + EVOLUTION_CAP_INPUT

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

def getWindowFrame(optionsValues: dict):
  HEADER_TEXT = [sg.Text("Pokemon S/V Randomizer", font=TITLE_FONT, background_color=BG_COLOR)]

  LAYOUTS_BUTTONS = [
    sg.Button("Step 1"),
    sg.Button("Step 2"),
    sg.Button("Step 3"),
    sg.Button("Step 4"),
  ]

  DEVS_HELP = [
    [sg.Checkbox("Keep files generated (such as binaries and jsons)", key="keepFiles", default=optionsValues["keepFiles"], text_color=DANGER_COLOR, background_color=BG_COLOR)]
  ]

  RANDOMIZE_BUTTON = [[sg.Button("Randomize!")]]

  NOTES = [
    [sg.Text("You should consider:", font=TEXT_FONT, background_color=BG_COLOR, text_color=DANGER_COLOR)],
    [sg.Text("* This only had been tested on Ryujinx Emulator", font=TEXT_FONT, background_color=BG_COLOR)],
    [sg.Text("* Pokemon from both version can spawn", font=TEXT_FONT, background_color=BG_COLOR)],
    [sg.Text("* Can spawn eggs (Shiny Lv. 0) on the overworld, but you can't do anything with them (as far I know)", font=TEXT_FONT, background_color=BG_COLOR)],
    [sg.Text("* Maybe the randomizer try to put an invalid item, so you may encounter pokemon without item", font=TEXT_FONT, background_color=BG_COLOR)],
    [sg.Text("* The raids still remain the same", font=TEXT_FONT, background_color=BG_COLOR)],
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
      sg.Column(areasLayout, key="step1", background_color=BG_COLOR),
      sg.Column(pokemonLayout, key="step2", visible=False, background_color=BG_COLOR),
      sg.Column(trainersLayout, key="step3", visible=False, background_color=BG_COLOR),
      sg.Column(DEVS_HELP + RANDOMIZE_BUTTON + NOTES + COPYRIGHT, key="step4", visible=False, background_color=BG_COLOR)
    ],
    
    LAYOUTS_BUTTONS
  ]

  window = sg.Window(f"Randomizer {os.environ.get('VERSION')}", finalLayout, size=LAYOUT_SIZE, background_color=BG_COLOR)

  return window