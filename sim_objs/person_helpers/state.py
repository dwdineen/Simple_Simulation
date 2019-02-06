from .genes import Genes
from model import Model

class State(dict):

    NAME     = 0
    ALIVE    = 1
    DOB      = 2
    
    def __init__(self, state, genes, traits):
        super().__init__(self)

        from sim_objs import Person
        self[State.NAME] = state.get(State.NAME) or Person.pickName(genes[Genes.GENDER])
        self[State.ALIVE] = True
        self[State.DOB] = Model.get().time

