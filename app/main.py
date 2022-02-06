# PrivacyChain
# A framework for personal data persistence in DLT applications for compliance to rtbf and right to retification 
# of the LGPD - Brazilian law for personal data protection.
# author: Anderson Boa Morte
# timestamp: 2021-05-17T00:55:59+00:00

from __future__ import annotations

import hashlib
import json
from typing import Optional
from fastapi import responses

import uvicorn
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Body

from pydantic import BaseModel, Field

import app.bib as bib
from app.utils import Blockchain, HashMethod

from web3 import Web3
import random

from hexbytes import HexBytes

from typing import List
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

from datetime import datetime

from http import HTTPStatus

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DEFAULT_BLOCKCHAIN = Blockchain.ETHEREUM
DEFAULT_HASHMETHOD = HashMethod.SHA256

tags_metadata = [
    {"name": "Pure Functions", "description": "Pure functions of the functional programmation"},
    {"name": "Operations", "description": "Operations"},
    {"name": "Transactions", "description": "Transactions"},
]

app = FastAPI(
    title='PrivacyChain',
    description='REST API specification for PrivacyChain (Personal Data Persistence for DLT)',
    version='1.0.0',
    openapi_tags=tags_metadata
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MyCustomException(Exception):
    def __init__(self, message: str):
        self.message = message

@app.exception_handler(MyCustomException)
async def MyCustomExceptionHandler(request: Request, exception: MyCustomException):
    return JSONResponse (status_code = 500, content = {"message": exception.message})

class HexJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, HexBytes):
            return obj.hex()
        return super().default(obj)
    

class Entity(BaseModel):
    content: str = Field(None, title="Entity content for request",
                         description="entity represent a object in json format in canonical form.")

class AnonymizeResponse(BaseModel):
    content: str = Field(None, title="Anonymized data", description="Anonymized data")
    
AnonymizeResponse_Example = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": {"content": "3d476e5fd240c4cf69d299b381e45c28024ab8eed735ba45f4f0746c65c7e3eb"}
            }
        }
    },
}

SecureAnonymizeResponse_Example = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": {"content": "b78676db55add54c5f50b3afc66d9255d546873b18d0febdf13430867427ecc4"}
            }
        }
    },
}



class Secure(BaseModel):
    content: str = Field(None, title="Entity content for request",
                         description="entity represent a object in json format in canonical form.")
    salt: str = Field(None, title="Salt", description="salt value result of UUIDv4 function.")

class VerifySecureAnonymizeResponse(BaseModel):
    result: bool = Field(None, title="Verify Anonymized data", description="Verify Anonymized data")

VerifySecureAnonymizeResponse_Example = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": {"result": True}
            }
        }
    },
}

VerifySecureImmutableRegister_Example = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": {"result": True}
            }
        }
    },
}

class RegisterOnChainResponse(BaseModel):
    transaction_id: str = Field(None, title="Transaction´s Id registered", description="Transaction´s Id registered")

RegisterOnChainResponse_Example = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": {"transaction_id": "0x2826ff7616850240ab914b986e50e353c607ef1014149d6b87f1946883d37668"}
            }
        }
    },
}

class GetOnChainResponse(BaseModel):
    hash: str = Field(None, title="Response content", description="")
    nonce: str = Field(None, title="Response content", description="")
    blockhash: str = Field(None, title="Response content", description="")
    blockNumber: str = Field(None, title="Response content", description="")
    transactionIndex: str = Field(None, title="Response content", description="")
    FROM: str = Field(None, title="Response content", description="")
    to: str = Field(None, title="Response content", description="")
    value: str = Field(None, title="Response content", description="")
    gas: str = Field(None, title="Response content", description="")
    gasPrice: str = Field(None, title="Response content", description="")
    input: str = Field(None, title="Response content", description="")
    v: str = Field(None, title="Response content", description="")
    r: str = Field(None, title="Response content", description="")
    s: str = Field(None, title="Response content", description="")

