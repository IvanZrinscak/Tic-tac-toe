import numpy as np


class Igra(object):
    class Igrac(object):

        def __init__(self, broj: int, ime=None, *args, **kwargs):
            if not isinstance(broj, int):
                raise TypeError("broj mora biti objekt klase `int'.")

            if not (ime is None or isinstance(ime, str)):
                raise TypeError("ime mora biti None ili objekt klase `str'.")

            self.broj = broj

            if ime is None:
                self.ime = '{0:s} {1:d}'.format(self.__class__.__name__, i)
            else:
                self.ime = ime

        def odigrajPotez(self, n, ponovi=False) -> tuple:
            if ponovi:
                print("ponovi: ")
            potez = []
            for i in range(n):
                potez.append(int(input("Koordinata: ")))
            return tuple(potez)

    def __new__(cls, *args, **kwargs):
        return super(Igra, cls).__new__(cls)


    def __init__(self, n=5, d=5):
        size = [n for i in range(d)]
        self.__tabla = np.ndarray(size, np.int8)
        self.__tabla.fill(-1)
        self.__pokrenuta = False
        self.__zavrsena = False
        self.__igraci = []
        self.__trenutni = 0
        self.__n = n
        self.__d = d
        self.__zadnji = tuple()


    def dohvatiTablu(self):
        return self.__tabla

    def dodajIgrace(self):
        self.__igraci.append(Igra.Igrac(0, "Ivan"))
        self.__igraci.append(Igra.Igrac(1, "Davor"))
        return


    def igraj(self):

        def binomial(n,k):
            if(k==1):
                return [[i] for i in range(n)]
            elif(n == 0):
                return []
            else:
                L = [ x+ [n-1] for x in binomial(n-1,k-1)]
            return binomial(n-1,k)+ L[::-1]
        
        def __pokreni():

            self.__pokrenuta = True

        def __zavrsi():

            self.__zavrsena = True

        def __pokaziTablu(tabla):
            for i in range(self.__n):
                linija = "|"
                for j in range(self.__n):
                    if tabla[i,j] == 0:
                        linija += "O|"
                    elif tabla[i,j] == 1:
                        linija += "X|"
                    else:
                        linija += " |"
                print(linija)

        def __pretvoriTablu(tabla):
            if tabla.ndim == 2:
                __pokaziTablu(tabla)
            else:
                a = [slice(None) for i in range(tabla.ndim)]
                for j in range(self.__n):
                    a[0] = j
                    __pretvoriTablu(tabla[tuple(a)])
                    print("\n")



        def __dohvatiPotez() -> tuple:

            ponovi = False
            while True:
                potez = self.__igraci[self.__trenutni].odigrajPotez(self.__d, ponovi)
                if self.__tabla[potez] == -1:
                    self.__tabla[potez] = self.__trenutni
                    print(self.__trenutni)
                    self.__trenutni = (self.__trenutni + 1) % 2
                    break
                else:
                    ponovi = True

            self.__zadnji = potez

            return potez

        def __gotovaIgra():
            if (self.__zadnji == tuple()):
                return False
            for dim in range(1,self.__d+1):
                for podskup in binomial(self.__d, dim):
                    k = podskup[0]
                    p = list(self.__zadnji) 
                    q = list(self.__zadnji) ##koordinate zadnjeg poteza
                    Dalje = False
                    podskup1 = []
                    podskup2 = []
                    for i in podskup:
                        if (self.__zadnji[k] == self.__zadnji[i]):
                            podskup1.append(i)
                        elif (self.__zadnji[k] == self.__n - 1 - self.__zadnji[i]):
                            podskup2.append(i)
                        else:
                            Dalje = True
                            break
                    if Dalje:
                        continue
                    
                    Nastavi1 = Nastavi2 = True
                    while Nastavi1:
                        if (self.__tabla[tuple(p)] != self.__tabla[self.__zadnji]):
                            Nastavi2 = False
                            break
                        for i in podskup1:
                            if p[i] == self.__n-1:
                                Nastavi1 = False
                            else:
                                p[i] += 1
                        for i in podskup2:
                            if p[i] == 0:
                                Nastavi1 = False
                            else:
                                p[i] -= 1
                    
                    Nastavi1 = True
                    while Nastavi1:
                        if (self.__tabla[tuple(q)] != self.__tabla[self.__zadnji]):
                            Nastavi2 = False
                        for i in podskup1:
                            if q[i] == 0:
                                Nastavi1 = False
                            else:
                                q[i] -= 1
                        for i in podskup2:
                            if q[i] == self.__n-1:
                                Nastavi1 = False
                            else:
                                q[i] += 1

                    if Nastavi2:
                        print("gotovo, pobjednik je:", self.__igraci[(self.__trenutni + 1) % 2].ime)
                        return True

            if self.__tabla.min() == 0:
                print("Gotovo je, nema pobjednika!")
                return True

            return False

        while not __gotovaIgra():
            __dohvatiPotez()
            __pretvoriTablu(self.__tabla)