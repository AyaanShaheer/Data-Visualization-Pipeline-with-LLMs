Data Visualization Pipeline With LLMs
This project, is a Streamlit-based web application that enables users to upload a dataset (CSV or Excel), ask questions about their data, and generate visualizations using an LLM. The app leverages LangChain and OpenAI's API to generate Python code for data analysis and visualization, which is then executed securely to display results. Due to OpenAI free-tier quota limits as of May 17, 2025, the app currently uses mocked responses, but it is designed to work seamlessly with an LLM once the quota resets.
Features

File Upload: Supports CSV and Excel files (up to 200MB).
Natural Language Queries: Ask questions about your data (e.g., "Show the average purchase amount by gender").
Automated Code Generation: Generates Python code for data analysis and visualization using pandas, Matplotlib, and Seaborn.
Secure Code Execution: Restricts unsafe operations (e.g., system-level imports like os or sys).
Interactive Visualizations: Displays results and visualizations directly in the Streamlit app.

Dataset
The project includes a sample dataset, customer_data.csv, with the following columns:

customer_id: Unique ID for each customer.
name: Customer name.
age: Customer age.
gender: Customer gender (Male/Female).
purchase_amount: Amount spent by the customer.
category: Purchase category (Clothing, Electronics, Books).

Example data:



customer_id
name
age
gender
purchase_amount
category



1
Alice
25
Female
50.5
Clothing


2
Bob
30
Male
75.0
Electronics


3
Charlie
22
Male
30.0
Books


Prerequisites

Python 3.8 or higher
Git (for cloning the repository)
A virtual environment (recommended)

Setup Instructions

Clone the Repository:
git clone https://github.com/AyaanShaheer/Data-Visualization-Pipeline-with-LLMs.git
cd resolute-ai-task-6


Set Up a Virtual Environment:
python -m venv venv
.\venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux


Install Dependencies:
pip install -r requirements.txt

The requirements.txt file includes all necessary packages, such as Streamlit, pandas, Matplotlib, Seaborn, and LangChain.

(Optional) Configure OpenAI API Key:

Create a .streamlit/secrets.toml file in the project directory:
OPENAI_API_KEY = "your-api-key-here"


Note: This step is not required currently, as the app uses mocked responses due to OpenAI quota limits.



Run the App:
streamlit run app.py


Open the app in your browser at http://localhost:8501.



Usage

Upload a Dataset:

Use the file uploader to upload a CSV or Excel file (e.g., customer_data.csv).
The app will display a preview of the data and basic information (e.g., column names, data types).


Ask a Question:

Enter a question in the text input, such as:
"Show the average purchase amount by gender"
"Create a bar plot of purchase amount by category"


The app will execute the corresponding mocked code and display the results.


View Results:

For "Show the average purchase amount by gender":
Output:
Female: 78.67
Male: 65.0


For "Create a bar plot of purchase amount by category":

A bar plot showing average purchase amounts per category (Clothing: 85.25, Electronics: 70.25, Books: 60.0).





Demo
Supported Questions (Mocked Responses)
Due to OpenAI quota limits, the following questions are currently mocked:

Show the average purchase amount by gender:
Output: Female: 78.67, Male: 65.0


Create a bar plot of purchase amount by category:
Output: A bar plot with categories (Clothing, Electronics, Books) on the x-axis and average purchase amounts on the y-axis.



Video Demonstration

A screen-recorded video demonstrating the user story is available in the submission.
The video shows:
Uploading customer_data.csv.
Asking the above questions and displaying the results.
Explaining the app’s functionality and limitations.



Limitations

Supports only CSV and Excel files (up to 200MB).
Visualizations are limited to Matplotlib and Seaborn.
Code execution is restricted to safe operations (no system-level access).
Currently using mocked responses due to OpenAI free-tier quota limits as of May 17, 2025.
Large datasets may slow down processing.

Notes

Quota Limitation: The app is designed to use OpenAI’s GPT-3.5-turbo for code generation. However, due to free-tier quota limits, it currently relies on mocked responses. Once the quota resets, the mock logic can be removed to enable LLM integration.
Future Improvements:
Add support for more file types (e.g., JSON).
Integrate alternative free LLMs (e.g., Hugging Face, Ollama).
Enhance visualizations with Plotly for interactivity.




This project is licensed under the MIT License - see the LICENSE file for details (if applicable).
