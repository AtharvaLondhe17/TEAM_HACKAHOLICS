import streamlit as st
import pandas as pd
import ast
import os

# Load CSV data
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Preview of the uploaded data:")
    st.write(df.head())

# Generate visualization code
def generate_visualization_code(df, plot_type, column_x, column_y=None, output_image="visualization.png"):
    """
    Generate Python code to plot various charts using Matplotlib.
    The code is saved to a file and executed to create the visualization.
    """
    if plot_type == "Bar Chart":
        code = f"""
import matplotlib.pyplot as plt

# Data
data = {df[[column_x, column_y]].to_dict(orient='list')}

# Create bar chart
plt.figure(figsize=(8, 6))
plt.bar(data['{column_x}'], data['{column_y}'], color='skyblue')
plt.title("Bar Chart of {column_x} vs {column_y}", fontsize=14)
plt.xlabel("{column_x}", fontsize=12)
plt.ylabel("{column_y}", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()

# Save the visualization
plt.savefig("{output_image}")
plt.close()
        """
    elif plot_type == "Line Plot":
        code = f"""
import matplotlib.pyplot as plt

# Data
data = {df[[column_x, column_y]].to_dict(orient='list')}

# Create line plot
plt.figure(figsize=(8, 6))
plt.plot(data['{column_x}'], data['{column_y}'], marker='o', color='skyblue')
plt.title("Line Plot of {column_x} vs {column_y}", fontsize=14)
plt.xlabel("{column_x}", fontsize=12)
plt.ylabel("{column_y}", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()

# Save the visualization
plt.savefig("{output_image}")
plt.close()
        """
    elif plot_type == "Scatter Plot":
        code = f"""
import matplotlib.pyplot as plt

# Data
data = {df[[column_x, column_y]].to_dict(orient='list')}

# Create scatter plot
plt.figure(figsize=(8, 6))
plt.scatter(data['{column_x}'], data['{column_y}'], color='skyblue')
plt.title("Scatter Plot of {column_x} vs {column_y}", fontsize=14)
plt.xlabel("{column_x}", fontsize=12)
plt.ylabel("{column_y}", fontsize=12)
plt.tight_layout()

# Save the visualization
plt.savefig("{output_image}")
plt.close()
        """
    elif plot_type == "Pie Chart":
        code = f"""
import matplotlib.pyplot as plt

# Data
data = {df[column_x].value_counts().to_dict()}

# Create pie chart
plt.figure(figsize=(8, 6))
plt.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
plt.title("Pie Chart of {column_x}", fontsize=14)
plt.tight_layout()

# Save the visualization
plt.savefig("{output_image}")
plt.close()
        """
    else:
        raise ValueError("Unsupported plot type.")

    # Save code to a text file
    with open("generated_code.py", "w") as file:
        file.write(code)
    return code

# Execute the code and generate visualization
def execute_code_and_visualize():
    os.system("python generated_code.py")

# Chatbot Interface
def chatbot(df):
    st.subheader("🤖 Chatbot Interface")
    query = st.text_input("Ask the chatbot to visualize data (e.g., 'Bar chart for column A and column B'):")
    
    if query:
        # Extract plot type and column names from the query
        try:
            # Identify the plot type from the query
            if "bar" in query.lower():
                plot_type = "Bar Chart"
            elif "line" in query.lower():
                plot_type = "Line Plot"
            elif "scatter" in query.lower():
                plot_type = "Scatter Plot"
            elif "pie" in query.lower():
                plot_type = "Pie Chart"
            else:
                st.write("Unsupported plot type. Please ask for 'Bar', 'Line', 'Scatter', or 'Pie' charts.")
                return

            # Extract column names
            if plot_type == "Pie Chart":
                column_x = query.split("for")[-1].strip()
                column_y = None
            else:
                columns = query.split("for")[-1].strip().split("and")
                column_x, column_y = columns[0].strip(), columns[1].strip()

            # Check if columns exist in the DataFrame
            if column_x in df.columns and (column_y in df.columns or plot_type == "Pie Chart"):
                # Generate visualization code
                st.write(f"Generating {plot_type.lower()} for {column_x} and {column_y}..." if column_y else f"Generating {plot_type.lower()} for {column_x}...")
                code = generate_visualization_code(df, plot_type, column_x, column_y)

                # Show the generated code
                st.code(code, language="python")

                # Execute the generated code
                execute_code_and_visualize()

                # Display the visualization
                st.image("visualization.png", caption=f"{plot_type}: {column_x} vs {column_y}" if column_y else f"{plot_type}: {column_x}")
            else:
                st.write("Invalid column names. Please ensure the column names exist in the dataset.")
        except Exception as e:
            st.write(f"Error processing query: {e}")

# Main App
def main():
    st.title("Data Visualization Chatbot")
    if uploaded_file:
        chatbot(df)

if __name__ == "__main__":
    main()