GetOnChainResponse_Example = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": {"hash": "0x2826ff7616850240ab914b986e50e353c607ef1014149d6b87f1946883d37668", 
                         "nonce": "8",
                         "blockhash": "0xb20fbdb0fb35390ccd884d4015761858cfaf9be5102ce21811d551a105523b27",
                         "blockNumber": "72",
                         "transactionIndex": "0",
                         "FROM": "0x1eca7eD6322B410219Ef953634442AF33aB05BA3",
                         "to": "0xE9Ae49e3F7B2134D55812296E635b01697C41542",
                         "value": "1",
                         "gas": "121512",
                         "gasPrice": "20000000000",
                         "input": "0xb78676db55add54c5f50b3afc66d9255d546873b18d0febdf13430867427ecc4",
                         "v": "38",
                         "r": "0x377cdb34a0277f028ed0e801f85e8e7ca20b33758df6b9a7fdd1151270ca0aca",
                         "s": "0x2e03fcdd12ae72011902e6884cb60f46228d056b493ad27313f2361891a3814c"}
            }
        }
    },
}
    
SetDefaultBlockchain_Example = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": {"blockchain_id": "Blockchain.ETHEREUM"}
            }
        }
    },
}
   
RegisterOffChain_Example = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": {"index_id": 6469}
            }
        }
    },
}    

RemoveOffChain_Example = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": {"index_id": 5468}
            }
        }
    },
}    

RemoveOnchain_Example = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": {"result": True}
            }
        }
    },
}    


IndexOnChain_Example = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": {"index_id": 251}
            }
        }
    },
}    

RectifyOffChain_Example = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": {"index_id": 6564}
            }
        }
    },
}    

RectifyOnChain_Example = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": {"transaction_id": "0x2826ff7616850240ab914b986e50e353c607ef1014149d6b87f1946883d37668"}
            }
        }
    },
}    

IndexSecureOnChain_Example = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": {"index_id": 65498}
            }
        }
    },
}    

UnindexOnChain_Example = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": {"result": True}
            }
        }
    },
}    


class Response(BaseModel):
    content: str = Field(None, title="Response content", description="")
        
class Verify(BaseModel):
    content: str = Field(None, title="Entity content for request",
                         description="entity represent a object in json format in canonical form.")
    anonymized: str = Field(None, title="Anonymized data", description="result of secure anonimization.")
    salt: str = Field(None, title="Salt", description="salt value result of UUIDv4 function.")
    
class OnChain(BaseModel):
    content: str = Field(None, title="Anonymized data", description="result of secure anonimization.")
    
class GetOnChain(BaseModel):
    transaction_id: str = Field(None, title="Transaction ID", description="transaction identifier")
    
class IndexOnChain(BaseModel):
    to_wallet: str = Field(None, title="Home wallet", description="random home wallet address.")
    from_wallet: str = Field(None, title="Destination wallet", description="random destination wallet address.")
    content: str = Field(None, title="Anonymized data", description="result of secure anonimization.")
    locator: str = Field(None, title="Entity locator", description="Entity locator")    
    datetime: str = Field(None, title="timestamp", description="timestamp")    

class IndexOnChainS(BaseModel):
    to_wallet: str = Field(None, title="Home wallet", description="random home wallet address.")
    from_wallet: str = Field(None, title="Destination wallet", description="random destination wallet address.")
    content: str = Field(None, title="Anonymized data", description="result of secure anonimization.")
    locator: str = Field(None, title="Entity locator", description="Entity locator")    
    datetime: str = Field(None, title="timestamp", description="timestamp")        
    salt: str = Field(None, title="Salt", description="salt value result of UUIDv4 function.")

class UnindexOnChain(BaseModel):
    locator: str = Field(None, title="Entity locator", description="Entity locator")    
    datetime: str = Field(None, title="timestamp", description="timestamp")        
    
class verifySecureImmutable(BaseModel):
    transaction_id: str = Field(None, title="Transaction ID", description="transaction identifier")
    content: str = Field(None, title="Entity content for request",
                         description="entity represent a object in json format in canonical form.")
    salt: str = Field(None, title="Salt", description="salt value result of UUIDv4 function.")    
    
