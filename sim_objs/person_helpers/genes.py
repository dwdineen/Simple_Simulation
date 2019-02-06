import random
from definitions import *

class Genes(dict):

    GENDER           = 0
    ETHNICITY        = 1
    REPRODUCTIVE_AGE = 2 # years
    ADULT_HEIGHT     = 3 # meters
    ADULT_WEIGHT     = 4 # kilograms

    def __init__(self, genes):
        super().__init__(self)

        self[Genes.GENDER] = genes.get(Genes.GENDER) or random.choice([MALE, FEMALE])
        self[Genes.ETHNICITY] = genes.get(Genes.ETHNICITY) or random.choice(ETHNICITIES)
        self[Genes.REPRODUCTIVE_AGE] = genes.get(Genes.REPRODUCTIVE_AGE)
        self[Genes.ADULT_HEIGHT] = genes.get(Genes.ADULT_HEIGHT)
        self[Genes.ADULT_WEIGHT] = genes.get(Genes.ADULT_WEIGHT)
        

        # Calculate Reproductive Age
        if not self[Genes.REPRODUCTIVE_AGE]:
            if self[Genes.GENDER] == MALE:
                self[Genes.REPRODUCTIVE_AGE] = round(random.uniform(13,17), 1)
            elif self[Genes.GENDER] == FEMALE:
                self[Genes.REPRODUCTIVE_AGE] = round(random.uniform(11,16), 1)

        # Calculate Adult Height
        if not self[Genes.ADULT_HEIGHT]:
            if self[Genes.GENDER] == MALE:
                self[Genes.ADULT_HEIGHT] = round(random.uniform(1.6,2.1), 1) # Height is in Meters.
            elif self[Genes.GENDER] == FEMALE:
                self[Genes.ADULT_HEIGHT] = round(random.uniform(1.5,1.9), 1) # Height is in Meters.

        # Calculate Adult Weight
        if not self[Genes.ADULT_WEIGHT]:
            if self[Genes.GENDER] == MALE:
                self[Genes.ADULT_WEIGHT] = round(random.uniform(50,110), 1) # Weight is in Kilograms
            elif self[Genes.GENDER] == FEMALE:
                self[Genes.ADULT_WEIGHT] = round(random.uniform(50,100), 1) # Weight is in Kilograms



    def to_list(self):
        """Returns list form of this dict"""
        return list(self.values())

    @staticmethod
    def convert_from_list(gene_list):
        """Converts list to dict, assumes that list is in correct order and complete. Dangerous"""

        genes = {}
        for x, i in enumerate(gene_list):
           genes[i] = x 

        return genes
