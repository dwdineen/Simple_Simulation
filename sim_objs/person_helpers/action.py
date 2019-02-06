from model import Model
import random
from .genes import Genes

class Action:

    def affinity(self, person):
        """ To be defined in concrete action classes. Returns a
        float [0, 1] which defines the affinity the given person
        has towards the action """

        raise NotImplementedError

    def apply(self, person):
        """ To be defined in the concrete action classes. Applies
        the action to the person. Can affect person's:

        - traits
        - state

        Returns: a list of actions to be immediately taken
        """

        raise NotImplementedError


class Breed(Action):

    def affinity(self, person):

        # For now I will just return one. This means that every person has a 100% affinity towards
        # breeding. In other words, there is a high likelihood that a person will try to breed.
        # everyday. This does not mean the breeding will be successful, this happens in
        # Breed.apply()

        return 1

    def apply(self, person):
        """
        One parent is the person. Gets random other parent.
        """

        # print (f"Trying to breed, {person.name}")

        parent1 = person
        parent2 = random.choice(Model.get().sim_objs)
        while parent1 == parent2:
            parent2 = random.choice(Model.get().sim_objs)

        if parent1.gender != parent2.gender:
            if parent1.age >= parent1.genes[Genes.REPRODUCTIVE_AGE] and parent2.age >= parent2.genes[Genes.REPRODUCTIVE_AGE]:
                if random.randint(0, 100) <= 2:
                    Model.get().sim_objs.append(Breed.breed(parent1, parent2))
                    print(f"{parent1.name} and {parent2.name} gave birth to a baby {Model.get().sim_objs[-1].gender} named {Model.get().sim_objs[-1].name}.")


    @staticmethod
    def breed(person1, person2):
        from collections import Iterable
        from sim_objs import Person

        #print(person1) Debugging
        #print(person2)
        new_genes = []
        testament = list(map(random.choice((lambda x: x, lambda x: x * -1)), [[] if isinstance(i, Iterable) else 1 if i % 2 == 0 else -1 for i in range(len(person1.genes.to_list()))]))
        for aj, bj in zip(person1.genes, person2.genes):
            #if isinstance(aj, Iterable):               Dafuq is this?
                #new_genes.append(breed(aj, bj))
                #continue                               Someone please explain this to me...
            translator = {-1: aj, 1: bj}
            chosen_succesor = random.choice(testament)
            testament.pop(testament.index(chosen_succesor))
            new_genes.append(translator[chosen_succesor])
        return Person(genes=Genes.convert_from_list(new_genes))


