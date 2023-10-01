# Book Giveaway Service API

## Table of Contents
1. [Overview](#overview)
2. [Core Features](#core-features)
3. [Tech Stack](#tech-stack)
4. [Deliverables](#deliverables)
5. [Bonus Features](#bonus-features)
6. [Setup and Installation](#setup-and-installation)
    - [Setting Up a Virtual Environment](#setting-up-a-virtual-environment)
    - [Clone the Repository](#clone-the-repository)
    - [Navigate to Project Directory](#navigate-to-project-directory)
    - [Activate the Virtual Environment](#activate-the-virtual-environment)
    - [Install Dependencies](#install-dependencies)
    - [Run Migrations](#run-migrations)
    - [Create SuperUser](#create-superuser)
    - [Run the Server](#run-the-server)
7. [Docker Setup](#docker-setup)
    - [Prerequisites](#prerequisites)
    - [Build Docker Image](#build-docker-image)
    - [Run Docker Container](#run-docker-container)
    - [Check API](#check-api)
    - [Stop Docker Container](#stop-docker-container)
    - [Docker Compose (Optional)](#docker-compose-optional)
    - [Troubleshooting](#troubleshooting)
8. [API Endpoints](#api-endpoints)
9. [Swagger Documentation](#swagger-documentation)
10. [Business Logic](#business-logic)
11. [Contributing](#contributing)

## Overview
Welcome to the Book Giveaway Service API, a Django RESTful API project for a book giveaway platform. This API allows users to manage books they want to give away, filter books based on various parameters, and manage supporting resources like authors, genres, conditions and images. It also includes user registration/authentication and a feature for book owners to select a recipient if multiple people are interested in a book.

# Core Features
1. ## User Authentication
   ### Registration with email:
   - Users can register with using their email address. Application checks a valid email. If there is a user registered with this email, re-registration is not allowed. After registration app provides unique Token. The registration endpoint is /register/
   ### User login:
   -  Users can login using their username and password. After login, app return message that authorization was succesfull and it gives the user a unique Token. The login endpoint is /login/.
   ### User logout:
   - Users can logout with using their username and password. The logout endpoint is /logout/.

2. ## Books Management
   ### CRUD operations for books:
   - Users can create, read, update, and delete their books. The CRUD operations are handled by the BookList class. For seeing all books users can use /books/ endpoint. For CRUD operations the endpoint is /books/{id}
   ### Book Filtering:
   - It is possible to filter books based on various parameters like author, genre, etc.

3. ## Supporting Resources:
   ### Manage authors, genres, conditions, images or posters:
   - The API allows users to manage authors, genres, conditions and images. These are managed by the AuthorList, GenreList, ConditionList, UploadImageView classes respectively.

4. ## Book Information
   ### Every Book include information about title, author, genres, condition, image, status, owner, when was the offer created, when was the information updated, location from where the book can be picked up, previous owner.

5. ## Ownership Decision
   ### Users Interests:
   - It is possible for users to express their interests on different books. For expressing the interest endpoint is /express-interest/. Process is managed by ExpressInterestView. If the user has already expressed interest in a specific book, the application will not allow it.
   ### Book Interests:
   - It is possible to see all the books in which users have expressed interest. It is also possible to see the interest expressed by users on each individual book, although only the owner of that book has the right to do so. Process is managed by BookInterestsView and AllBooksInterestsView. Endpoints are /book-interests/<int:pk>/ and /all-book-interests/.
   ### Owner Decision:
   - If multiple people are interested in a book, the owner can choose the recipient. The application checks the book on which the user makes a decision whether it belongs to him/her or not and whether the selected user expresses interest in this book. Process is managed by ChooseInterestedUserView. For owner decision endpoint is /choose-interested-user/.

# Tech Stack
- Django (Django Rest Framework for building the API)
- SQLite (Database used for development)
- Docker (Platform for containerization)

# Libraries Used

## Django REST Framework:
- The Django REST framework is used to build the API.

## Django-filter:

- The application uses Django-filter for various filtering, including books with different parameters

### How to filter:
- There are two ways to filter books:
  - When entering in the /books/ endpoint, using the "Filter" button 
  - Specifying the appropriate query parameters in the URL, for example:

```bash
GET /books/?author=author
```
```bash
GET /books/?author=author&genre=genre
```

### Pagination:
- Pagination is implemented in settings.py using Django REST Framework DEFAULT_PAGINATION_CLASS.

### drf_spectacular:
- drf_spectacular was used for generating the swagger documentation. For swagger documentation endpoints are /schema/; /swagger/; /redoc/;


# Deliverables
- Source code in a public GitHub repository.
- API documentation using Swagger.
- Docker and Docker Compose files for containerization.
- A comprehensive README containing all the necessary information on how to set up and run the project.

# Bonus Features
- Swagger (API documentation)
- Containerization (Docker)
- Unit tests (Only for demonstration)


# Setup and Installation

## Setting Up a Virtual Environment
Before you begin, it's advisable to set up a Python virtual environment to isolate your project and avoid conflicts with other packages. Here's how to create one:

**For macOS and Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**For Windows:**
```bash
python3 -m venv venv
venv\Scripts\activate
```

**Clone the Repository:**
```bash
git clone https://github.com/giorgi1121/books_giveaway_service_api.git
```

**Navigate to Project Directory:**
```bash
cd books_giveaway
```

### Activate the Virtual Environment
**For macOS and Linux:**
```bash
source venv/bin/activate
```

**For Windows:**
```bash
venv\Scripts\activate
```

**Install Dependencies:**
```bash
pip install -r requirements.txt
```

**Run Migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

**Create SuperUser:**
```bash
python manage.py createsuperuser
```

**Run the Server:**
```bash
python manage.py runserver
```

## Docker Setup

### Prerequisites
- Docker installed on your machine. [Get Docker](https://docs.docker.com/get-docker/)
- Docker Compose installed if you're using Windows or macOS. [Get Docker Compose](https://docs.docker.com/compose/install/)

## Build Docker Image
**Navigate to the project directory where the Dockerfile is located and run the following command to build the Docker image:**

```bash
docker build -t book_giveaway_api .
```

### This will build the Docker image with the name book_giveaway_api.

## Run Docker Container
**To run the Docker container, execute the following command:**
```bash
docker run -p 8000:8000 book_giveaway_api
```

### This will map port 8000 inside the container to port 8000 on your host machine.

## Check API
#### Open your browser and navigate to [http://localhost:8000](http://localhost:8000) to confirm that the API is running.

## Stop Docker Container
#### To stop the running container, you can use the docker stop command with the container ID or name.
```bash
docker stop [CONTAINER_ID_OR_NAME]
```


# Docker Compose (Optional)
### If you're using Docker Compose, you can define services in a docker-compose.yml file. To bring up the services, use:
```bash
docker-compose up
```
### To stop them:
```bash
docker-compose down
```

# Troubleshooting
### If you encounter any issues while setting up or running the Docker container, consult the Docker documentation for troubleshooting tips.


# API Endpoints
- /register/: User Registration
- /login/: User Login
- /logout/: User Logout
- /book/: Creating Book and Seeing Books List
- books/{id}/ CRUD operations for specific book
- /authors/: CRUD operations for authors
- /genres/: CRUD operations for genres
- /conditions/: CRUD operations for conditions
- /images/: CRUD operations for photos
- /express-interest/: For expressing interest in the book
- /book-interests/{id}/: Expressed interest in a particular book
- /all-book-interests/: Expressed interest for all books
- /choose-interested-user/: The book owner's choice of which interested user to give the book to
- /me/: Information about Authorized user


# Swagger Documentation
### Access the Swagger documentation at http://localhost:8000/swagger/


# Business Logic
### The core logic of the application revolves around the management of books and users. The API provides a set of functionalities for users to add, edit, delete, or give away books. The book listing and retrieval are optimized through the use of pagination, ensuring a smooth user experience even with a large dataset.



# Contributing
### Feel free to fork the project, open a PR, or submit an issue.