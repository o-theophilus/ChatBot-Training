from flask import Blueprint

from llama_index import (
    GPTSimpleVectorIndex,
    LLMPredictor, PromptHelper, ServiceContext,
    download_loader
)
from langchain import OpenAI
from . import db, now
from uuid import uuid4

bp = Blueprint("brain", __name__)


def construct_index(data):
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

    reader = download_loader("StringIterableReader")
    documents = reader().load_data(texts=[data])

    index = GPTSimpleVectorIndex.from_documents(
        documents,
        service_context=service_context
    )

    return index.save_to_string()


def build_brain(data=None):
    if not data:
        data = db.data()

    training = ""

    for row in data:
        if row["type"] == "training":
            training = f"""
{training}
question: {row["question"]}
answer: {row["answer"]}
"""

    brain_data = construct_index(training)
    brain = db.get_brain(data)

    if brain:
        brain['"updated_at"'] = now()
        brain['data'] = brain_data
    else:
        brain = {
            "key": uuid4().hex,
            "created_at": now(),
            "updated_at": now(),
            "type": "brain",
            "data": brain_data
        }

    db.add(brain)
