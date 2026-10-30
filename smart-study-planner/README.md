# Smart Study Planner

A student productivity web app built using Python and Streamlit.

## Features

- Add subjects and study topics
- Set exam dates and estimated study hours
- Prioritize pending topics by exam urgency
- Generate a daily study plan
- Track completed and pending topics
- Visualize progress by subject
- Export study tasks to CSV

## Technologies

- Python
- Streamlit
- Pandas
- Datetime

## Run locally

1. Install Python.
2. Clone or download this repository.
3. Install dependencies:

   pip install -r requirements.txt

4. Start the application:

   streamlit run app.py

5. Open the local URL shown in the terminal.

## Limitations

Topics are stored in Streamlit session state and are not
persisted to a database. The schedule is a basic priority-based
allocation, not an optimized timetable.

## Project purpose

This project demonstrates a simple study planning workflow,
task prioritization, progress tracking, and data export.
