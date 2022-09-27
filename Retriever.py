from haystack.nodes import TextConverter, PDFToTextConverter, DocxToTextConverter, PreProcessor
from haystack.utils import convert_files_to_docs, fetch_archive_from_http
from haystack.utils import clean_wiki_text, convert_files_to_docs, fetch_archive_from_http, print_answers
from haystack.nodes import FARMReader, TransformersReader
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import EmbeddingRetriever
from haystack.pipelines import ExtractiveQAPipeline
import time  # 引入time模块
from haystack.nodes import BM25Retriever
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import BM25Retriever
from haystack.pipelines import ExtractiveQAPipeline

# path = '../data.pdf'
'''
document_store = FAISSDocumentStore()
document_store.delete_documents()
'''
def prepare_retrieve(path, document_store, split_length=3):

    converter = PDFToTextConverter(remove_numeric_tables=True, valid_languages=["en"])
    doc_pdf = converter.convert(file_path=path)[0]

    preprocessor = PreProcessor(
        clean_empty_lines=True,
        clean_whitespace=True,
        clean_header_footer=True,
        split_by="sentence",
        split_length=split_length,
        split_respect_sentence_boundary=False,
        # remove_substrings = string_list
    )

    docs_default = preprocessor.process([doc_pdf])
    # print(f"n_docs_input: 1\nn_docs_output: {len(docs_default)}")
    # document_store.delete_documents()
    # FAISSDocumentStore.delete_documents()
    # el document_store
    # document_store = FAISSDocumentStore(faiss_index_factory_str="Flat")

    # document_store = FAISSDocumentStore.load(index_path="my_faiss")
    document_store.delete_documents()

    try:
        document_store = FAISSDocumentStore.load(index_path="../my_faiss")
        # print(document_store)
        # document_store = FAISSDocumentStore(index_path="my_faiss")
    except (TypeError, ValueError):
        document_store = FAISSDocumentStore()
        document_store.delete_documents()

    retriever = EmbeddingRetriever(
        document_store=document_store,
        embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1",
        model_format="sentence_transformers",
        use_gpu=True
    )

    #document_store.delete_documents()
    document_store.write_documents(docs_default, duplicate_documents='skip')
    document_store.update_embeddings(retriever)
    document_store.save("my_faiss")

    return document_store, retriever

'''
document_store = FAISSDocumentStore.load(index_path="my_faiss")
# documents = document_store.get_all_documents(return_embedding=True)
retriever = EmbeddingRetriever(
    document_store=document_store,
    embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1",
    model_format="sentence_transformers",
    use_gpu=True
)
'''

# document_store = FAISSDocumentStore.load(index_path="../my_faiss")

def return_candidate_documents(document_store, query, top_k=3):
    retriever = EmbeddingRetriever(
        document_store=document_store,
        embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1",
        model_format="sentence_transformers",
        use_gpu=True
    )
    candidate_documents = retriever.retrieve(
        query=query,
        top_k=top_k,
        # filters={"year": ["2015", "2016", "2017"]}
    )
    results = []
    for i in range(len(candidate_documents)):
        results.append(candidate_documents[i].content)
    return results

# d, retriever = prepare_retrieve(path)
# results = return_candidate_documents(document_store, top_k=3)
# print(results)
# print(candidate_documents[0].content)

# print(candidate_documents)

'''
from haystack.nodes import DensePassageRetriever
r = DensePassageRetriever(documents)
candidate_documents = retriever.retrieve(
    query="JiaWei Han ",
    top_k=10,
    #filters={"year": ["2015", "2016", "2017"]}
)
'''


# print(candidate_documents)
# print(documents[0].embedding)

def retrieve_content(document_store):
    candidate_documents = retriever.retrieve(
        query="international climate conferences",
        top_k=10,
        # filters={"year": ["2015", "2016", "2017"]}
    )

    '''
    retriever = BM25Retriever(document_store)

    p = ExtractiveQAPipeline(reader, retriever)
    '''
    return candidate_documents


# candidate_documents = retrieve_content(t)

# print(candidate_documents)

'''

document_store.write_documents(docs_default)

document_store = FAISSDocumentStore(faiss_index_factory_str="HNSW")

document_store.write_documents(docs)


retriever = EmbeddingRetriever(
    document_store=document_store,
    embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1",
    model_format="sentence_transformers",
    use_gpu=True
)

document_store.update_embeddings(retriever)

reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)

pipe = ExtractiveQAPipeline(reader, retriever)

start_time = time.time()
# You can configure how many candidates the reader and retriever shall return
# The higher top_k for retriever, the better (but also the slower) your answers.
prediction = pipe.run(
    query='What are the instances of Data Cube?', params={"Retriever": {"top_k": 3}, "Reader": {"top_k": 3}}
)

print_answers(prediction, details="maximum")
end_time = time.time()
print("耗时: {:.2f}秒".format(end_time - start_time))

'''