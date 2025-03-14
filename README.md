# discord-bot
## Description

Un bot discord en python qui permet d'assigner un rôle quand une personne arrive dans le serveur. Il peut aussi transformer les liens x et twitter qui renvoient sur l'application en vxtwitter qui permettent de lire le média sans quitter discord. Il contient aussi plusieurs commandes pour des gestions d'anniversaire.

## Installation 
1. **Cloner le dépôt**
  ```bash
git clone https://github.com/Elgrnd/discord-bot
cd <NOM_DU_DEPOT>
```

2. **Installer les dépendances**
  ```bash
pip install -r requirements.txt
```

3. **Recupérez le token du bot**
   
Pour fonctionner, vous devez récupérer le token de votre bot sur le portail développeur de discord et créer un fichier .env et écrire :

   ```env
clientId="votre_token"
```

4. **Modifiez comme voulez les id pour les permissions**

## Lancement du bot
1. **En local sur votre machine**

Exécutez le fichier start.bat, cela lancera un terminal et mettra votre bot en ligne

2. **Hébergement gratuit sur railway.com**

Vous pouvez héberger votre bot en connectant le repository github de votre bot à railway. Il vous faudra créer une variable d'environnement dans le projet railway en l'appelant clientId et en mettant votre token. Il vous faudra aussi créer un volume avec un path mnt/data. Votre bot sera maintenant fonctionnel.

## Contributeur

Moi 
