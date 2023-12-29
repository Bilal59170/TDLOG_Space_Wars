import time
import matplotlib.pyplot as plt


class Profiler:
    def __init__(self) -> None:
        self.functions = {}
        
        
    def profile(self, function):

        self.functions[function.__name__] = []

        def wrapper(*args, **kwargs):
            start = time.time()
            result = function(*args, **kwargs)
            end = time.time()
            self.functions[function.__name__].append(end-start)
            return result
        
        return wrapper
    
    def open_plot(self):
        plt.figure()
        plt.title("Temps d'exécution des fonctions")
        plt.xlabel('Nombre d\'appels')
        plt.ylabel('Temps (s)')
    
    def update_plot(self):
        for name, times in self.functions.items():
            plt.plot(range(len(times)), times, label=name)
        plt.legend()
        plt.pause(0.001)