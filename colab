import requests
from bs4 import BeautifulSoup
import streamlit as st

def extract_data_from_url(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    title = soup.find("title").text

    metadescription = soup.find("meta", attrs={"name": "description"})["content"]

    headers = {"h1": [], "h2": [], "h3": [], "h4": [], "h5": [], "h6": []}
    for header_type in headers.keys():
        headers[header_type] = [header.text for header in soup.find_all(header_type)]
    
    return url, title, metadescription, headers["h1"], headers["h2"], headers["h3"], headers["h4"], headers["h5"], headers["h6"]

def extract_data_from_urls(urls):
    data = []
    for url in urls:
        data.append(extract_data_from_url(url))
    return data

def main():
    st.title("Web Data Extractor")
    st.write("Upload a file containing URLs to extract data from.")
    uploaded_file = st.file_uploader("Choose a file", type=["txt"])

    if uploaded_file is not None:
        urls = []
        with open(uploaded_file, "r") as file:
            for line in file:
                urls.append(line.strip())

        data = extract_data_from_urls(urls)

        st.write("Data extracted:")
        st.write(data)

if __name__ == "__main__":
    main()
