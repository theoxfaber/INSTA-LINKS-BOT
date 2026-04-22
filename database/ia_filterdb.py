import logging
from struct import pack
import re
import base64
from pyrogram.file_id import FileId
from pymongo.errors import DuplicateKeyError
from umongo import Instance, Document, fields
from motor.motor_asyncio import AsyncIOMotorClient
from marshmallow.exceptions import ValidationError
from info import FILE_DB_URL, FILE_DB_NAME, COLLECTION_NAME, MAX_RIST_BTNS

try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    import asyncio
except ImportError:
    SentenceTransformer = None

_embed_model = None

def get_embed_model():
    global _embed_model
    if _embed_model is None and SentenceTransformer is not None:
        _embed_model = SentenceTransformer('all-MiniLM-L6-v2')
    return _embed_model

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


client = AsyncIOMotorClient(FILE_DB_URL)
db = client[FILE_DB_NAME]
instance = Instance.from_db(db)

@instance.register
class Media(Document):
    file_id = fields.StrField(attribute='_id')
    file_ref = fields.StrField(allow_none=True)
    file_name = fields.StrField(required=True)
    file_size = fields.IntField(required=True)
    file_type = fields.StrField(allow_none=True)
    mime_type = fields.StrField(allow_none=True)
    caption = fields.StrField(allow_none=True)
    vector = fields.ListField(fields.FloatField(), allow_none=True)

    class Meta:
        collection_name = COLLECTION_NAME


async def save_file(media):
    file_id, file_ref = unpack_new_file_id(media.file_id)
    file_name = re.sub(r"@\w+|(_|\-|\.|\+)", " ", str(media.file_name))
    vector = None
    model = get_embed_model()
    if model is not None:
        loop = asyncio.get_event_loop()
        vector = await loop.run_in_executor(None, lambda: model.encode(file_name).tolist())
    try:
        file = Media(
            file_id=file_id,
            file_ref=file_ref,
            file_name=file_name,
            file_size=media.file_size,
            file_type=media.file_type,
            mime_type=media.mime_type,
            vector=vector
        )
    except ValidationError:
        logger.exception('Error Occurred While Saving File In Database')
        return False, 2
    else:
        try:
            await file.commit()
        except DuplicateKeyError:      
            logger.warning(str(getattr(media, "file_name", "NO FILE NAME")) + " is already saved in database")
            return False, 0
        else:
            logger.info(str(getattr(media, "file_name", "NO FILE NAME")) + " is saved in database")
            return True, 1



async def semantic_search(query: str, max_results: int, offset: int = 0):
    model = get_embed_model()
    if model is None:
        return None
    
    loop = asyncio.get_event_loop()
    query_vector = await loop.run_in_executor(None, lambda: model.encode(query).tolist())
    
    pipeline = [
        {
             "$vectorSearch": {
                 "index": "vector_index",
                 "path": "vector",
                 "queryVector": query_vector,
                 "numCandidates": 100,
                 "limit": max_results + offset
             }
        },
        {
             "$project": {
                 "score": {"$meta": "vectorSearchScore"},
                 "file_id": "$_id", "file_ref": 1, "file_name": 1, "file_size": 1, "file_type": 1, "mime_type": 1, "caption": 1, "vector": 1
             }
        }
    ]
    try:
        cursor = Media.collection.aggregate(pipeline)
        results = await cursor.to_list(length=max_results + offset)
        if results and results[0].get("score", 0) > 0.65: # Lowered threshold for natural language queries
            results = results[offset:offset+max_results]
            return [Media(**{k: v for k, v in r.items() if k != 'score' and k != 'file_id'}, file_id=r['file_id']) for r in results], '', len(results)
    except Exception:
        cursor = Media.find({"vector": {"$exists": True}})
        all_docs = await cursor.to_list(length=10000)
        if all_docs:
            docs_vectors = np.array([doc.vector for doc in all_docs])
            query_vec_np = np.array(query_vector)
            
            # Simple cosine similarity via dot product (assuming vectors are normalized by the library)
            scores = docs_vectors.dot(query_vec_np)
            top_k_idx = np.argsort(scores)[::-1]
            
            if len(top_k_idx) > 0 and scores[top_k_idx[0]] > 0.65:
                top_k_idx = top_k_idx[offset:offset+max_results]
                res = [all_docs[i] for i in top_k_idx]
                return res, '', len(all_docs)
    return None

async def get_search_results(query, file_type=None, max_results=(MAX_RIST_BTNS), offset=0, filter=False):
    sem_results = await semantic_search(query, max_results, offset)
    if sem_results and sem_results[0]:
        return sem_results

    query = query.strip()
    if not query: raw_pattern = '.'
    elif ' ' not in query: raw_pattern = r'(\b|[\.\+\-_])' + query + r'(\b|[\.\+\-_])'
    else: raw_pattern = query.replace(' ', r'.*[\s\.\+\-_]')
    try: regex = re.compile(raw_pattern, flags=re.IGNORECASE)
    except: return [], '', 0
    filter = {'file_name': regex}
    if file_type: filter['file_type'] = file_type

    total_results = await Media.count_documents(filter)
    next_offset = offset + max_results
    if next_offset > total_results: next_offset = ''

    cursor = Media.find(filter)
    # Sort by recent
    cursor.sort('$natural', -1)
    # Slice files according to offset and max results
    cursor.skip(offset).limit(max_results)
    # Get list of files
    files = await cursor.to_list(length=max_results)
    return files, next_offset, total_results


async def get_file_details(query):
    filter = {'file_id': query}
    cursor = Media.find(filter)
    filedetails = await cursor.to_list(length=1)
    return filedetails

async def get_all_file_names():
    return await Media.collection.distinct("file_name")


def encode_file_id(s: bytes) -> str:
    r = b""
    n = 0
    for i in s + bytes([22]) + bytes([4]):
        if i == 0:
            n += 1
        else:
            if n:
                r += b"\x00" + bytes([n])
                n = 0
            r += bytes([i])
    return base64.urlsafe_b64encode(r).decode().rstrip("=")


def encode_file_ref(file_ref: bytes) -> str:
    return base64.urlsafe_b64encode(file_ref).decode().rstrip("=")


def unpack_new_file_id(new_file_id):
    """Return file_id, file_ref"""
    decoded = FileId.decode(new_file_id)
    file_id = encode_file_id(
        pack(
            "<iiqq",
            int(decoded.file_type),
            decoded.dc_id,
            decoded.media_id,
            decoded.access_hash
        )
    )
    file_ref = encode_file_ref(decoded.file_reference)
    return file_id, file_ref
