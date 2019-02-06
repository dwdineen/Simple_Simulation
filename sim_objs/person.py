# TODO: need to add more to the person class
#  what things should they be able to do?
#  what are all of their characteristics?
import random, datetime
import os
from model import Model
from .sim_obj import SimObj
from definitions import RESOURCES_DIR, DEATH_PROBS, CHANCE_OF_DEATH, MALE, FEMALE, ETHNICITIES
from pathlib import Path
from collections import Iterable
import sim_objs.person_helpers.action as action
from sim_objs.person_helpers import Traits, Genes, State



class Person(SimObj):

    # Some class variables. These might be moved to a better home later. Where they are does
    # not really matter
    
    # List of all actions that must be evaluated every day, for every person
    required_actions = [
        action.Breed(),
    ] 

    # List of all optional actions that can be done and picked based on an optional_picking function
    optional_actions = [
        action.HitByACar()
    ]

    def __init__(self, name=None, genes=None, traits=None, state=None, age=0):

        self.genes = Genes(genes or {})
        self.traits = Traits(traits or {}, self.genes)
        self.state = State({State.NAME: name}, self.genes, self.traits)


    # I am making properties to easily access some of the more popular Person
    # genes/traits/state
    # I do not want to make a property for every property

    @property
    def name(self):
        return self.state[State.NAME]

    @property
    def days(self):
        return Model.get().time - self.state[State.DOB]

    @property
    def years(self):
        return (Model.get().time - self.state[State.DOB] / 365)

    @property
    def gender(self):
        return self.genes[Genes.GENDER]

    def update(self):
        """
        1. Go through list of all required actions. Any action that is a non-zero affinity is performed
        

        2. Use self.pick_optional_actions() to get a list of optional actions to perform. Keep executing the
           actions until done.
        
        TODO: Implement scheduled actions
        """

        # 1. Filter the required actions by affinity > 0
        reqs = [act for act in Person.required_actions if act.affinity(self) > 0]
              

        # apply each required action to Person
        for act in reqs: 
            reqs += (act.apply(self) or [])


        # 2. use pick_optional_action to get a list of optional_actions
        action_list = self.pick_optional_action()
        for act in action_list:
            action_list += (act.apply(self) or [])

    def pick_optional_action(self):
        """
        For now, just pick a single optional action randomly, weighted by affinity. This function needs to be improved.
        """

        def norm(li):
            return [float(i)/sum(li) for i in li]

        return random.choices(
                population = Person.optional_actions,
                weights    = norm([act.affinity(self) for act in Person.optional_actions]),
                k = 1
        )

    @staticmethod
    def pickName(gender):
        """
        Input: gender, one of : 'male' , 'female'
        Output: A random full name  (string)
        Example use:
        pickName('female') will return a female name as string.
        """

        def load_names(filename):
            """
            Input: Name of file that contains a single name per line (string)
            Output: List of all the names in file with \n removed from the end (string list)
            """
            namelist = []
            file_location = os.path.join(RESOURCES_DIR, filename)
            with open(file_location, 'r') as f:
                for line in f:
                    namelist.append(line.strip('\n'))
            return namelist
            
        if gender == MALE:
            firstnames = load_names('male_firstnames.txt')
        elif gender == FEMALE:
            firstnames = load_names('female_firstnames.txt')
        else:
            return "NO GENDER"
        lastnames = load_names('lastnames.txt')
        # Sizes of the firstnames and lastnames lists:
        first = random.choice(firstnames)
        last = random.choice(lastnames)
        fullname = ''.join((first,' ', last))
        return fullname

    def getInfo(self):
        if self.gender.lower() == "male":
            self.pronoun1 = "He"
            self.pronoun2 = "his"
        elif self.gender.lower() == "female":
            self.pronoun1 = "She"
            self.pronoun2 = "her"
        if self.state == "alive":
            print(f'{self.name} is {round(self.age, 3)} years old, is a {self.gender}, and is {self.ethnicity}. {self.pronoun1} is {self.height} meters tall, and {self.weight} kilograms. {self.pronoun1} will reach {self.pronoun2} reproductive age at {self.reproductive_age} years old.')
        elif self.state == "deceased":
            print(f'{self.name} died at age {round(self.age, 3)}, was a {self.gender}, and was {self.ethnicity}. {self.pronoun1} was {self.height} meters tall, and weighed {self.weight} kilograms. {self.pronoun2} cause of death was {self.death_cause}')
    
    def kill(self, cause):
        """
        Kills this person
        Input: Cause of death (string)
        """
        if self.state == 'alive':
            self.state = 'deceased'
            self.death_cause = cause

    def decide_fate(self):
        """
        Decides if person dies of some cause. CHANCE_OF_DEATH chance of coming close to death at a given day
        """
        if random.randint(1,1000) >= CHANCE_OF_DEATH:
            return None
        deathprobs = DEATH_PROBS[self.gender.lower()]
        for cause, prob in deathprobs.items():
            if random.randint(1, 100) <= round(prob['chance']*100 + prob['age_factor']*self.age):
                return cause
        return None    

    def get_age_string(self):
        if self.age < 1:
            return ' '.join((str(round(self.age * 365)),'days'))
        else:
            return ' '.join((str(round(self.age, 1)),'years')) 
        
    def update_old(self):
        if self.state == "alive":
            self.age = float(self.age)
            self.age += (1/365)
            cause_of_death = self.decide_fate()
            if cause_of_death:
                self.kill(cause_of_death)
                print(f'{self.name} has died due to {cause_of_death} at {self.get_age_string()} old.')

        parent1 = random.choice(Model.get().sim_objs)
        parent2 = random.choice(Model.get().sim_objs)
        while parent1 == parent2:
            parent2 = random.choice(Model.get().sim_objs)

        if parent1.gender != parent2.gender:
            if parent1.age >= parent1.reproductive_age and parent2.age >= parent2.reproductive_age:
                if random.randint(0, 100) <= 2:
                    Model.get().sim_objs.append(breed(parent1, parent2))
                    print(f"{parent1.name} and {parent2.name} gave birth to a baby {Model.get().sim_objs[-1].gender} named {Model.get().sim_objs[-1].name}.")

            # Should only print age when getInfo is called
            #if self.age < 1:
            #    print(f'{self.name} is {round(self.age * 365)} days old.')
            #else:
            #    print(f'{self.name} is {round(self.age, 1)} years old.')











