# TDLOG_pied.io

**Caractéristique du jeu**

***Synopsis:***

Il s'agirait d'un jeu dans lequel le joueur contrôle un vaisseau spatial et doit survivre le plus longtemps possible à des vagues d'ennemis d'intensité croissante en collectant des ressources et en éliminant des ennemis afin d'accéder à de nouvelles fonctionnalités et renforcer son vaisseau.

Dans un premier temps, on se concentrera sur l'implémentation de ce jeu en temps réel, qui requiert une interface graphique. Une fois les mécaniques de base efficacement implémentées, on s'attachera à développer un arbre de fonctionnalités (armes, attaques spéciales, protections, détecteurs de ressources) originales et intéressantes conférant à chaque partie un aspect unique, mais aussi stratégique sur le long-terme. 

Le code du jeu de base devrait permettre de jouer à un jeu équilibré et fluide malgré un grand nombre d’entités (vaisseaux, missiles, astéroïdes) contrôlées de façon plus ou moins complexe. Son architecture devrait également permettre une implémentation facile de nouveau contenu (nouvelles fonctionnalités, nouveaux types d’ennemis, nouvelles ressources) dans l’esprit d’une application en développement continu.

En fonction de l’avancement du projet, on pourra être amenés à explorer quelques pistes d’approfondissement :
- implémenter une mode de jeu en multijoueur, si possible en ligne
- rendre le jeu accessible depuis un site internet, notamment pour permettre aux joueurs d’enregistrer leur partie sur un leaderboard
- implémenter une IA contrôlant dynamiquement la faction adverse (type / mouvement des entités ennemies) en fonction de ses ressources et des choix du joueur pour mieux contrer son vaisseau et anticiper ses déplacements



**Utilisation de la documentation doxygen**

Dans ce projet, afin de mieux communiquer et d'avoir une vue globale sur les objets que l'on manipule, nous avons intégré une documentation Doxygen.



**Lancement du jeu**

Il suffit d'executer le fichier main du projet après avoir téléchargé les librairies appropriées. Ces dernières sont numpy, pyglet 1.5, matplotlib et shapely.
