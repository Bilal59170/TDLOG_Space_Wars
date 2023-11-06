


"""

Objectif de ce fichier :
 - Créer une classe qui permet d'utiliser des variables synchronisées entre le serveur et le client, sans même avoir besoin de la distinguer d'une variable réelle
    => Exemple :
        => Server :
            
            socket_handler = socketDataChangesHandler(socket)       # Crée un objet qui gère les changements de variables
            socket_handler.await()                                  # Synchronise l'exécution du code avec le client

            ma_variable = DataStructure(socket_handler)             # Crée une variable synchronisée
            ma_variable = 5                                         # Change la valeur de la variable
            socket.pushNewDataStructures()                          # Envoie les variables synchronisées au client

            time.sleep(5)                                           # Attend 5 secondes

            print(ma_variable)                                      # Affiche 10

        => Client :
            socket_handler.await()                                  # Synchronise l'exécution du code avec le serveur

            ma_variable, =  socket_handler.pullNewDataStructures()  # Récupère les nouvelles variables synchronisées du serveur
            print(ma_variable) # Affiche 5                          # Affiche 5

            ma_variable = 10                                        # Change la valeur de la variable
            
    


"""

class dataChangesHandler:
    """
    Interface pour les classes qui gèrent les changements des objets
    Définit juste le squelette des deux sous-classes
    """

    def __init__(self, object):
        pass
    def add(self, object):
        pass

class gameDataChangesHandler:
    pass

class socketDataChangesHandler:
    pass

class sharedDataStructure:
    def __init__(self, socketInstance):
        self._socket = socketInstance

    @property
    def shared_data(self):
        return self._shared_data

    @shared_data.setter
    def shared_data(self, value):
        if self._shared_data != value:
            # Send the new value to the server inside the setter
            self.send_data_to_server(value)
            self._shared_data = value
    
    def __set__(self, instance, value):
    
    def send_data_to_server(self, data):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('127.0.0.1', 12345))
        serialized_data = pickle.dumps(data)
        client_socket.send(serialized_data)
        client_socket.close()

