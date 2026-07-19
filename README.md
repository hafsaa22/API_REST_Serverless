# API_REST_Serverless

### My choice of AWS Services :  
AWS SDK - IAM - CloudWatch - CloudFormation (AWS SAM) - AWS Lambda - API Gateway - DynamoDB - Amazon S3 - Amazon CloudFront  


## Description
Ce projet contient le code source et les fichiers de configuration de l'infrastructure (IaC) pour l'API Serverless du catalogue de services de Smartovate. 
L'infrastructure est automatisée et déployée à l'aide du framework AWS SAM (Serverless Application Model).

## Architecture Technique
* **Infrastructure as Code** : AWS SAM (`template.yaml`).
* **API REST** : Amazon API Gateway.
* **Compute** : AWS Lambda (Runtime : `Python 3.12`).
* **Base de données** : Amazon DynamoDB.
  * Table : `CatalogTable`
  * Modèle de données : Clé de partition (PK) et Clé de tri (SK).
  * Mode de facturation : On-Demand (`PAY_PER_REQUEST`).

## Prérequis
Avant de commencer, assurez-vous d'avoir installé les outils suivants sur votre poste de travail :
* [AWS CLI] 
* [AWS SAM CLI]
* [Python 3.12]
* [Git]

## Structure du Projet
* `hello_world/` : Dossier contenant le code source de la fonction Lambda.
  * `app.py` : Logique applicative de la fonction.
* `template.yaml` : Fichier principal définissant l'infrastructure AWS (Ressources, Permissions IAM, Variables d'environnement).
* `samconfig.toml` : Fichier généré automatiquement sauvegardant les paramètres de déploiement.

## Instructions de déploiement local

### 1. Construction du projet (Build)
Pour compiler le projet et préparer les artefacts de déploiement, exécutez la commande suivante à la racine du projet :
```bash
sam build