class rectifyOnChain(BaseModel):
    content: str = Field(None, title="Entity content for request",
                        description="entity represent a object in json format in canonical form.")
    salt: str = Field(None, title="Salt", description="salt value result of UUIDv4 function.")
    to_wallet: str = Field(None, title="Home wallet", description="random home wallet address.")
    from_wallet: str = Field(None, title="Destination wallet", description="random destination wallet address.")
    locator: str = Field(None, title="Entity locator", description="Entity locator")    
    datetime: str = Field(None, title="timestamp", description="timestamp")      
    
class removeOnChain(BaseModel):
    locator: str = Field(None, title="Entity locator", description="Entity locator")    
    datetime: str = Field(None, title="timestamp", description="timestamp")              


#@app.get("/")        
#def root():
#    return {"PrivacyChain endpoints."}     
    
"""
@app.get('/classify/{entity}/{type}')
def classification(entity: str, type: TypeClassification) -> json:
 
        [EXPANDED] E → ⟦PII, PPII, NPII⟧ \n
        \t Classify the attributes of an entity E in PII, PPII and NPII
        
        [SUMMARIZED] E → ⟦PI, NPII⟧ \n
        \t Classify the attributes of an entity E in PI and NPII

    return entity
"""

@app.post('/simpleAnonymize/', tags=["Pure Functions"], response_model=AnonymizeResponse, responses=AnonymizeResponse_Example)
def simple_anonymize(data: Entity = Body(
    ...,
    example={
        "content": "{cpf:72815157071, exam:HIV, datetime:2021-09-14T19:50:47.108814, result:POS}"
    },
), hashMethod: Optional[str] = "SHA256") -> json:
    """
        A = α (D, h) \n 
        \t Anonymizes D by generates A through hash function h (optional), default SHA256.  
    """
    anonymizedData = ""

    try:
        hashData = {'content': hashlib.sha256(data.content.encode()).hexdigest()}
        hashData = json.dumps(hashData)
        anonymizedData = json.loads(hashData)
    except Exception as e:
        raise MyCustomException(message = str(e))
    return anonymizedData


@app.post('/secureAnonymize/', tags=["Operations"], response_model=AnonymizeResponse, responses=SecureAnonymizeResponse_Example)
def secure_anonymize(data: Secure = Body(
    ...,
    example={
        "content": "{cpf:72815157071, exam:HIV, datetime:2021-09-14T19:50:47.108814, result:POS}",
        "salt": "4efc1400-29b8-40b7-9bd7-7fce480b39e8"
    },
), hashMethod: Optional[str] = 'SHA256') -> bool:
    """
        A = γ(D,s,h) \n 
        \t Anonymizes D (with a salt 's') by generates A through hash function h (optional), default SHA256.  
    """
    try:    
        anonymizedData = ""

        if data.salt == "":
            salt = bib.salt()
        else:
            salt = data.salt

        # dict to object Entity
        s_content = data.content[:-1] + ', salt:' + salt + "}"
        entit_dict = {
            'content': s_content
        }

        entity = Entity(**entit_dict)
        anonymizedData = simple_anonymize(entity, hashMethod)
    except Exception as e:
        raise MyCustomException(message = str(e))
    return anonymizedData

