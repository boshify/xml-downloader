import streamlit as st
import requests
from requests.auth import HTTPBasicAuth

# Streamlit app interface
st.title("XML File Downloader")

# URL input
xml_url = st.text_input("Enter the URL of the XML file to download:")

# Username and password input (optional)
username = st.text_input("Username (optional)", value="", type="default")
password = st.text_input("Password (optional)", value="", type="password")

# Download button
if st.button("Download XML File"):
    if xml_url:
        try:
            # Prepare authentication if username and password are provided
            auth = HTTPBasicAuth(username, password) if username and password else None

            # Start the download request with streaming enabled
            with requests.get(xml_url, stream=True, auth=auth) as response:
                response.raise_for_status()
                total_size = int(response.headers.get('content-length', 0))
                downloaded_size = 0
                chunk_size = 8192

                # Use Streamlit's progress bar
                progress_bar = st.progress(0)

                # Download the file in chunks
                xml_content = b""
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:  # filter out keep-alive chunks
                        xml_content += chunk
                        downloaded_size += len(chunk)
                        progress = int(downloaded_size / total_size * 100) if total_size > 0 else 0
                        progress_bar.progress(progress)

                # Display download completion message
                st.success("Download complete!")

                # Provide a download button for the downloaded XML file
                st.download_button(
                    label="Download XML",
                    data=xml_content,
                    file_name="downloaded_file.xml",
                    mime="application/xml"
                )

        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a valid URL.")
