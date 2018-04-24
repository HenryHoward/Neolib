""":mod:`Pet` -- Represents a Neopet

.. module:: Pet
   :synopsis: Represents a Neopet
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""


# TODO: add ways to get info for all pets of a user

class Pet:
    
    """Represents a Neopet - assuming we can get this information on every page
    for the primary pet.
    
    Attributes
       name (str) -- Neopet name
       species (str) -- Neopet species
       health (str) -- Neopet health
       mood (str) -- Neopet mood
       hunger (str) -- Neopet hunger level
       age (str) -- Neopet age
       level (str) -- Neopet level
        
    Example
       >>> pet = Pet("somename")
    """
    
    name = ""
    species = ""
    health = ""
    mood = ""
    hunger = ""
    age = ""
    level = ""

    def __create_petinfo_map(self, pet_info):
        table = pet_info.find('table')
        pinfo = {}
        for tr in table.findAll('tr'):
            td = tr.findAll('td')
            left = td[0].text.lower().strip()[:-1]
            right = td[1].text.lower().strip()
            pinfo[left] = right
        return pinfo

    def __init__(self, usr):
        page = usr.getPage('http://www.neopets.com') # todo: maybe use pet info page? for now just whatever.
        # assuming we can use usr.getPage, we can load at least the primay pet's data
        pet_sidebar = page.find_all('div', class_='sidebarModule')[0]
        self.name = pet_sidebar.find('td', class_='sidebarHeader medText').text
        pet_info = self.__create_petinfo_map(
                pet_sidebar.find('td', class_='activePetInfo'))
        print pet_info
        self.species = pet_info['species']
        self.health = pet_info['health']
        self.mood = pet_info['mood']
        self.hunger = pet_info['hunger']
        self.age = pet_info['age']
        self.level = pet_info['level']

