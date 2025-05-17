import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
import seaborn as sns
from langchain_experimental.agents.agent_toolkits import create_python_agent
from langchain.agents import AgentExecutor
from langchain_experimental.tools import PythonREPLTool
from langchain_openai import ChatOpenAI
import os
import uuid
import ast
import re
from contextlib import redirect_stdout

# Set up OpenAI API key (assumes environment variable is set)
os.environ["OPENAI_API_KEY"] = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY"))

# Initialize the LLM and agent (commented out since we're mocking the response)
# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
# agent_executor = create_python_agent(
#     llm=llm,
#     tool=PythonREPLTool(),
#     verbose=True
# )

# Function to safely parse and execute generated code
def safe_execute_code(code_string, df):  # Added df as a parameter
    try:
        # Clean the code
        code_string = re.sub(r'```python\n|```', '', code_string).strip()
        
        # Parse code to AST to check for dangerous operations
        tree = ast.parse(code_string)
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for n in node.names:
                    if n.name in ['os', 'sys', 'subprocess', 'shutil']:
                        return None, "Error: Code contains unsafe imports"
        
        # Execute code in a controlled environment
        output = io.StringIO()
        with redirect_stdout(output):
            # Include df in the namespace
            exec(code_string, {"pd": pd, "plt": plt, "sns": sns, "st": st, "df": df})
        return output.getvalue(), None
    except Exception as e:
        return None, f"Error executing code: {str(e)}"

# Streamlit app layout
st.title("Data Visualization Pipeline with LLM")
st.write("""
Upload a CSV or Excel file and ask questions about your data. 
The LLM will generate and execute code to analyze and visualize the data.
""")

# File uploader
uploaded_file = st.file_uploader("Upload CSV or Excel file", type=['csv', 'xlsx', 'xls'])

if uploaded_file:
    # Read the file
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.write("Data Preview:")
        st.dataframe(df.head())
        
        # Store DataFrame in session state
        st.session_state['df'] = df
        
        # Display basic info
        st.write("Dataset Info:")
        buffer = io.StringIO()
        df.info(buf=buffer)
        st.text(buffer.getvalue())
        
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        st.stop()

    # User question input
    user_question = st.text_input("Ask a question about your data:", 
                                 placeholder="e.g., Show a bar plot of sales by region")
    
    if user_question:
        try:
            # Prepare prompt for the agent (for reference, not used in mock)
            prompt = f"""
            You are a data analysis expert. The user has uploaded a dataset and asked: '{user_question}'.
            The dataset is available as a pandas DataFrame named 'df'.
            Generate Python code to analyze the data and create visualizations using pandas, matplotlib, and seaborn.
            Ensure the code:
            - Uses only pd, plt, sns, and st (for Streamlit display)
            - Produces clear, labeled visualizations
            - Handles potential errors (e.g., missing columns)
            - Is safe and doesn't use system-level operations
            Return only the Python code wrapped in ```python``` blocks.
            """
            
            # Mock the LLM response based on the user question
            if user_question.lower() == "show the average purchase amount by gender":
                result = {
                    "output": """
```python
avg_purchase = df.groupby('gender')['purchase_amount'].mean()
print("Female:", avg_purchase['Female'])
print("Male:", avg_purchase['Male'])
```
                """
                }
            elif user_question.lower() == "create a bar plot of purchase amount by category":
                result = {
                    "output": """
```python
plt.figure(figsize=(8, 6))
sns.barplot(x='category', y='purchase_amount', data=df)
plt.title('Purchase Amount by Category')
plt.xlabel('Category')
plt.ylabel('Purchase Amount')
st.pyplot(plt)
plt.clf()
```
                """
                }
            else:
                # For other questions, provide a placeholder response
                result = {
                    "output": """
```python
print("Mock response: This question is not mocked. Please wait for your OpenAI quota to reset or mock this question manually.")
```
                """
                }
            
            # Extract and execute the generated code, passing df
            output, error = safe_execute_code(result["output"], df)  # Pass df to the function
            
            if error:
                st.error(error)
            else:
                st.success("Analysis completed!")
                if output:
                    st.text("Output:")
                    st.text(output)
                
        except Exception as e:
            st.error(f"Error processing request: {str(e)}")

# Instructions and limitations
st.sidebar.header("How It Works")
st.sidebar.write("""
1. Upload a CSV or Excel file.
2. The app previews the data and shows basic info.
3. Ask a question about your data (e.g., "Plot a histogram of age" or "Show correlation between variables").
4. The LLM generates Python code to analyze and visualize the data.
5. The code is executed securely, and results are displayed.
""")
st.sidebar.header("Limitations")
st.sidebar.write("""
- Only supports CSV and Excel files.
- Visualizations use matplotlib and seaborn.
- Code execution is restricted to safe operations.
- Large datasets may slow down processing.
- Currently using a mock response due to OpenAI quota limits.
""")