@app.get('/verifySecureAnonymize/', tags=["Pure Functions"], response_model=VerifySecureAnonymizeResponse, responses=VerifySecureAnonymizeResponse_Example)
def verify_secure_anonymize(data: Verify = Body(
    ...,
    example={
        "content": "{cpf:72815157071, exam:HIV, datetime:2021-09-14T19:50:47.108814, result:POS}",
        "anonymized": "b78676db55add54c5f50b3afc66d9255d546873b18d0febdf13430867427ecc4",
        "salt": "4efc1400-29b8-40b7-9bd7-7fce480b39e8"
    },
), hashMethod: Optional[str] = 'SHA256') -> bool:
    """
        Γ(A,D,s,h)  \n 
        \t Verify whether the value 'A'  is the result of anonimyze secure of D with salt s and hash h    
    """
    try:
        # dict to object Secure
        entit_dict = {}
        entit_dict['content'] = data.content
        entit_dict['salt'] = data.salt

        secure = Secure(**entit_dict)
        return_secure_anonymize = secure_anonymize(secure)['content']

        if (return_secure_anonymize == data.anonymized):
            result = {'result': True}
        else:
             result = {'result': False}    
             
        resultDump = json.dumps(result)
        resultJson = json.loads(resultDump)
    
        return resultJson
    
    except Exception as e:
        raise MyCustomException(message = str(e))

@app.post('/setDefaultBlockchain/{blockchain}', tags=["Pure Functions"], responses=SetDefaultBlockchain_Example)
def set_default_blockchain(blockchain: Blockchain):
    """
        Δ(β) \n 
        \t Makes privacychain adopt β as the default blockchain:
         
         \t 1: "HYPERLEDGER" \n
         \t 2: "ETHEREUM (default)" \n
         \t 3: "BITCOIN" \n
    """
    blockchain = {
        1: "HYPERLEDGER",
        2: "ETHEREUM",
        3: "BITCOIN"
    }

    try:
        DEFAULT_BLOCKCHAIN = blockchain.get(int(blockchain.value))
    except Exception as e:
        DEFAULT_BLOCKCHAIN = Blockchain.ETHEREUM
        raise MyCustomException(message = str(e))
    finally:
        return DEFAULT_BLOCKCHAIN

@app.post('/registerOnChain/', tags=["Operations"], response_model=RegisterOnChainResponse, responses=RegisterOnChainResponse_Example)
def register_onchain(data: OnChain = Body(
    ...,
    example={
        "content": "b78676db55add54c5f50b3afc66d9255d546873b18d0febdf13430867427ecc4"
    }
    )) -> json:
    """
        T_β=W(d,β) \n 
        \t Persist array bytes d in blockchain β
    """
    try:
        # HTTPProvider:
        w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
        
        # Randomly to get 'to' and 'from' address of the ganache address list
        lst_address = w3.eth.accounts
        source = random.choice(lst_address)
        target = random.choice(lst_address)

        transaction_id_return = ""
        
        print("registerOnChain: " + data.content)
        
        # send Transaction
        transaction_id_hex =  w3.eth.send_transaction({'to': target, 
                                'from': source, 
                                'value': 1,
                                'data': data.content})
        
        transaction_id = {'transaction_id': transaction_id_hex.hex()}
        transaction_id_json = json.dumps(transaction_id)
        transaction_id_return = json.loads(transaction_id_json)
        return transaction_id_return
    except Exception as e:
        raise MyCustomException(message = str(e))

@app.post('/registerOffChain/', tags=["Operations"], status_code=HTTPStatus.NO_CONTENT)
def register_offchain():
    """
        INSERT in application SGBD \n 
        \t In pratice is a insert in the application SGBD
    """
    return Response(status_code=HTTPStatus.NO_CONTENT.value)
    
@app.get('/getOnChain/', tags=["Operations"], response_model=GetOnChainResponse, responses=GetOnChainResponse_Example)
def get_onchain(data: GetOnChain = Body(
    ...,
    example={
        "transaction_id": "0x2826ff7616850240ab914b986e50e353c607ef1014149d6b87f1946883d37668"
    }
    )) -> json:
    """
        d=R(T_β,β) \n 
        \t In blockchain β, get d bytes array (registered under transaction T_β) 
    """  
    try:
        # HTTPProvider:
        w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
    
        # get Transaction
        tx = w3.eth.get_transaction(data.transaction_id)
        tx_dict = dict(tx)
        tx_str = json.dumps(tx_dict, cls=HexJsonEncoder)
        tx_json = json.loads(tx_str)
        
        return GetOnChainResponse.parse_obj(tx_json)
    except Exception as e:
        raise MyCustomException(message = str(e))
    
