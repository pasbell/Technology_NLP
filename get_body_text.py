#Get body text of NYT article
def get_body(article_url):
    try:
        import requests
        from bs4 import BeautifulSoup


        article_response = requests.get(article_url)
        article_results = BeautifulSoup(article_response.content)


        body_paras = article_results.find_all('p',{"class":'css-exrw3m evys1bk0'})
        body = ""
        for para in body_paras:
            body = body + para.get_text()
        
        if (body == ""):
            body_paras = article_results.find_all('p',{"class":'css-1byx4j2'})
            body = ""
            for para in body_paras:
                body = body + para.get_text()
            
            body = body[:-35]
            
        return body
    except: 
        return ""

#Get URLs for NYT articles about technology
def get_article_urls(year, month, page_no):
    try:
        import time
        month_ends = {
            "01":"31",
            "02":"28",
            "03":"31",
            "04":"30",
            "05":"31",
            "06":"30",
            "07":"31",
            "08":"31",
            "09":"30",
            "10":"31",
            "11":"30",
            "12":"31",
        }

        import requests
        from bs4 import BeautifulSoup
        import json

        base_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"

        query = "?q=technology"
        qfilter = "&fq=document_type:article AND pub_year:{pub_year}"
        dates = "&begin_date={year}{month}01&end_date={year}{month}{month_end}"

        api_key = "&api-key=" + "Q5izy6Gwv1VhcOZHMdk72yQJFshZl6OK"
        page = "&page={page}"
        sort = "&sort=relevance"

        url_list = list()
        month = str(month).zfill(2)

        url = base_url + query + qfilter.format(pub_year = year) + page.format(page = str(page_no)) +\
            dates.format(year = str(year), month = month, month_end = month_ends[month]) + sort + api_key

        response = requests.get(url)
        content = json.loads(response.content)

        docs = content['response']['docs']

        for doc in docs:
            url = doc['web_url']
            url_list.append(url)
        time.sleep(6)
        return url_list
    except: 
        print(response)
        return list()


def join_text(x):
    seperator = ', '
    return seperator.join(x)


if __name__ == '__main__':
    import pandas as pd
    #Create Dataframe with months to include in analysis
    urls_df = pd.DataFrame(columns = {"Month", "urls"})
    all_months = pd.Series([(i,j) for i in range(1980, 2020) for j in range(1,13)])
    urls_df['Month'] = all_months

    
    page_nos = [i for i in range(3)]

    for page_no in page_nos:
        #Get urls
        urls_df['urls'] = all_months.apply(lambda x: (get_article_urls(x[0], x[1], page_no)))
        urls_df['urls'] = urls_df['urls'].apply(lambda x: x[1:-1].replace('\'', '').split(","))

        #Get Body data
        body_df = urls_df.copy()
        body_df['text'] = body_df['urls'].apply(lambda x: [get_body(i) for i in x]).apply(lambda x: join_text(x))

        #Save to csv
        body_df.to_csv("bodies_" + page_no)

