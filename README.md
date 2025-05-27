# Library Project

Ce projet est une application de gestion de bibliothèque développée avec Django. Elle permet de gérer les livres, les auteurs, les membres, les emprunts et les réservations, avec une interface utilisateur moderne et responsive grâce à Bootstrap 5.


## Installation
1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Install requirements: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`

## Testing
- Run tests: `pytest`
- Generate coverage: `pytest --cov=library --cov-report=html`

## Library API Endpoints
- GET /api/books/ - List all books
- POST /api/books/ - Create new book

### Books
- `GET /api/books/` - List all books
- `POST /api/books/` - Create new book
- Sample Request:
```json
{
    "title": "New Book",
    "author": 1,
    "isbn": "1234567890123"
}



   ```


## Utilisation

- **Gestion des livres** : Ajouter, modifier, supprimer et rechercher des livres.
- **Gestion des auteurs** : Ajouter, modifier, supprimer des auteurs.
- **Gestion des membres** : Inscription, connexion, emprunt et réservation de livres.
- **Emprunt et réservation** : Les membres peuvent emprunter ou réserver des livres disponibles.
- **Interface d’administration** : Gérer tous les objets du projet via l’admin Django.

---
