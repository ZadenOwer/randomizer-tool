import os

import PySimpleGUI as sg

LAYOUT_SIZE = (800, 600) # (WIDTH, HEIGHT)

DEFAULT_FONT_FAMILY = ''

TITLE_FONT = ('Courier', 24)
INPUT_FONT = (DEFAULT_FONT_FAMILY, 14, 'bold')
TEXT_FONT = (DEFAULT_FONT_FAMILY, 12)
COPYRIGHT_FONT = (DEFAULT_FONT_FAMILY, 12, 'italic')

BG_COLOR = "#7c8487"

DANGER_COLOR = "#894103"

ON_CLOSE = sg.WIN_CLOSED

def getAreasLayout(optionsValues: dict):
  
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

  layout = ITEMS_CHECKBOX + LEGENDARIES_CHECKBOX + PARADOX_CHECKBOX

  return layout

def getPokemonLayout(optionsValues: dict):
  
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

  layout = ABILITIES_CHECKBOX + TM_CHECKBOX + MOVES_CHECKBOX

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
  ]

  RANDOMIZE_BUTTON = [[sg.Button("Randomize!")]]

  NOTES = [
    [sg.Text("You should consider:", font=TEXT_FONT, background_color=BG_COLOR, text_color=DANGER_COLOR)],
    [sg.Text("* This only had been tested on Ryujinx Emulator", font=TEXT_FONT, background_color=BG_COLOR)],
    [sg.Text("* Pokemon from both version can spawn", font=TEXT_FONT, background_color=BG_COLOR)],
    [sg.Text("* Can spawn eggs (Shiny Lv. 0) on the overworld, but you can't do anything with them (as far I know)", font=TEXT_FONT, background_color=BG_COLOR)],
    [sg.Text("* Maybe the randomizer try to put an invalid item, so you may encounter pokemon without item", font=TEXT_FONT, background_color=BG_COLOR)],
    [sg.Text("* Just the overworld pokemon are randomized, trainers and raids still remain the same", font=TEXT_FONT, background_color=BG_COLOR)],
  ]

  COPYRIGHT = [
    [sg.Text("Author: ZadenOwer", font=COPYRIGHT_FONT, background_color=BG_COLOR)],
    [sg.Text(f"Version: {os.environ.get('VERSION')}", font=COPYRIGHT_FONT, background_color=BG_COLOR)]
  ]

  areasLayout = getAreasLayout(optionsValues)
  pokemonLayout = getPokemonLayout(optionsValues)

  finalLayout = [
    HEADER_TEXT,

    [
      sg.Column(areasLayout, key="step1", background_color=BG_COLOR),
      sg.Column(pokemonLayout, key="step2", visible=False, background_color=BG_COLOR),
      sg.Column(RANDOMIZE_BUTTON + NOTES + COPYRIGHT, key="step3", visible=False, background_color=BG_COLOR)
    ],
    
    LAYOUTS_BUTTONS
  ]

  window = sg.Window(f"Randomizer {os.environ.get('VERSION')}", finalLayout, size=LAYOUT_SIZE, background_color=BG_COLOR)

  return window