# SHL-Assessment-Recommendation-System

An AI-powered tool that recommends relevant SHL assessments based on query or a job description. It scrapes product data from SHL's official catalog and uses NLP techniques (TF-IDF + cosine similarity) for intelligent recommendations.

## Features

- Scrapes SHL assessment data including description, duration, and test type.
- REST API using **FastAPI** to handle recommendations.
- Frontend built with **Streamlit** for interactive querying.
- Supports similarity-based retrieval using **TF-IDF** and **cosine similarity**.

## Installation

### 1. Clone the repository

```bash
git clone https://itsmohitnamdeo/SHL-Assessment-Recommendation-System.git
cd SHL-Assessment-Recommendation-System
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Scrape Product Data

Use the scraper to fetch product data from SHL's catalog (approx. 500 items by default):

```bash
cd product_catalog
python product_catalog.py
```

> This will generate a file `product_catalog.csv`.


## Run the API

Start the FastAPI backend:

```bash
cd backend
uvicorn api:app --reload --port 8000
```

* Test: Visit [http://localhost:8000/health](http://localhost:8000/health)
* Swagger Docs: [http://localhost:8000/docs](http://localhost:8000/docs)


## Launch the Streamlit App

Start the frontend in a new terminal:

```bash
cd frontend
streamlit run app.py
```

* Visit [http://localhost:8501](http://localhost:8501) to use the recommender.

## Screenshots

- SHL-Assessment-Recommender
  
![shl_assessment_reommender](https://github.com/user-attachments/assets/5038bb0f-847a-462d-847b-17b7e34fc770)


## API Requests

- /health

![health](https://github.com/user-attachments/assets/9fec03c7-ce29-4167-8b50-530e2dfc1355)



- /recommend

![recommend](https://github.com/user-attachments/assets/d876e283-541f-4f79-b5da-9c13c4649a7e)

![recommend1](https://github.com/user-attachments/assets/4a1a0368-b9b5-4317-8a9d-efec0e44a9f6)


## Contact

If you have any questions, suggestions, or need assistance related to the CSV-File-Utility-Tool, feel free to reach out to Me.

- MailId - namdeomohit198@gmail.com
- Mob No. - 9131552292
- Portfolio : https://itsmohitnamdeo.github.io
- Linkedin : https://www.linkedin.com/in/mohit-namdeo
