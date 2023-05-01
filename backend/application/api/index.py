from flask import Blueprint, jsonify  # , request
from llama_index import (
    GPTSimpleVectorIndex,
    LLMPredictor, PromptHelper, ServiceContext,
    download_loader
)
from langchain import OpenAI
from . import db, now  # ,dd
# import io
from uuid import uuid4

bp = Blueprint("index", __name__)


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


@bp.post("/index")
def post():

    trainings = db.get_type("training")
    trainings.reverse()
    data = ""

    for x in trainings:
        data = f"""
{data}
question: {x["question"]}
answer: {x["answer"]}"""

    index = construct_index(data)

    # dd.add(io.StringIO(index))
    db.add({
        "key": uuid4().hex,
        "created_at": now(),
        "updated_at": now(),
        "type": "index",
        "data": index
    })

    return jsonify({
        "status": 200,
        "message": "successful",
    })