@app.post('/indexOnChain/', tags=["Operations"], responses=IndexOnChain_Example)
def index_onchain(data: "IndexOnChain" = Body(
    ...,
    example={
        "to_wallet": "0x1eca7eD6322B410219Ef953634442AF33aB05BA3",
        "from_wallet": "0x190e97032E45A1c3E1D7E2B1460b62098A5419ab",
        "content": "{cpf:72815157071, exam:HIV, datetime:2021-09-14T19:50:47.108814, result:POS}",
        "locator": "72815157071",
        "datetime": "2021-09-14T19:50:47.108814"
    }
    ), db: Session = Depends(get_db), hashMethod: Optional[str] = 'SHA256') -> json:
    """
        I(L_E,t,d,β) \n 
        \t Records in the blockchain β the data d of an entity E identified by the locator L_E, associating the timestamp t. 
    """  
    try:     
        # dict to object Entity
        entit_dict = {}
        entit_dict['content'] = data.content
        entity = Entity(**entit_dict)
        
        anonymizedData = simple_anonymize(entity)['content']

        # dict to object OnChain
        entit_dict = {}
        entit_dict['content'] = anonymizedData
        onchain = OnChain(**entit_dict)
        
        transaction_id = register_onchain(onchain)['transaction_id']
 
        now = datetime.now()
        
        # dict to object schemas.TrackingCreate
        entit_dict = {}
        entit_dict['canonical_data'] = data.content
        entit_dict['anonymized_data'] = anonymizedData       
        entit_dict['blockchain_id'] = DEFAULT_BLOCKCHAIN
        entit_dict['transaction_id'] = transaction_id                       
        entit_dict['salt'] = ""                               
        entit_dict['hash_method'] = HashMethod(DEFAULT_HASHMETHOD).name                                
        entit_dict['tracking_dt'] = now.strftime("%Y-%m-%dT%H:%M:%S.%f")
        entit_dict['locator'] = data.locator
        trackingCreate = schemas.TrackingCreate(**entit_dict)

        db_tracking = crud.get_tracking_by_transaction_id(db, transaction_id)
        
        if db_tracking:
            raise HTTPException(status_code=400, detail="Transaction already registered")        
        return crud.create_tracking(db=db, tracking=trackingCreate)
    except Exception as e:
        raise MyCustomException(message = str(e))


@app.post('/indexSecureOnChain/', tags=["Operations"], responses=IndexSecureOnChain_Example)
def index_secure_onchain(data: IndexOnChainS = Body(
    ...,
    example={
        "to_wallet": "0x1eca7eD6322B410219Ef953634442AF33aB05BA3",
        "from_wallet": "0x190e97032E45A1c3E1D7E2B1460b62098A5419ab",
        "content": "{cpf:72815157071, exam:HIV, datetime:2021-09-14T19:50:47.108814, result:POS}",
        "locator": "72815157071",
        "datetime": "2021-09-14T19:50:47.108814",
        "salt": "e3719002-8c09-4c8f-8da3-9f5ce34c2d76"
    }
    ), db: Session = Depends(get_db), hashMethod: Optional[str] = 'SHA256') -> json:
    try:     
        # dict to object Secure
        secure_dict = {}
        secure_dict['content'] = data.content
        secure_dict['salt'] = data.salt        
        secure = Secure(**secure_dict)
        
        secureAnonymizedData = secure_anonymize(secure)['content']
        
        # dict to object OnChain
        entit_dict = {}
        entit_dict['content'] = secureAnonymizedData
        onchain = OnChain(**entit_dict)
       
        transaction_id = register_onchain(onchain)['transaction_id']

        now = datetime.now()
        
        # dict to object schemas.TrackingCreate
        entit_dict = {}
        entit_dict['canonical_data'] = data.content
        entit_dict['anonymized_data'] = secureAnonymizedData       
        entit_dict['blockchain_id'] = DEFAULT_BLOCKCHAIN
        entit_dict['transaction_id'] = transaction_id                       
        entit_dict['salt'] =  data.salt
        entit_dict['hash_method'] = HashMethod(DEFAULT_HASHMETHOD).name   
        entit_dict['tracking_dt'] = now.strftime("%Y-%m-%dT%H:%M:%S.%f")
        entit_dict['locator'] = data.locator                                     
        trackingCreate = schemas.TrackingCreate(**entit_dict)

        db_tracking = crud.get_tracking_by_transaction_id(db, transaction_id)
        
        if db_tracking:
            raise HTTPException(status_code=400, detail="Transaction already registered")        
        return crud.create_tracking(db=db, tracking=trackingCreate)
        
    except Exception as e:
        raise MyCustomException(message = str(e))
            

