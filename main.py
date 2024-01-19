import streamlit as st
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import openai

# Set your OpenAI GPT-3 API key
openai.api_key = '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'

def generate_introductory_lines(data):
    prompt = f"Summarize this business information:\n{data}\n\nGenerate introductory lines compliment what they are doing must be of 2 line compliment in a sense of 2nd person"
    prompt_obj = {"role": "user", "content": f"{prompt}"}
    messages = [prompt_obj]
    
    # Use the OpenAI API to generate text
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages
    )
    
    assistant_response = response['choices'][0]['message']["content"].strip()
    message = {"role": "assistant", "content": assistant_response}
    messages.append(message)
    
    return assistant_response



 # Check the status code
import streamlit as st
import requests  # Import the requests module

# Assuming you have a function scrape_website(url) for scraping website information
# Assuming you have a function generate_intro(lines) for generating introductory lines using GPT-3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
max_length = 300
def scrape_website(url):
    # Initialize Selenium webdriver with Gecko Driver
    if url.split(":")[0] == "https":
        url = url
    else:
        url = f"https://{url}"

    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options)

    try:
        # Open the website
        driver.get(url)

        # Use WebDriverWait to wait for an element to be present before proceeding
        wait = WebDriverWait(driver, 2)
        wait.until(EC.presence_of_element_located((By.XPATH, "//p|//h1|//h2|//h3|//h4|//h5|//h6")))

        # Extract relevant information using appropriate Selenium commands
        text_elements = driver.find_elements(By.XPATH, "//p|//h1|//h2|//h3|//h4|//h5|//h6")
        text_elements = driver.find_elements(By.XPATH, "//p|//h3|//h6|//h1")
        

        extracted_text = ' '.join(element.text for element in text_elements)

        return extracted_text[:300]

        

    except TimeoutException:
        print(f"Timed out waiting for elements to load on {url}")
    except Exception as e:
        print(f"Error: {e} on {url}")
    finally:
        # Close the browser window
        driver.quit()


FIELDNAME = "M"
def process_record(record, i):
    fields = record.get("fields", {})
    record_id = fields.get(FIELDNAME)

    # Apply custom styling to the title
    st.write(f"Row #: {i}")
    # Display the record id
    st.write(f"Record ID: {record_id}")

    # Scrape the website to extract business information
    website_url = fields.get(FIELDNAME, "")  # Replace with the actual field name in your Airtable
    business_info = scrape_website(website_url)

    # Generate introductory lines using GPT-3
    if business_info:
        intro_lines = generate_introductory_lines(business_info)

        # Apply custom styling to the introductory lines
        st.markdown(f'#####{intro_lines}')

        # Display a separator
        st.markdown("---")
    else:
        st.warning("Failed to scrape website for business information.")

def process_records(record):
    fields = record.get("fields", {})
    record_id  = fields.get(FIELDNAME)

    # Display the record id
    st.write(f"Record : {record_id}")
# Replace with the actual field name in your Airtable
    business_info = scrape_website(record_id)

    # Generate introductory lines using GPT-3
    if business_info:
        intro_lines = generate_introductory_lines(business_info)

        # Apply custom styling to the introductory lines
        st.markdown(f'#####{intro_lines}')

        # Display a separator
        st.markdown("---")
    else:
        st.warning("Failed to scrape website for business information.")
    return None
    
def main():
    YOUR_TOKEN = "pattonUdT0LYNSkmj.461ac2a6afc7a3ada758a5640b34b29aa382422ae850a79d4a8022516192470b"
    BASE_ID = "app6EeISye5oVXslP"
    TABLE_NAME = "Website%20URLs"  # Note: Replace spaces with %20 in the table name
    
    # Airtable API endpoint URL
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"

    # Headers with Authorization
    headers = {
        "Authorization": f"Bearer {YOUR_TOKEN}",
    }

    # Make a GET request to retrieve records
    response = requests.get(url, headers=headers)

    # Display title and description
    st.title("Interactive GPT-3.5 Turbo Intro Generator")

    if response.status_code == 200:
        data = response.json()
        records = data.get("records", [])
        
        if st.button("GENERATE FOR ALL THE ROWS"):
            # Display the total number of records
            st.sidebar.write(f"#     Total Records: {len(records)}")  # Display total records in the sidebar
            # Process all records
            for i, record in enumerate(records, start=1):
                process_record(record, i)

                # Add a progress bar
                progress_percentage = (i / len(records)) * 100

            st.success("All records processed successfully!")

        generate_range = st.checkbox("Generate Intros for the Specified Range")
        if generate_range:
            st.sidebar.write(f"#     Total Records: {len(records)}")
            start_record = st.number_input("Enter Start Record Number (Row):")
            end_record = st.number_input("Enter End Record Number (Row):")
            start_record = int(start_record)
            end_record = int(end_record)
            if st.button("Generate Intros for the Specified Range"):
                if start_record <= end_record:
                    # Process records within the specified range
                    for record_number, record in enumerate(records[start_record-1:end_record], start=start_record):
                        process_records(record)

                    st.success("Records {} to {} processed successfully!".format(start_record, end_record))
                else:
                    st.warning("Invalid range. Please ensure that the start record number is less than or equal to the end record number.")



                

if __name__ == "__main__":
    main()