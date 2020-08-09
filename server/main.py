"""FastAPI Server"""
from bson.json_util import dumps
from bson.json_util import loads

from fastapi import Body, FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

import nlp.processing.text_processor as tp
import nlp.processing.pos_tagging as pos_tagging
import nlp.processing.active_voice as active_voice
import nlp.processing.passive_voice as passive_voice

import logging
from pymongo import MongoClient
from server.settings import DB_STORAGE
import spacy
import uvicorn

logging.basicConfig(filename='server.log', level=logging.DEBUG,
                    format='%(asctime)s: %(funcName)s - %(levelname)s - %(message)s')

# Spacy models init
spacy.prefer_gpu()
logging.info(spacy.prefer_gpu())
nlp_pos = tp.nlp_setup(spacy.load('en_core_web_sm'), 'pos')
nlp_task_creator = tp.nlp_setup(spacy.load('en_core_web_sm'), 'tense')

# Mongo db init
cluster = MongoClient(DB_STORAGE)
db = cluster.itb
collection = db.users

# FastAPI server
app = FastAPI()
app.mount("/_static", StaticFiles(directory="_static"), name="_static")


def add_user(session_id: str):
    """Add user to database by session_id

    Parameters
    ----------
    session_id: str,
        id of extenstion session

    Returns
    -------

    """
    sample_user = {
        "session_id": session_id,
    }
    collection.insert_one(sample_user)


def update_db(session_id, stats):
    """Update database by given session_id and statistics.

    Parameters
    ----------
    session_id: str,
        id of extension session
    stats: dict,
        user statistics from front-end task execution

    Returns
    -------

    """
    results = list(collection.find({"session_id": session_id}))
    if len(results) == 0:
        add_user(session_id)

    collection.update_one({"session_id": session_id}, {"$set": {"statistics": stats}})


@app.post(
    '/db/get_data', status_code=200,
)
async def get_data(
        session_id: str
):
    """Get data from the database by session_id.

    Parameters
    ----------
    session_id: str,
        id of extenstion session

    Returns
    -------
    200 if success, error code with "msg" field of details otherwise
    """
    try:
        data = list(collection.find({"session_id": session_id}))
        if len(data) == 0:
            logging.info(f'session id: {session_id} zero collection length')
            return {"statistics: null"}
        json_data = loads(dumps(data))
        stats = json_data[0]['statistics']
        result = {"statistics": stats}
        return result
    except Exception as e:
        logging.warning(f'request error occured: {e}')
        raise HTTPException(
            status_code=500, detail={"msg": e}
        )


@app.post('db/update', status_code=200)
async def update_data(

        extensionID: str = Body(str),
        json: dict = Body(None),
):
    """Get data from the database by session_id(extensionID) and user statistics.

    Parameters
    ----------
    extensionID: str,
        id of extenstion session
    json:  dict,
        user statistics from front-end task execution

    Returns
    -------
    200 if success, error code with "msg" field of details otherwise
    """
    try:
        stats = json['statistics']
        logging.info(f'update stats by id: {extensionID}')
        update_db(extensionID, stats)
        return
    except Exception as e:
        logging.warning(f'request error occured: {e}')
        raise HTTPException(
            status_code=500, detail={"msg": e}
        )


@app.post('/app/task', status_code=200)
async def process_task(
        text: str = Body(str),
        task: str = Body(str),
        specifiedTask: str = Body(str)
):
    """Process provided text with task

    Parameters
    ----------
    text: str,
        Text for analysis.
    task: str,
        Task to process, i.e.: Passive
    specifiedTask: str,
        Specification of general task, i.e.: Passive Continuous

    Returns
    -------
        List of tokens and their indices.
    """
    try:
        result = []
        if task == "POS":
            result = pos_tagging.pos_tag_search(nlp_pos, text, specifiedTask)

        if task == 'ACTIVE_VOICE':
            result = active_voice.active_voice_search_batches(nlp_task_creator, text, specifiedTask)

        if task == 'PASSIVE_VOICE':
            result = passive_voice.passive_voice_search_batches(nlp_task_creator, text, specifiedTask)
        return {"result": result}
    except Exception as e:
        logging.warning(f'request error occurred: {e}')
        raise HTTPException(
            status_code=500, detail={"msg": e}
        )


@app.post('/app/answer', status_code=200)
async def send_answer(
        text: str = Body(str),
        result: dict = Body(str),
):
    """Generate user statistics.

    Parameters
    ----------
    text: str,
        Text for analysis.
    result: List,
        List of tokens and their indices.

    Returns
    -------
    List of tokens and their indices, length of this result, and provided text
    """
    data = {"result": result, "num_of_result": len(result), "text": text}
    return data


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8050)