@app.post('/unindexOnChain/', tags=["Operations"], responses=UnindexOnChain_Example)
def unindex_onchain(data: UnindexOnChain = Body(
    ...,
    example={
        "locator": "72815157071",
        "datetime": "2021-09-14T19:50:47.108814"
    }
    ), db: Session = Depends(get_db)) -> json:
    """
        Δ(L_E,t) \n
        \t Dissociation an previous indexation on-chain for L_E locator in 't' moment. When omiss 't', all registers for L_E are deleted. \n
        \t In pratice is the delete of the tuple 〈L_E |t|β|T_β |…〉 
    """
    try:
        print('unindexOnChain')
        print('data.locator: ' + data.locator)
        print('data.datetime: ' + data.datetime)
        # get list of transactions for deleting
        db_trackings = crud.get_trackings_for_unindex(db, data.locator, data.datetime)
        
        print('db_trackings: ' +  str(len(db_trackings)))
        
        if len(db_trackings) == 0:
            raise HTTPException(status_code=400, detail="Nothing to unindex.")        
        return crud.delete_trackings_for_unindex(db, data.locator, data.datetime) 
    except Exception as e:
        raise MyCustomException(message = str(e))

@app.get('/verifySecureImmutableRegister/', tags=["Operations"], responses=VerifySecureImmutableRegister_Example)
def verify_secure_immutable_register(data: verifySecureImmutable = Body(
    ...,
    example={
        "transaction_id": "0xa313998e80da563e74da68fdaeae1708f083276f838689d54c5679d1a88d284a",
        "content": "{cpf:72815157071, exam:HIV, datetime:2021-09-14T19:50:47.108814, result:POS, salt: e3719002-8c09-4c8f-8da3-9f5ce34c2d76}",
        "salt": "e3719002-8c09-4c8f-8da3-9f5ce34c2d76"
    }
    ), hashMethod: Optional[str] = 'SHA256') -> bool:
    """
        In pratice:\n
        \t 1. Get in blockchain β, the data A' registered with a transactionId (T_β): A'=R(T_β,β), 
            \t \t - call getOnChain(blockchain_id, transaction_id)
        \t 2. Calculate secure anonimization of D, with salt s, and hash h: A=γ(D,s,h), 
            \t \t - call secureAnonymize(content, salt)
        \t 3. Return True if A=A' or False otherwise.
    """
    try:
        # HTTPProvider:
        w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
    
        # get Transaction
        tx = w3.eth.get_transaction(data.transaction_id)
        anonymized_data_in_blockchain = tx.input[2:] 
        
        # calculate secure anonimization 
        entit_dict = {}
        entit_dict['content'] = data.content
        entit_dict['salt'] = data.salt

        secure = Secure(**entit_dict)
        return_secure_anonymize = secure_anonymize(secure)['content']

        if (return_secure_anonymize == anonymized_data_in_blockchain):
            result = {'result': True}
        else:
             result = {'result': False}    
             
        resultDump = json.dumps(result)
        resultJson = json.loads(resultDump)
    
        return resultJson

    except Exception as e:
        raise MyCustomException(message = str(e))


