# Hearthstone Card Search APP

## ER Diagram
![ERD](images/Diagram.png?raw=true "ER Diagram")

## Methods

  ### Creates

    1. Insert a Card
      - when inserting also insert into bridge tables the class/effect or set (if information is avail)
        - if PROVIDED class/effect/set does not exist in corresponding table -> Don't Insert
    2. Insert a Class
      - cards without a class are neutral
    3. Insert an Effect
      - cards without an effect are vanilla
    4. Insert a Set
      - cards withoug a set are from base set (TBD)
    5. Insert a relation into CardClass bridge table
    6. Insert a relation into CardEffect bridge table
    7. Insert a relation into CardSet bridge table
    
  ### Reads
  
    1. Find 1 Card based on ID or Name
    2. Find all Cards
    3. Find all Cards by Effect
    4. Find all Cards by Class
    5. Find all Cards by Set
    6. List out all Effects
    7. List out all Classes
    8. List out all Sets
    9. Find cards using a combination of Effects, Classes or Sets (TBD)
    
  ### Updates
    
    There are 2 types of updateds
    1. Replace
      - Replace everything about an EXISTING Card by ID (or Name)
        -Must update Bridge tables
    2. Append
      - Add another relation to the corresponding bridge table
      
  ### Deletes
  
    1. Delete Card by ID or Name
      - must do upkeep on bridge tables
    2. Delete Class,Effect or Set by ID or Name
      - must do upkeep on bridge table
