import time
import matplotlib.pyplot as plt


class Profiler:
    """
    Classe permettant de profiler le temps d'exécution des fonctions décorées
    exemple d'utilisation :

    profiler = Profiler()
    
    @profiler.profile
    def my_function():
        ...

    """

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
        # Créée la figure avec un camembert
        self.fig, self.ax = plt.subplots()
        self.ax.pie([1], labels=[""], autopct="%1.1f%%")
        self.ax.axis("equal")
        plt.show(block=False)

    def update_plot(self):
        # Met à jour le camembert
        self.ax.clear()
        prcts = [sum(self.functions[function]) for function in self.functions]
        labels = [f"{function} : {1000*sum(self.functions[function])/len(self.functions[function]):.4f} ms" for function in self.functions]
        self.ax.pie(prcts, labels=labels, autopct="%1.1f%%")
        self.ax.axis("equal")
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.pause(0.001)

        