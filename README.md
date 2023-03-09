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
  ### Updates
  ### Deletes
