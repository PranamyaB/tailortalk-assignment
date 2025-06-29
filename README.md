# TailorTalk Calendar Assistant

A Streamlit-based AI calendar assistant that uses LangGraph + Google Calendar API to schedule meetings using natural language.

## Features

- Natural language to Google Calendar integration
- LangGraph agent with OpenAI
- Event creation & time parsing
- Sample queries like:
  - "Book a meeting tomorrow at 3 PM"
  - "Do I have any free time next Friday?"

## Tech Stack

- Python, Streamlit
- LangGraph, LangChain, OpenAI
- Google Calendar API (OAuth2)

## Run Locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
