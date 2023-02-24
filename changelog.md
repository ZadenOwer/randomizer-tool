# 1.1.8 - 02/23/2023

- Fixed an issue when the option hidden items was market, the randomizer didn't create correctly the files
- Keep the random abilities algonside the evolutions implemented
- Keep the random types algonside the evolutions implemented
- Keep the random TMs compatibility algonside the evolutions implemented
- Keep the random Learnset algonside the evolutions implemented

# 1.1.7 - 02/06/2023

- Fixed an issue when the option hidden items was not marked the randomizer throws an exception
- Fixed an issue on dex.json file to match the pokemon id with their DEX id instead of the Dev Id
- Fixed an issue where running locally the repository, throws an exception because the logs file don't exist
  
# 1.1.6 - 01/22/2023

- Fixed an issue on hidden items randomizer that make all items as ITEM_NONE
- Fixed an issue when force evolution was active, don't randomize the form of the evolution by a valid one 
- Fixed an issue were pokemon moves repeats on the learnset

# 1.1.5 - 01/22/2023

- Name of each pokemon added to the pokemon list
- Fixed relationship between dexID and devID (for personal data)
- Equalized Catch Rate implemented
- Hidden Items Fields randomizer implemented

# 1.1.4 - 01/09/2023

- Randomizer Script refactored to subdivide into classes
- Reimplemented the generation of random pokemon
- Reimplemented the calculation of similar stats
- New Option for Random Types
- New Option for Random Evolutions
- New Option for randomize the learnset based on the power and the original type of the move

# 1.1.3 - 01/08/2023

- Improvements on performance
- Clean up code
- Option for instant hatching eggs implemented
- Better User Feedback with progress bar
  
- # 1.1.2 - 01/06/2023

- Option for randomize the base stats values was implemented
- Improvement on the value randomization logic
  
- # 1.1.1 - 12/22/2022

- Fix on trainers' pkm with static moves

# 1.1.0 - 12/15/2022

- Logger implemented
- Validations on species ID and similar stats fixed

# 1.0.9 - 12/14/2022

- Option for check similar base stat when randomizing was implemented
- Option for keep the respective initial of the Rival Nemona/Mencía 

# 1.0.8 - 12/12/2022

- Evolutions data for every pokemon updated
- Excluded moves updated to the last list of excluded moves from 9th

# 1.0.7 - 12/08/2022

- Missing Paldean Dex entries added to the randomizer
- Fixed the pokemon forms randomizing

# 1.0.6 - 12/07/2022

- The window frame now is scrollable, to avoid getting stuck on the Step 3
- New way on the creation of the personal_array binary, this makes possible to not use the DLLs anymore
- Trainers' Pokemon sex change to "DEFAULT" value when randomizing them

# 1.0.5 - 12/06/2022

- Initials randomizer
- New randomizing options
- [Fix] All the trainers have full team

# 1.0.4 - 12/05/2022

Trainers randomizer:
- Trainer can use teracristalize
- Force Full Team
- Keep Important Trainers Type (Gym leader, Team Start Boss, Elite 4)
- Trainers' Pokemon held Items
- Trainers' Pokemon with perfect IVs
- Trainers' Pokemon Shiny Rate
- Force Final Evolution when Pokemon great or equal to a threshold level

# 1.0.3 - 12/04/2022

- Implemented Abilities Randomizer
- Implemented TM compatibility Randomizer
- Implemented Learnset Randomizer
- Option for keep the binary and jsons generated after the execution instead of deleted

# 1.0.2 - 12/02/2022

- New tool based on Python
- Implemented with a UI that can be packed as an .exe
- Implemented Items Randomizer
- Implemented Pokemon Spawn Randomizer
- Option for blacklist the legendaries and/or paradox pokemon out of the randomization

# 1.0.1 - 12/01/2022

- Trying to fix the problems of the 1.0.0, failed attempt, so this version of the tool was deprecated and deleted

# 1.0.0 - 12/01/2022

- First implementation on the tool
- Created on Javascript
- Cannot run efficiently on every PC
