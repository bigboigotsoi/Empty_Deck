# Flash-Carder: Flash Cards on Python!
  
First, you should provide the Card Data. You can either...

    A.  Let the Flash-Carder read all data from your own 
        'Card Data' type of file, held in the 'Your Cards' Folder.
        (and set 'FetchingDataFile' to True)

     B.  Hard Code in your FlashCard data into the 'AllCards' Array, in the format of...
    
        AllCards = [
                      ["Question 1s Title",
                       "Answer 1.1", "Answer 1.2"...],
                       
                        ["Question 2s Title",
                       "Answer 2.1", "Answer 2.2"...],
                       
                       ...
                   ]
                   
        (and set 'FetchingDataFile' to False).
    
To do Part A...

    A.1 Modify your copy of the 'Card Data' file to include your own data:

        Note...
        A.1.1   You can modify 'questionBullet' and 'answerBullet' to your liking.
        A.1.2   Use them appropiately as demonstrated with the Example Data
                already in the Card Data file, in order for loading to work.

    A.2 Modify the directory/name stored in the 
        'cardFile' variable to locate your card data file.

    A.3 Run the Flash-Carder and it should load your data!

Also, JC.py is just a module of handy functions I like to use, named after me. 
