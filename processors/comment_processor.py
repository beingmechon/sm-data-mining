import json
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sentence_transformers import SentenceTransformer
from transformers import BartTokenizer, BartForConditionalGeneration
from processor_interface import CommentProcessor

class CommentClusterSummarizer(CommentProcessor):
    def __init__(self):
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
        self.summarization_model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

    def get_similarity_matrix(self, comments):
        embeddings = self.model.encode(comments)
        return np.matmul(embeddings, embeddings.T)

    def get_cluster_labels(self, similarity_matrix, threshold=0.7, n_clusters=None, metric='precomputed', linkage='average'):
        clustering = AgglomerativeClustering(n_clusters=n_clusters, metric=metric, linkage=linkage, distance_threshold=threshold)
        cluster_labels = clustering.fit_predict(1 - similarity_matrix)
        return cluster_labels

    def generate_cluster_summaries(self, clusters):
        cluster_summaries = {}
        for cluster_id, sentences in clusters.items():
            input_text = "".join(sentences)
            input_length = len(input_text)
            char_limit = 50

            if input_length > char_limit:
                max_length = input_length if input_length < 150 else 150
                min_length = char_limit if input_length < char_limit else input_length

                inputs = self.tokenizer(input_text, return_tensors='pt', max_length=1024, truncation=True)
                summary_ids = self.summarization_model.generate(inputs['input_ids'], 
                                    num_beams=4, 
                                    min_length=min_length, 
                                    max_length=max_length, 
                                    length_penalty=1, 
                                    early_stopping=False, 
                                    temperature=150,
                                    repetition_penalty=0.5)
                summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)

                cluster_summaries[cluster_id] = summary.strip()
            else:
                print(f"Ignoring summarization for comments clusters with less than {char_limit} characters.")
                cluster_summaries[cluster_id] = input_text

        return cluster_summaries
