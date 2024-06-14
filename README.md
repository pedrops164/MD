# LLM-based Tourist Guide for Northern Portugal - Practical Assignment for the Data Mining Course in UMinho

## Overview

This project leverages a Large Language Model (LLM) to create a comprehensive tourist guide for various locations in Northern Portugal. From the outset, the goal was to develop an application that utilizes advanced data mining techniques and a Retrieval-Augmented Generation (RAG) approach to provide not only accurate and detailed information about tourist attractions, culture, and history, but also personalized travel itineraries for visitors to Northern Portugal.

## Introduction

The project aims to enhance the quality of tourist information available for Northern Portugal by integrating an LLM refined with data from public sources. The main goal is to create a tourist guide that provides precise and user-tailored information about various locations in the region.

## Architecture

The architecture of the application involves:
- Data extraction and processing from public sources.
- Integration of an LLM (GPT-3.5) through the OpenAI API.
- Utilization of RAG for enhanced data retrieval.
- A user interface built with Tkinter for easy interaction.

## Data

Data was sourced from the VisitPortugal website, downloaded as PDFs, and processed using the `fitz` and `langchain` libraries. The processed data was divided into chunks and stored in separate databases for different entities like accommodations, activities, beaches, casinos, gardens, museums, thematic parks, and zoos.

## Functionality

The application performs three main actions after receiving a user prompt:
1. **Validation**: Checks if the user’s request is feasible.
2. **Entity Detection**: Identifies relevant entities from the user's query.
3. **Itinerary Generation**: Creates a detailed itinerary using the identified entities and the user's preferences.

## Examples

### Example Prompt
User: "I want to do a 3-day road trip starting in Porto and finishing in Braga, Portugal. On the first day, I want to visit beaches and tourist sites. On the second day, I want to go to a zoo in the afternoon, and a casino in the evening. On the third day, I want to spend my day in the hotel. Build me an itinerary."

### Example Output
- **Day 1**:
  - Start your road trip in Porto.
  - Visit Praia da Foz in Porto to enjoy the beach and the ocean view.
  - Address: Praia da Foz, Porto.
  - Explore the tourist sites in Porto.
  - Drive towards Braga.
  - Stay overnight at Casa da Ponte do Porto in Braga.
  - Address: Av. Ponte do Porto, 47, 4710-730 Braga.
- **Day 2**:
  - Visit Zoo Santo Inácio in Vila Nova de Gaia, Porto.
  - Address: Rua 5 de Outubro, 4503, 4430-809 Vila Nova de Gaia.
  - In the evening, head to Casino da Póvoa in Póvoa de Varzim.
  - Address: Edifício do Casino da Póvoa de Varzim, 4490-403 Póvoa de Varzim.
  - Stay overnight at Casa da Ponte do Porto in Braga.
- **Day 3**:
  - Spend the day relaxing at Casa da Ponte do Porto in Braga.

## Results and Discussion

The project's effectiveness was evaluated by comparing the performance of the LLM integrated with RAG against other solutions like standard ChatGPT and Mistral Small. Metrics for evaluation included accuracy and relevance of responses.

## Project Structure

```plaintext
├── dbs
│   ├── accomodations_emb
│   ├── activities_emb
│   ├── beaches_emb
│   ├── casinos_emb
│   ├── gardens_emb
│   ├── museums_emb
│   ├── thematicparks_emb
│   ├── zoos_emb
│   ├── __init__.py
│   └── db.py
├── images
│   └── demo_projeto_1.gif
├── logs
│   └── README.md
├── pdfs
│   ├── accomodation
│   ├── activities.pdf
│   ├── beaches.pdf
│   ├── casinos.pdf
│   ├── gardens.pdf
│   ├── museums.pdf
│   ├── thematicparks.pdf
│   └── zoos.pdf
├── presentations
│   ├── .env
│   ├── apresentacao_1.pptx
│   └── apresentacao_2.pdf
├── .gitignore
├── agent.py
├── artigofinal_grupo2.pdf
├── gui.py
├── main.py
├── queries.txt
├── README.md
├── requirements.txt
├── scraper.py
└── templates.py
```

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/tourist-guide-north-portugal.git
    cd tourist-guide-north-portugal
    ```

2. **(Optional) Create and activate a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the main application**:
    ```bash
    python main.py
    ```

2. **Interacting with the GUI**:
   - Enter your travel preferences and locations.
   - Receive personalized itineraries.

![Demo](./images/demo_projeto_1.gif)

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## Authors

- **Pedro Pereira Sousa PG54721**
- **Mateus Pereira PG54089**
- **Nuno Miguel Leite da Costa PG54121**
- **Elione Culeca Cossengue PG51634**
