import json
import os
import weaviate
import weaviate.classes as wvc
import newspaper
"""
Class to support input into Weaviate database, including:
    - Adding a new news article
    - Deleting a news article
    - Searching database
"""

class DBManager():
    def __init__(self):
        try:
            self.client = self.create_client()
            self.client.collections.delete_all()

            self.news_article_schema = [
                wvc.config.Property(name="title", data_type=wvc.config.DataType.TEXT),
                wvc.config.Property(name="url", data_type=wvc.config.DataType.TEXT),
                wvc.config.Property(name="date", data_type=wvc.config.DataType.DATE),
                wvc.config.Property(name="news_site", data_type=wvc.config.DataType.TEXT),
                wvc.config.Property(name="keywords", data_type=wvc.config.DataType.TEXT_ARRAY),
                wvc.config.Property(name="summary", data_type=wvc.config.DataType.TEXT)
            ]
            self.articles_collection, retrieved = self.create_collection("Articles")
            if not retrieved:
                self.load_data('articles.txt')
        except Exception as e:
            print(f"\nFailed to initialize vector database :( \n{e}")
            exit(1)


    def create_client(self, weaviate_version = "1.24.10") -> weaviate.WeaviateClient:
        '''
        Connects to Weaviate instance running in Docker
        '''
        client = weaviate.connect_to_custom(
            http_host="localhost",
            http_port="8080",
            http_secure=False,
            grpc_host="localhost",
            grpc_port="50051",
            grpc_secure=False,
            headers = {
            "X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")
            }
        )
        return client


    def create_collection(self,
                          collection_name: str,
                          embedding_model: str = 'text-embedding-3-small',
                          model_dimensions: int = 512):
        """
        Create a Weaviate collection with a schema based on self.properties.
        If it already exists, just return it.
        """
        collection = None
        retrieved = True
        if self.client.collections.exists(collection_name):
            collection = self.client.collections.get(collection_name)
            return collection, retrieved
        else:
            retrieved = False
            collection = self.client.collections.create(
                name = collection_name, 
                properties = self.news_article_schema,
                vectorizer_config = wvc.config.Configure.Vectorizer.text2vec_openai(
                    model = embedding_model,
                    dimensions = model_dimensions
                ),
                generative_config = wvc.config.Configure.Generative.openai(model='gpt-3.5-turbo')
            )
        return collection, retrieved
    

    def load_data(self, data_file_path: str):
        '''
        Loads articles from a .txt file of article URLs into the collection.
        '''
        try:
            with open(data_file_path, 'r') as file:
                articles = file.readlines()
            for article in articles:
                self.add_to_collection(article)
        except:
            print(f"\n'{data_file_path}' does not exist.\n")
            exit(1)


    def add_to_collection(self, url: str):
        '''
        Accepts URL to a news article, creates Newspaper object, adds it to the collection.
        '''
        try:
            article = newspaper.article(url)
        except:
            print(f'\nFailed to fetch news article: {url}\n')
            return
        
        # Run before getting keywords & summary
        article.nlp()

        data = {
            "title": article.title,
            "url": article.url,
            "date": article.publish_date,
            "news_site": article.meta_site_name,
            "keywords": article.keywords,
            "summary": article.summary
        }

        try:
            self.articles_collection.data.insert(data)
        except :
            print(f'\nFailed to add item to collection: {url}\n')
    

    def search_articles_collection(self, query) -> str:
        '''
        Returns [title, url, date, site name, keywords, summary] of top 3 articles in json
        '''
        response = self.articles_collection.generate.near_text(query=query, limit=5)

        result = [article.properties for article in response.objects]

        return json.dumps(result, default=str)
