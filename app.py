import streamlit as st
import pandas as pd
import io

def process_excel(file, account_column, share_column):
    # Load the Excel file
    excel_data = pd.ExcelFile(file)
    
    # Parse the first sheet
    df = excel_data.parse(excel_data.sheet_names[0])
    
    # Check if the provided columns exist in the DataFrame
    if account_column not in df.columns or share_column not in df.columns:
        raise KeyError("One or both specified columns are not found in the file.")
    
    # Group by the user-specified account column and sum the user-specified share column
    grouped_df = df.groupby(account_column, as_index=False)[share_column].sum()
    
    # Sort by the account column
    sorted_grouped_df = grouped_df.sort_values(by=account_column)
    
    return sorted_grouped_df

def main():
    st.title('Excel File Processor')
    
    # File uploader
    uploaded_file = st.file_uploader("Upload your Excel file", type=['xlsx'])
    
    if uploaded_file is not None:
        # Get user input for column names
        account_column = st.text_input('Enter the column name for account ID or number (e.g., "acc"):', 'acc')
        share_column = st.text_input('Enter the column name for the share amount (e.g., "fr"):', 'fr')
        
        # Validate column names and process the file
        if account_column and share_column:
            try:
                # Process the file
                processed_df = process_excel(uploaded_file, account_column, share_column)
                
                # Convert DataFrame to Excel
                output = io.BytesIO()
                with pd.ExcelWriter(output) as writer:  # Use default engine
                    processed_df.to_excel(writer, index=False, sheet_name='Processed Data')
                output.seek(0)
                
                # Provide download link
                st.download_button(
                    label="Download Processed File",
                    data=output,
                    file_name="processed_file.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except KeyError as e:
                st.error(f"Error: {e}")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
