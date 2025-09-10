import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from whoosh.index import create_in, open_dir  
from whoosh.fields import Schema, TEXT, ID     
from whoosh.qparser import QueryParser         
import os
import tkinter as tk
from tkinter import scrolledtext


nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

def preprocess_text(text: str) -> str:
    text = str(text).lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    words = [stemmer.stem(word) for word in words if word not in stop_words]
    return " ".join(words)


class SimpleSearchEngine:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.vectorizer = TfidfVectorizer(max_features=10000)
        self.tfidf_matrix = self.vectorizer.fit_transform(df['clean_text'] + " " + df['clean_title'])

    def search(self, query: str, top_n: int = 5) -> pd.DataFrame:
        query_vec = self.vectorizer.transform([query])
        similarity = cosine_similarity(query_vec, self.tfidf_matrix)
        top_indices = similarity[0].argsort()[-top_n:][::-1]
        return self.df.iloc[top_indices][['title', 'source', 'category', 'label']]


class WhooshSearchEngine:
    def __init__(self, df: pd.DataFrame, index_dir: str = "indexdir"):
        self.df = df
        self.index_dir = index_dir
        if not os.path.exists(index_dir):
            os.mkdir(index_dir)
            self.create_index()

    def create_index(self):
        schema = Schema(
            id=ID(stored=True),
            title=TEXT(stored=True),
            text=TEXT(stored=True),
            source=TEXT(stored=True),
            category=TEXT(stored=True),
            label=TEXT(stored=True)
        )
        ix = create_in(self.index_dir, schema)
        writer = ix.writer()
        for _, row in self.df.iterrows():
            writer.add_document(
                id=str(_),
                title=row['title'],
                text=row['text'],
                source=row['source'],
                category=row['category'],
                label=row['label']
            )
        writer.commit()

    def search(self, query: str, top_n: int = 5) -> list[str]:
        ix = open_dir(self.index_dir)
        qp = QueryParser("text", schema=ix.schema)
        q = qp.parse(query)
        with ix.searcher() as searcher:
            results = searcher.search(q, limit=top_n)
            return [f"{r['title']} - {r['source']} - {r['label']}" for r in results]


file_path = "fake_news_dataset.csv"  
df = pd.read_csv(file_path)

df['source'] = df['source'].fillna('Unknown')
df['author'] = df['author'].fillna('Unknown')

df['clean_text'] = df['text'].apply(preprocess_text)
df['clean_title'] = df['title'].apply(preprocess_text)


tfidf_engine = SimpleSearchEngine(df)
whoosh_engine = WhooshSearchEngine(df)


def search_tfidf():
    query = entry.get()
    results = tfidf_engine.search(query, top_n=5)
    output.delete('1.0', tk.END)
    for i, row in results.iterrows():
        output.insert(tk.END, f"{row['title']} - {row['source']} - {row['label']}\n\n")

def search_whoosh():
    query = entry.get()
    results = whoosh_engine.search(query, top_n=5)
    output.delete('1.0', tk.END)
    for r in results:
        output.insert(tk.END, r + "\n\n")

root = tk.Tk()
root.title("Fake News Search Engine")

tk.Label(root, text="Enter search query:").pack(pady=5)
entry = tk.Entry(root, width=50)
entry.pack(pady=5)

tk.Button(root, text="Search TF-IDF", command=search_tfidf).pack(pady=5)
tk.Button(root, text="Search Whoosh", command=search_whoosh).pack(pady=5)

output = scrolledtext.ScrolledText(root, width=100, height=30)
output.pack(pady=10)

root.mainloop()
