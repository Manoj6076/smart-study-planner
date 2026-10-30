# Smart Study Planner

A student productivity web application built using Python and Streamlit. It helps students organize study topics, prioritize upcoming exams, generate daily study plans, and track their learning progress.

## Live Application

**Try the application here:**  
[Smart Study Planner – Live Demo](https://smart-study-planner-ks2xlklt2gahjakfqduavw.streamlit.app/)

## Features

- Add subjects and individual study topics.
- Set exam dates and estimated study hours.
- Prioritize pending topics based on exam urgency.
- Generate a daily study plan based on available study hours.
- Track completed and pending topics.
- Visualize progress by subject using charts.
- Export study tasks to CSV format.

## Technologies Used

- Python
- Streamlit
- Pandas
- Datetime

## 6-Hour Build Sprint – Development Work Log

The following table summarizes the planned breakdown of the six-hour development sprint.

| Time | Development Activity | Work Completed |
|---|---|---|
| Hour 1 | Project Planning and Setup | Identified the problem, planned the application features, and configured the Python and Streamlit environment. |
| Hour 2 | Topic Management | Developed the interface for adding subjects, study topics, exam dates, and estimated study hours. |
| Hour 3 | Priority Management | Implemented priority classification based on the number of days remaining until an exam. |
| Hour 4 | Daily Study Planner | Developed the logic to allocate available daily study time to pending topics. |
| Hour 5 | Progress Tracking and Visualization | Implemented completed/pending status updates, dashboard metrics, and progress charts. |
| Hour 6 | CSV Export, Testing and Deployment | Added CSV export, tested the main application workflow, prepared project documentation, and deployed the application using Streamlit Community Cloud. |

## How to Run Locally

1. Install Python.
2. Clone or download this repository.
3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the application:

   ```bash
   streamlit run app.py
   ```

5. Open the local URL displayed in the terminal.

## Limitations

- Study topics are stored in Streamlit session state and are not permanently saved to a database.
- The daily schedule uses basic priority-based allocation rather than an advanced timetable optimization algorithm.
- The current version does not use a trained machine learning model.

## Project Purpose

This project demonstrates a practical student productivity solution involving interactive web application development, task prioritization, time allocation, progress tracking, data visualization, and CSV export.

It was developed as a small-scale project for a six-hour Build Sprint, with a focus on delivering a functional application within a limited development timeframe.
