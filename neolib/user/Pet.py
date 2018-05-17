""":mod:`Pet` -- Represents a Neopet

.. module:: Pet
   :synopsis: Represents a Neopet
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""


import re


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
        self.species = pet_info['species']
        self.health = pet_info['health']
        self.mood = pet_info['mood']
        self.hunger = pet_info['hunger']
        self.age = pet_info['age']
        self.level = pet_info['level']


def get_pet_names(pets_div):
    wrapper_div = pets_div.find('div', id='bxwrap')
    # NOTE: i could just use these links
    links = [a['href'] for a in wrapper_div.find_all('a')]
    names = [re.search('.*pet=([^"]+)', l).groups(0)[0] for l in links]
    return names


def get_pets(usr):
    userlookup = usr.getPage('http://www.neopets.com/userlookup.phtml?user={}'.format(usr.username))
    # parse out petnames using div id=userneopets
    pets_div = userlookup.find('div', id='userneopets')

    pet_names = get_pet_names(pets_div)
    for pet_name in pet_names:
        # another option is using quickref.phtml, div content, each div has id "petname_details"
        # lookups do NOT include hunger, happiness
        petlookup = usr.getPage('http://www.neopets.com/petlookup.phtml?pet={}'.format(pet_name))

    # NOTE: this gives way more info than the summary active pet sidebar module (shrug)
    return pet_names
