# TP_SOA_REST
L'idée c'est de mettre en place un Service Web Composite qui permet l'évaluation de Demande de Prêt Immobilier. Il est conçu pour automatiser le processus d'évaluation
des demandes de prêt immobilier en utilisant des services Web spécialisés. Il permet aux clients de soumettre des demandes de prêt 
immobilier exprimées en langage naturel. Le service intègre des composants d’extraction des informations métiers de texte de la demande, 
de vérification de solvabilité, d'évaluation de la propriété et de décision d'approbation pour fournir une évaluation complète 
et précise des demandes de prêt.
L'ensemble des services seront mis en place en utilisant le protocole REST.

# Technologies
- FastApi
- REST
- Docker

# Architecture
Chaque service est dockersier et nous avons orchestrer tous les services avec docker-compose:
```bash
.
├── README.md
├── docker-compose.yml
├── evaluation-propriete-service
│   ├── Dockerfile
│   ├── app
│   │   ├── __pycache__
│   │   │   └── main.cpython-311.pyc
│   │   ├── api
│   │   │   ├── __pycache__
│   │   │   │   ├── evaluation.cpython-311.pyc
│   │   │   │   └── models.cpython-311.pyc
│   │   │   ├── db.py
│   │   │   ├── db_manager.py
│   │   │   ├── evaluation.py
│   │   │   └── models.py
│   │   └── main.py
│   └── requirements.txt
├── extraction-informations-service
│   ├── Dockerfile
│   ├── app
│   │   ├── api
│   │   │   ├── db.py
│   │   │   ├── db_manager.py
│   │   │   ├── extraction.py
│   │   │   └── models.py
│   │   └── main.py
│   └── requirements.txt
├── service-composite
│   ├── Dockerfile
│   ├── app
│   │   ├── __pycache__
│   │   │   └── main.cpython-311.pyc
│   │   ├── api
│   │   │   ├── composite.py
│   │   │   ├── db.py
│   │   │   ├── db_manager.py
│   │   │   ├── listener.py
│   │   │   └── models.py
│   │   ├── main.py
│   │   └── templates
│   │       ├── index.html
│   │       └── loan.html
│   └── requirements.txt
└── solvabilite-service
    ├── Dockerfile
    ├── app
    │   ├── __pycache__
    │   │   └── main.cpython-311.pyc
    │   ├── api
    │   │   ├── __pycache__
    │   │   │   ├── db.cpython-311.pyc
    │   │   │   ├── db_manager.cpython-311.pyc
    │   │   │   ├── models.cpython-311.pyc
    │   │   │   └── solvabilite.cpython-311.pyc
    │   │   ├── db.py
    │   │   ├── db_manager.py
    │   │   ├── models.py
    │   │   └── solvabilite.py
    │   └── main.py
    └── requirements.txt
```



<!-- # Demo -->
<!-- ![Page_Web](/screenshots/demo-tp-soa.gif?raw=true)
-->
## Variables d'environnement

Pour lancer le projet, vous devez:

Créer un fichier .env et ajouter la clé openai qui permet d'utiliser l'Api openai:

`OPENAI_API_KEY=mykey`

```bash
    cd TP-SOA-REST/extraction-informations-service/app
    touch .env
```

## Lancer le projet

Clone the project

```bash
    git clone [https://github.com/aiMBF/TP_SOA_REST.git](https://github.com/aiMBF/TP_SOA_REST.gitgit)
```


Lancer l'application Docker 

Se positionner à la racine du projet

```bash
    cd TP-SOA-REST
    docker-compose up --build
```

![Services](/screenshots/containers.png?raw=true)



Se rendre à l'URL: http://localhost:8003/home/

![Home Page](/screenshots/home.png?raw=true)

![Acceptation Page](/screenshots/acceptation.png?raw=true)

![Refus Page](/screenshots/refus.png?raw=true)



