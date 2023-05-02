
from llama_index import (
    GPTSimpleVectorIndex,
    LLMPredictor, PromptHelper, ServiceContext,
    StringIterableReader
)
from langchain import OpenAI
from . import db
from uuid import uuid4
from flask import request
import os


def construct_index(training_data):
    max_input_size = 4096
    num_outputs = 2000
    max_chunk_overlap = 20
    chunk_size_limit = 600

    prompt_helper = PromptHelper(
        max_input_size,
        num_outputs,
        max_chunk_overlap,
        chunk_size_limit=chunk_size_limit
    )

    os.environ["OPENAI_API_KEY"] = request.json["openai_api_key"]
    llm_predictor = LLMPredictor(
        llm=OpenAI(
            temperature=0.5,
            model_name="text-davinci-003",
            max_tokens=num_outputs
        )
    )

    service_context = ServiceContext.from_defaults(
        llm_predictor=llm_predictor,
        prompt_helper=prompt_helper
    )

    doc = StringIterableReader().load_data([training_data])
    index = GPTSimpleVectorIndex.from_documents(
        doc,
        service_context=service_context
    )

    return index.save_to_string()


def build_brain(training_data, data):
    brain_data = construct_index(training_data)
    brain = db.get_brain(data)

    if brain:
        brain["updated_at"] = db.now()
        brain['data'] = brain_data
    else:
        brain = {
            "key": uuid4().hex,
            "created_at": db.now(),
            "updated_at": db.now(),
            "type": "brain",
            "data": brain_data
        }

    db.add(brain)
