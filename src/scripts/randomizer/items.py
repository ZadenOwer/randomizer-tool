# randomizer/items.py

import random

class ItemRandomizer:

  itemData = {}
  itemList = {}
  itemsByType = {}

  bannedFieldPocket = {
    'FPOCKET_PICNIC', # Skip all the picnic items
  }

  def __init__(self, data) -> None:
    self.itemData = data["itemData"]
    self.itemList = data["itemList"]

    for item in self.itemData["values"]:
      if item['SetToPoke'] and item['FieldPocket'] not in self.bannedFieldPocket:
        item_type = item['ItemType']
        if item_type not in self.itemsByType:
          self.itemsByType[item_type] = []
        self.itemsByType[item_type].append(item)

  def getRandomItem(self):
    # itemTypesWeighted helps randomize the type of item that it will be used
    itemTypesWeighted = ['ITEMTYPE_NUTS', 'ITEMTYPE_NUTS', 'ITEMTYPE_NUTS', 'ITEMTYPE_NUTS', 'ITEMTYPE_NUTS', 'ITEMTYPE_NUTS', 'ITEMTYPE_NUTS', 'ITEMTYPE_NUTS', 'ITEMTYPE_NUTS', 'ITEMTYPE_NONE', 'ITEMTYPE_NONE', 'ITEMTYPE_NONE', 'ITEMTYPE_NONE', 'ITEMTYPE_NONE', 'ITEMTYPE_NONE', 'ITEMTYPE_NONE', 'ITEMTYPE_NONE', 'ITEMTYPE_NONE', 'ITEMTYPE_DRUG', 'ITEMTYPE_DRUG', 'ITEMTYPE_DRUG', 'ITEMTYPE_DRUG', 'ITEMTYPE_DRUG', 'ITEMTYPE_DRUG', 'ITEMTYPE_BALL', 'ITEMTYPE_BALL', 'ITEMTYPE_BALL', 'ITEMTYPE_BALL', 'ITEMTYPE_BALL', 'ITEMTYPE_BALL', 'ITEMTYPE_WAZA', 'ITEMTYPE_WAZA', 'ITEMTYPE_WAZA', 'ITEMTYPE_WAZA', 'ITEMTYPE_WAZA', 'ITEMTYPE_WAZA']
    itemType = random.choice(itemTypesWeighted)

    itemsSubGroup = self.itemsByType.get(itemType, [])

    itemRaw = random.choice(itemsSubGroup)
    item: dict = self.itemList.get(itemRaw['Id'], self.itemList.get("0"))

    return item