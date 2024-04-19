import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# get absolute path to dbs folder
dbs_path = os.path.dirname(os.path.abspath(__file__))

persist_dir_accomodations = os.path.join(dbs_path, "accomodations_emb") # accomodations embedded database
persist_dir_beaches = os.path.join(dbs_path, "beaches_emb") # beaches embedded database
persist_dir_activities = os.path.join(dbs_path, "activities_emb") # activies embedded database
persist_dir_gardens = os.path.join(dbs_path, "gardens_emb") # gardens, parks, forests embedded database
persist_dir_thematicparks = os.path.join(dbs_path, "thematicparks_emb") # thematic parks embedded database
persist_dir_zoos = os.path.join(dbs_path, "zoos_emb") # zoos, aquariums embedded database
persist_dir_casinos = os.path.join(dbs_path, "casinos_emb") # casinos embedded database
persist_dir_museums = os.path.join(dbs_path, "museums_emb") # museums, monuments, touristic sites embedded database
persist_dir_default = os.path.join(dbs_path, "default_emb") # other entities embedded database

def get_persist_dir(db_name='default'):
    switch = {
        "accomodations": lambda: persist_dir_accomodations,
        "beaches": lambda: persist_dir_beaches,
        "activities": lambda: persist_dir_activities,
        "gardens": lambda: persist_dir_gardens,
        "thematicparks": lambda: persist_dir_thematicparks,
        "zoos": lambda: persist_dir_zoos,
        "casinos": lambda: persist_dir_casinos,
        "museums": lambda: persist_dir_museums,
        "default": lambda: persist_dir_default,
    }
    persist_dir = switch.get(db_name, switch["default"])()
    return persist_dir

def get_vector_db(db_name='default'):
    persist_dir = get_persist_dir(db_name)
    return Chroma(persist_directory=persist_dir, embedding_function=OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY))

# creates a chroma database given chunks (array of documents)
def create_vector_db_from_documents(chunks, entity_type='default'):
    db = Chroma.from_documents(chunks,
                               OpenAIEmbeddings(),
                               persist_directory=get_persist_dir(entity_type))
    db.persist()
    return db
    
# Given an array of documents (chunks), adds these chunks to the database and persists the changes in the disk
def add_chunks_to_db(documents, entity_type='default'):
    db = get_vector_db(entity_type)
    db.add_documents(documents)

    # Persist the updated database in disk
    db.persist()
    
# similarity search
def get_top_n_chunks(query, topn=1, entity_type='default'):
    db = get_vector_db(entity_type)
    chunks = db.similarity_search(query)
    return chunks[:topn]