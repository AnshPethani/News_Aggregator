# News Articles API

This project is a FastAPI-based application that provides an API for managing and retrieving news articles. It includes endpoints for fetching all articles, retrieving specific articles, and searching for articles by keywords. The project also provides a front-end interface to interact with the API.

## Features

- **Retrieve all articles** with optional filtering by category, start date, and end date.
- **Retrieve a specific article** by its ID.
- **Search articles** by keywords in the summary.
- **Static files** for serving additional resources like favicon.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/AnshPethani/News_Aggregator.git
    cd News_Aggregator
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. **Start the FastAPI server:**

    ```bash
    uvicorn main:app --reload
    ```

2. **Access the API:**

    Open your browser and navigate to `http://127.0.0.1:8000` to see the root endpoint message. Use Postman or a similar tool to interact with the API endpoints.

## API Endpoints

- **GET `/`**: Provides information about the API.
- **GET `/articles`**: Retrieve all articles. Optional query parameters:
  - `category`: Filter by category.
  - `start_date`: Filter articles published on or after this date (format: YYYY-MM-DD).
  - `end_date`: Filter articles published on or before this date (format: YYYY-MM-DD).
- **GET `/articles/{id}`**: Retrieve a specific article by its ID.
- **POST `/search`**: Search articles by keywords in the summary. The request body should be a JSON object with the `keywords` field.

## Example Requests

### Retrieve All Articles

**Request:**

    GET http://127.0.0.1:8000/articles

**Response:**

    200 OK
    Content-Type: application/json
    [
      {
        "title": "German far right hails 'historic' election victory in east",
        "summary": "Germany's anti-immigration party Alternative for Germany is on course for victory in Thuringia.",
        "publication_date": "2024-09-02 03:15:51",
        "category": "Politics",
        "url": "No URL available"
      }
    ]

### Retrieve Specific Article

**Request:**

    GET http://127.0.0.1:8000/articles/1

**Response:**

    200 OK
    Content-Type: application/json
    {
      "title": "German far right hails 'historic' election victory in east",
      "summary": "Germany's anti-immigration party Alternative for Germany is on course for victory in Thuringia.",
      "publication_date": "2024-09-02 03:15:51",
      "category": "Politics",
      "url": "No URL available"
    }

### Search Articles

**Request:**

    POST http://127.0.0.1:8000/search
    Content-Type: application/json

    {
      "keywords": "election victory"
    }

**Response:**

    200 OK
    Content-Type: application/json
    [
      {
        "title": "German far right hails 'historic' election victory in east",
        "summary": "Germany's anti-immigration party Alternative for Germany is on course for victory in Thuringia.",
        "publication_date": "2024-09-02 03:15:51",
        "category": "Politics",
        "url": "No URL available"
      }
    ]
