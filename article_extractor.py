from bs4 import BeautifulSoup as bs
import requests
import pandas as pd


def get_content(URL):
    """
    This function extracts the content of the article from a URL.
    """
    soup = bs(requests.get(URL, timeout=3).content, 'html.parser')
    p = [i.text for i in soup.find_all('p')]
    b = [i.text for i in soup.find_all('b')]
    return p, b


# Loading the data contains the URLs:
df = pd.read_excel('Fake News Stories.xlsx', sheet_name='Sheet1', engine='openpyxl')
# Filtering only the "Fake" cases:
fake_news_df = df[df['Fake or Satire?'] == 'Fake'].copy()

# Creating a list to keep the content of the articles:
articles_content_1 = []
articles_content_2 = []

# Loop over the rows in the data set and extracting the content:
for row in fake_news_df['URL of article']:
    URL = row

    try:
        p, b = get_content(URL)
        articles_content_1.append(p) #paragraph
        articles_content_2.append(b) #bold text

    # Excepting cases such as the website doesn't exist anymore, the URL is broken
    # or it takes too much time to connect the server:

    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError, requests.exceptions.MissingSchema):
        articles_content_1.append([])
        articles_content_2.append([])

# Adding new column to our data set with the content of the articles:
fake_news_df['content_1'] = articles_content_1
fake_news_df['content_2'] = articles_content_2

# Saving it into a new file:
fake_news_df.to_csv(r'fake_news_df.csv', index=False)
print("Finished")
