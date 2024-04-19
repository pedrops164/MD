# .\venv\Scripts\Activate.ps1

from dotenv import load_dotenv
from pathlib import Path
import os
from templates import ValidationTemplate, EntitiesTemplate, ItineraryTemplate, MappingTemplate
from dbs.db import get_top_n_chunks

def load_secets():
    load_dotenv()
    env_path = Path(".") / ".env"
    load_dotenv(dotenv_path=env_path)

    open_ai_key = os.getenv("OPENAI_API_KEY")
    google_palm_key = os.getenv("GOOGLE_PALM_API_KEY")

    return {
        "OPENAI_API_KEY": open_ai_key,
        "GOOGLE_PALM_API_KEY": google_palm_key,
    }


import logging
import time
# for Palm
#from langchain.llms import GooglePalm
from langchain_community.llms import GooglePalm
# for OpenAI
#from langchain.chat_models import ChatOpenAI
#from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain, SequentialChain

logging.basicConfig(level=logging.INFO)

class Agent(object):
    def __init__(
        self,
        open_ai_api_key,
        model="gpt-3.5-turbo",
        temperature=0,
        debug=True,
    ):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self._openai_key = open_ai_api_key

        self.chat_model = ChatOpenAI(model=model, temperature=temperature, openai_api_key=self._openai_key)
        self.validation_prompt = ValidationTemplate()
        self.entity_prompt = EntitiesTemplate()
        self.itinerary_prompt = ItineraryTemplate()
        self.mapping_prompt = MappingTemplate()

        self.validation_chain = self._set_up_validation_chain(debug)
        self.entity_identification_chain = self._set_up_entity_identification_chain(debug)
        self.agent_chain = self._set_up_agent_chain(debug)

    def _set_up_validation_chain(self, debug=True):
      
        # make validation agent chain
        validation_agent = LLMChain(
            llm=self.chat_model,
            prompt=self.validation_prompt.chat_prompt,
            output_parser=self.validation_prompt.parser,
            output_key="validation_output",
            verbose=debug,
        )
        
        # add to sequential chain 
        overall_chain = SequentialChain(
            chains=[validation_agent],
            input_variables=["query", "format_instructions"],
            output_variables=["validation_output"],
            verbose=debug,
        )

        return overall_chain
    
    def _set_up_entity_identification_chain(self, debug=True):
        entity_identification_agent = LLMChain(
            llm=self.chat_model,
            prompt=self.entity_prompt.chat_prompt,
            output_parser=self.entity_prompt.parser,
            output_key="entity_identification_output",
            verbose=debug,
        )
        
        # add to sequential chain 
        overall_chain = SequentialChain(
            chains=[entity_identification_agent],
            input_variables=["query", "format_instructions"],
            output_variables=["entity_identification_output"],
            verbose=debug,
        )

        return overall_chain
    
    def _set_up_agent_chain(self, debug=True):

        travel_agent = LLMChain(
            llm=self.chat_model,
            prompt=self.itinerary_prompt.chat_prompt,
            verbose=debug,
            output_key="agent_suggestion",
        )

        parser = LLMChain(
            llm=self.chat_model,
            prompt=self.mapping_prompt.chat_prompt,
            output_parser=self.mapping_prompt.parser,
            verbose=debug,
            output_key="mapping_list",
        )

        overall_chain = SequentialChain(
            chains=[travel_agent, parser],
            input_variables=["query", "format_instructions", "entities"],
            output_variables=["agent_suggestion", "mapping_list"],
            verbose=debug,
        )

        return overall_chain

    def build_itinerary(self, query):
        self.logger.info("Validating query")
        t1 = time.time()
        self.logger.info(
            "Calling validation (model is {}) on user input".format(
                self.chat_model.model_name
            )
        )
        validation_result = self.validation_chain(
            {
                "query": query,
                "format_instructions": self.validation_prompt.parser.get_format_instructions(),
            }
        )

        validation_test = validation_result["validation_output"].dict()
        t2 = time.time()
        self.logger.info("Time to validate request: {}".format(round(t2 - t1, 2)))

        if validation_test["plan_is_valid"].lower() == "no":
            self.logger.warning("User request was not valid!")
            print("\n######\n Travel plan is not valid \n######\n")
            print(validation_test["updated_request"])
            return None, None, validation_result

        else:
            # plan is valid
            self.logger.info("Query is valid")

            # identifying entities in users request
            self.logger.info("Identifying entities in user's request")
            t1 = time.time()
            identification_result = self.entity_identification_chain(
                {
                    "query": query,
                    "format_instructions": self.entity_prompt.parser.get_format_instructions(),
                }
            )
            rag_queries = [] # array with the rag chunks
            identification_test = identification_result["entity_identification_output"].dict()
            for key, value in identification_test.items():
                print(key, value)
                if value==True:
                    chunks = get_top_n_chunks(query, entity_type=key)
                    for doc in chunks:
                        rag_queries.append(doc.page_content)
            for chunks in rag_queries:
                print(chunks)
            entities: str = "\n\n".join(rag_queries)

            t2 = time.time()
            self.logger.info("Time to identify entities: {}".format(round(t2 - t1, 2)))

            #self.logger.info(
            #    "User request is valid, calling agent (model is {})".format(
            #        self.chat_model.model_name
            #    )
            #)

            self.logger.info("Getting travel suggestions")
            t1 = time.time()
            # getting travel suggestions
            agent_result = self.agent_chain(
                {
                    "query": query,
                    "format_instructions": self.mapping_prompt.parser.get_format_instructions(),
                    "entities": entities,
                }
            )

            trip_suggestion = agent_result["agent_suggestion"]
            list_of_places = agent_result["mapping_list"].dict()
            t2 = time.time()
            self.logger.info("Time to get suggestions: {}".format(round(t2 - t1, 2)))

            return trip_suggestion, list_of_places, validation_result
    


secrets = load_secets()
travel_agent = Agent(open_ai_api_key=secrets["OPENAI_API_KEY"],debug=True)

query1: str = """
        I want to do a 5 day roadtrip from Cape Town to Pretoria in South Africa.
        I want to visit remote locations with mountain views
        """

query2: str = """
        I want to walk from Cape Town to Pretoria in South Africa.
        I want to visit remote locations with mountain views
        """

query3: str = """
        I want to do a 5 day roadtrip from Braga to Algarve in Portugal.
        I want to visit remote locations with beaches
        """

query4: str = """
        I want to do a 2 day roadtrip in Braga, Portugal.
        I want to visit beaches and forests.
        Build me an itinerary.
        """

query5: str = """
        I want to do a 3 day roadtrip starting in Porto and finishing in Braga, Portugal.
        In the first day I want to visit beaches and touristic sites.
        In the second day I want to go to a zoo in the afternoon, and a casino in the evening.
        In the third day I want to spend my day in the hotel.
        Build me an itinerary.
        """

trip_suggestion, list_of_places, validation_result = travel_agent.build_itinerary(query5)
print("-----------------------------------------------------------------\n\n\n\n")
print("Query Exemplo:", query4)
print("-----------------------------------------------------------------\n\n\n\n")
print(trip_suggestion)
print("-----------------------------------------------------------------\n\n\n\n")
print(list_of_places)
print("-----------------------------------------------------------------\n\n\n\n")
print(validation_result)
print("-----------------------------------------------------------------\n\n\n\n")