@app.post('/rectifyOffChain/', tags=["Transactions"], status_code=HTTPStatus.NO_CONTENT)
def rectify_offchain():
    """
    UPDATE in application SGBD \n 
    \t In pratice is a update in the application SGBD
    """
    # if entity.hasPI()
    #   rectify_onchain(entity)
    return Response(status_code=HTTPStatus.NO_CONTENT.value)

@app.post('/rectifyOnChain/', tags=["Transactions"], responses=RectifyOnChain_Example)
def rectify_onchain(data: rectifyOnChain = Body(
    ...,
    example={
        "content": "{cpf:72815157071, exam:HIV, datetime:2021-09-14T19:50:47.108814, result:POS}",
        "salt": "e3719002-8c09-4c8f-8da3-9f5ce34c2d76",
        "to_wallet": "0x1eca7eD6322B410219Ef953634442AF33aB05BA3",
        "from_wallet": "0x190e97032E45A1c3E1D7E2B1460b62098A5419ab",
        "locator": "72815157071",
        "datetime": "2021-09-14T19:50:47.108814"
    }
    ), db: Session = Depends(get_db), hashMethod: Optional[str] = 'SHA256') -> json:

    try:     
        # unindex_onchain all locator's registers
        entit_dict = {}
        entit_dict['locator'] = data.locator
        entit_dict['datetime'] = ""

        locators_registers = UnindexOnChain(**entit_dict)
        unindex_onchain(locators_registers, db)
        
        #index_secure_onchain for locator
        entit_dict = {}
        entit_dict['to_wallet'] = 'random'
        entit_dict['from_wallet'] = 'random'
        entit_dict['content'] = data.content
        entit_dict['locator'] = data.locator
        entit_dict['datetime'] = data.datetime
        entit_dict['salt'] =  data.salt
        
        index_locator = IndexOnChainS(**entit_dict)
        return index_secure_onchain(index_locator, db)     

    except Exception as e:
        raise MyCustomException(message = str(e))

@app.post('/removeOffChain/', tags=["Transactions"], status_code=HTTPStatus.NO_CONTENT)
def remove_offchain():
    """
    DELETE in application SGBD \n 
    \t In pratice is a delete in the application SGBD
    """
    # if entity.hasPI()
    #   remove_onchain(entity_locator)
    return Response(status_code=HTTPStatus.NO_CONTENT.value)

@app.post('/removeOnChain/', tags=["Transactions"], responses=RemoveOnchain_Example)
def remove_onchain(data: removeOnChain = Body(
    ...,
    example={
        "locator": "72815157071",
        "datetime": "2021-09-14T19:50:47.108814"
    }
    ), db: Session = Depends(get_db), hashMethod: Optional[str] = 'SHA256') -> json:
    try:
        # unindex_onchain all locator's registers
        entit_dict = {}
        entit_dict['locator'] = data.locator
        entit_dict['datetime'] = ""

        locators_registers = removeOnChain(**entit_dict)
        return unindex_onchain(locators_registers, db)

    except Exception as e:
        raise MyCustomException(message = str(e))

#@app.post("/tracking/", response_model=schemas.Tracking)
def create_tracking(tracking: schemas.TrackingCreate, db: Session = Depends(get_db)):
    db_tracking = crud.get_tracking_by_transaction_id(db, transaction_id=tracking.transaction_id)
    if db_tracking:
        raise HTTPException(status_code=400, detail="Transaction already registered")
    print("main: post tracking")
    return crud.create_tracking(db=db, tracking=tracking)

#@app.get("/tracking/", response_model=List[schemas.Tracking])
def read_trackings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    trackings = crud.get_trackings(db, skip=skip, limit=limit)
    return trackings

#@app.get("/tracking/{tracking_id}", response_model=schemas.Tracking)
def read_tracking(tracking_id: int, db: Session = Depends(get_db)):
    db_tracking = crud.get_tracking(db, tracking_id= tracking_id)
    if db_tracking is None:
        raise HTTPException(status_code=404, detail="Tracking not found")
    return db_tracking

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
