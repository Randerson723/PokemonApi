import requests, pprint, json
pp = pprint.PrettyPrinter(indent=4)



#Object that takes in data and reorganizes in the form specified



class Pokemon:
    def __init__(self, name= None, abilities= None, types= None, height=None, weight=None):
        self.name = name
        if abilities is None:
            self.abilities = []
            if types is None:
                self.types = []
            self.height = height
            self.weight = weight

    def from_dict(self, data):
        for field in ['name', 'abilities', 'types','height', 'weight']:
            if field in data:
                setattr(self, field, data[field])


    def __repr__(self):
        return f'<Pokemon>: {self.name}'

    def __str__(self):
        return f'{self.name}'
    


# Class that runs program and gathers Data for API
class Index:
    _list = []
    


    @classmethod
    def show(cls):
        print('!#' * 40)
        for idx, p in enumerate(cls._list):
            print(f'{idx+1}: {p}')          #Prints the String of the Pokemon Object
        print('!#' * 40)



    @classmethod
    def instructions(cls):
        print(""" Type 'Show' to view Index
                  Type 'quit' to exit the Index
                  Type 'sort' to view a categorized Index
""")
    @classmethod
    def add(cls, pokemon_name):
        #Check to see if Pokemon has already been added to Index
        print(pokemon_name)
        #If the Pokemon is in the Index
        if cls._list:
            for p in cls._list:
                if pokemon_name.title() == p.name:
                    input("That Pokemon already exists. Please choose another")
                    return
        try:
            #connect to the API
            print("Please wait while we populate the Index")
            r = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}').json()
        #Create new Pokemon
            print(r)
        #Abilities is set to grab both keys within the Dictionary
        #Types is to grab both keys in Dictionary
            p = Pokemon()
            data_dict = {
            'name': r['name'].title(),
            'abilities': [a['ability']['name'].title()for a in r['abilities']],
            'types':[t['type']['name'].title() for t in r['types']],
            'height':r['height'],
            'weight':r['weight'],
            }
            print("Dictionary complete")
            p.from_dict(data_dict)
            print("Pokemon Created")
            #Add New Pokemon
            cls._list.append(p)
        
        except Exception as error:
            print(error)
            input("Error populating the Index, Try Again.")
                   
        
        
    
    @classmethod
    def sort(cls):
    #Build a dictionary that categorizes the Pokemon into types
        sorted_dict = {}

        for p in cls._list:
            #while inside the player, take a look at their types list
            for t in p.types:
                #if Pokemon type hasn't been found in sorted_dict
                if t not in sorted_dict:
                    #create new key and set as empty dictionary
                    sorted_dict[t] = {}
            for p in cls._list:
                # if Pokemon has multiple types
                for t in p.types:
                    #create a Pokemon dictionary that will show from Index
                    if p.name not in sorted_dict[t]:
                        poke_data = {
                            p.name: {
                                'abilities': p.abilities,
                                'height': p.height,
                                'weight': p.weight,
                            }
                        }
                        sorted_dict[t].update(poke_data)
                    else:
                        print('That Pokemon already exists')
            pp.pprint(sorted_dict)
    
    @classmethod
    def run(cls):
        #Flag to end the program
        done = False
        

        while not done:

            cls.instructions()

            pokemon_choice = input("Type in the name of the Pokemon to add them to the Index.  Type 'quit' to exit the program")
            if pokemon_choice == 'quit':
                done = True
            elif pokemon_choice == 'show':
                cls.show()
                input("Press 'Enter' to continue")
            elif pokemon_choice == 'sort':
                cls.sort()
                input("Press 'ENTER' to continue")
            else:
                #Send API Request for Pokemon
                
                #Put Pokemon in Index
                cls.add(pokemon_choice)

Index.run()


#Pokemon(name = 'charizard')

