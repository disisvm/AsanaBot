# AsanaBot

This repository contains the code and resources for developing and analyzing an AI-powered chatbot designed to answer questions about Asana, a popular project management tool. The bot uses natural language processing (NLP) techniques to understand user queries and provide accurate responses.

## Table of Contents

- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-eda)
- [Contributing](#contributing)
- [License](#license)

## Project Structure

Here is an overview of the directory structure:

```bash
├── .idea/                     # IDE configuration files
├── .ipynb_checkpoints/        # Jupyter Notebook checkpoints
├── __pycache__/               # Python cache files
├── static/                    # Static files (CSS, JS, etc.)
├── templates/                 # HTML templates for the Flask app
├── annotated_asana_articles.xlsx  # Annotated articles related to Asana
├── app.py                     # Flask application to run the chatbot
├── asana_qa_dataset.xlsx      # QA dataset for the chatbot
├── asanabot-eda.ipynb         # Jupyter Notebook for EDA on QA dataset
├── bot_functions.py           # Python functions for chatbot operations
├── Final demo recording.mp4   # Demo video of the chatbot
├── qa_pairs.py                # Script to manage QA pairs for the bot
├── question_embeddings_cache.pkl  # Precomputed embeddings cache for the questions
```

## Installation

To set up the project locally, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/disisvm/AsanaBot.git
cd asanabot
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

Make sure to set up any necessary environment variables for your Flask app (like `FLASK_APP`, `FLASK_ENV`, etc.).

## Usage

1. **Run the Flask Application:**

```bash
python app.py
```

2. **Access the chatbot:**

Open your web browser and navigate to `http://127.0.0.1:5000/` to interact with the AsanaBot.

3. **Reset the Chat History:**

Use the "Reset" button in the chat interface to clear the chat history and start a new session.

## Features

- **Interactive Chat Interface:** Ask questions about Asana, and the bot will respond with relevant information.
- **Context Management:** The bot can handle multi-turn conversations and context switches.
- **Reset Functionality:** Easily reset the chat history to start fresh.
- **Exploratory Data Analysis (EDA):** Insights into the QA dataset using various visualizations and statistical methods.

## Exploratory Data Analysis (EDA)

The `asanabot-eda.ipynb` notebook contains the exploratory data analysis of the QA pairs. The EDA includes:

- Distribution of question and answer lengths.
- Common words and phrases.
- Word cloud visualizations.
- Heatmaps and correlation analyses.

## Contributing

Contributions are welcome! If you have any suggestions, feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.