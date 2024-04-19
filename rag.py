
from dbs.db import get_top_n_chunks, add_chunks_to_db

query = """
build me an itinerary near a beach and with a hotel
"""

docs = get_top_n_chunks(query, topn=3, entity_type='beaches')
#print(docs[0].page_content)
for doc in docs:
    print(doc.page_content)
    print()

"""

{
    beaches: 0
    accomodation: 1
    casino: 1
    monumentos: 0
    ...
}

"""