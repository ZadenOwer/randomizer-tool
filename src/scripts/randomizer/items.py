# randomizer/items.py

import math
import random

from src.scripts.frame import updateProgress

class ItemRandomizer:

  itemData = {}
  itemList = {}
  hiddenItemData = {}
  itemsByType = {}

  fieldItemsProgress = 0

  bannedFieldPocket = {
    'FPOCKET_PICNIC', # Skip all the picnic items
  }

  def __init__(self, data) -> None:
    self.itemData = data["itemdata_array_file"]
    self.itemList = data["item_list_file"]
    self.hiddenItemData = data["hidden_item_list_file"]

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
    item: dict = next((item for item in list(self.itemList.values()) if item["id"] == itemRaw['Id']), self.itemList.get("0"))
    return item

  def getRandomizedHiddenItemData(self):
    randomizedList = []

    totalItems = len(self.hiddenItemData["values"])

    for hiddenItem in self.hiddenItemData["values"]:
      for fieldKey in hiddenItem.keys():
        if "item_" not in fieldKey:
          continue

        if hiddenItem[fieldKey]["itemId"] == "ITEMID_NONE":
          continue

        randomItem = self.getRandomItem()

        hiddenItem[fieldKey] = {
          **hiddenItem[fieldKey],
          "itemId": randomItem["devName"]
        }

        if randomItem["id"] == 1:
          # If is a master ball, reduce spawn rate to 2%
          hiddenItem[fieldKey] = {
            **hiddenItem[fieldKey],
            "emergePercent": 2
          }

      randomizedList.append(hiddenItem)
      self.fieldItemsProgress = math.floor((len(randomizedList)/totalItems)*100)
      print(f'Processing: Hidden Items Data {self.fieldItemsProgress}% / 100%', end='\r')
      updateProgress(value=self.fieldItemsProgress, title="Processing: Hidden Items Data")

    return randomizedList