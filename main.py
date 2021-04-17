import itertools
import statistics
from pprint import pprint
from random import randint


class Escenario:
    def __init__(self, mesa1, mesa2):
        self.mesa1 = mesa1.copy()
        self.mesa2 = mesa2.copy()
        self.history = {k: [] for k in self.mesa1 + self.mesa2}
        self.permutaciones = list()
        self.secuencia = list()
        self.save_history()

    def evaluar_todas_combinaciones(self):
        for k, v in self.history.items():
            if len(set(v)) < len(self.mesa1) + len(self.mesa2) - 1:
                return False
        return True

    def save_history(self):

        for persona in self.mesa1:
            mesa = self.mesa1.copy()
            mesa.remove(persona)
            self.history[persona] += mesa

        for persona in self.mesa2:
            mesa = self.mesa2.copy()
            mesa.remove(persona)
            self.history[persona] += mesa

        self.save_secuencia()

    def save_secuencia(self):
        self.secuencia.append((self.mesa1.copy(), self.mesa2.copy()))

    def permutar(self):
        position1 = randint(0, len(self.mesa1) - 1)
        position2 = randint(0, len(self.mesa2) - 1)
        self.permutaciones.append(f"{self.mesa1[position1]}x{self.mesa2[position2]}")
        self.mesa1[position1], self.mesa2[position2] = (
            self.mesa2[position2],
            self.mesa1[position1],
        )
        self.save_history()

    def recount(self):
        matches = dict()
        for k, v in self.history.items():
            others = list(self.history.keys())
            others.remove(k)
            matches[k] = [v.count(persona) for persona in others]
        return matches

    def varianza(self):
        """varianza general de cruces"""
        repetitions = list(itertools.chain.from_iterable(self.recount().values()))
        return statistics.variance(repetitions)

    def max_repeated(self):
        repetitions = list(itertools.chain.from_iterable(self.recount().values()))
        return max(repetitions)

    def show(self):
        print(f"Cambios: {len(self.permutaciones)} - {self.permutaciones}")
        print(f"Varianza: {self.varianza()}")
        print(f"Maximo repite {self.max_repeated()} veces")
        print("")
        print("Recount repeticiones (Cruces)")
        pprint(self.recount())
        print("")
        print("Pretty Escenas")
        for i, paso in enumerate(self.secuencia):
            print(
                f"--------------------------------- {self.permutaciones[i-1]}"
            ) if i >= 1 else ...
            print(f"Mesa1: {paso[0]}")
            print(f"Mesa2: {paso[1]}")
        print("")


def simular(n_sims, mesa1=["A", "B", "C"], mesa2=["1", "2", "3"]):

    sims = list()
    for n in range(n_sims):
        print(f"Running sim {n+1}/{n_sims}...")
        escenario = Escenario(mesa1, mesa2)
        while not escenario.evaluar_todas_combinaciones():
            escenario.permutar()
        sims.append(escenario)

    return sims


if __name__ == "__main__":

    # sims = simular(n_sims=10000)
    sims = simular(n_sims=10000, mesa1=["A", "B", "C", "D", "E"], mesa2=["1", "2", "3", "4", "5"])

    print("Sorting simulations...")
    # Ordenar por...

    # by numero de permutaciones only
    # sorted_sims = sorted(sims, key=lambda x: (len(x.permutaciones)))

    # by permutaciones & maximo gente repetida
    # sorted_sims = sorted(sims, key=lambda x: (len(x.permutaciones), x.max_repeated()))

    # by maximo gente repetida only
    # sorted_sims = sorted(sims, key=lambda x: x.max_repeated())

    # by permutaciones & varianza
    # sorted_sims = sorted(sims, key=lambda x: (len(x.permutaciones), x.varianza()))

    # by varianza only (ignora numero perms)
    # sorted_sims = sorted(sims, key=lambda x: x.varianza())

    # by perms > maximo reps > varianza general
    sorted_sims = sorted(sims, key=lambda x: (len(x.permutaciones), x.max_repeated(), x.varianza()))


    print("Printing 3 best results")
    for i, escenario in enumerate(sorted_sims[:3]):
        print("")
        print("xxxxxxxxxxxxxxxxxxxxxxxxx")
        print(f"  ESCENARIO {i+1}")
        print("xxxxxxxxxxxxxxxxxxxxxxxxx")
        print("")
        escenario.show()
