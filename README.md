# PrivacyChain

## Introduction
A framework for personal data persistence in DLT applications for compliance to RTBF and right to retification of the LGPD - Brazilian law for personal data protection.  

 ![PrivacyChain OpenAPI specification](img/privacychain-spec.png)

---  

## Motivation
This project is part of the Dissertation of the Master's at PPGTI-IFPB. The dissertation is  
the partial requirement to get the Master Title.  


In applications based on DLT (Distributed Ledger Technology), or blockchain as they are more commonly called, that process personal data, the characteristic of immutability intrinsic to this technology can be an obstacle for the data subject exercises the rights to be forgotten and to rectification of compliance with the LGPD – Brazilian Law for the Protection of Personal Data.  

An investigation was conducted. The investigation showed the suitability of using two techniques combined: (1) off-chain storage and (2) cryptographic commitment.  

A framework PrivacyChain was built with two techniques cited above. PrivacyChain features are made available through an API. Each resource of PrivacyChain is implemented as a API's endpoint.  

---

## Good for
Compliance with LGPD's rights: RTBF (Right To Be Forgotten) and Right to rectification.  

---

## Built with
- [FAST API](https://fastapi.tiangolo.com/)
- [Ganache](https://trufflesuite.com/ganache)
- [PostgreSQL](https://www.postgresql.org/download/)
- [Web3.py](https://web3py.readthedocs.io/en/stable/#)

---

## Instructions for installation
1. Download code from GitHub: [https://github.com/abmorte/privacychain](https://github.com/abmorte/privacychain)
2. Create a virtual environment with libraries from requirements.txt.
3. Download and install PostgreSQL database, vide [https://www.postgresql.org/download/](https://www.postgresql.org/download/).
4. Create the database (for control and tracking of personal data) with script.sql.
5. Install Ganache vide [https://trufflesuite.com/ganache/](https://trufflesuite.com/ganache/)
6. Execute command:
  ```
    uvicorn app.main:app --reload.
 ``` 
6. Access localhost:8000/docs for swagger UI interface, or localhost:8000/redoc for redoc interface.
7. Demonstration:
 ![Demonstration](video/load-app.gif)
---

## Usage

-  Data preparation
1. List - according to the application's business context - the personal data you want to store in the blockchain.

2. Select data that atomically identifies the owner of the personal data. This will be the *locator* key, to be used on the logging endpoints in the blockchain.

- Adequate application to trigger PrivacyChain services
It´s necessary to adequate the application that will use PrivacyChain´s services. Below is the howto for the major´s endpoint´s.
---

### Register on blockchain
#### Use endpoint /indexOnChain/ for simple anonymization or /indexSecureOnChain for secure anonymization.

---
```python
# Pseudocode for insert secure on-chain

def insert_health_record(locator: str) -> bool:
  """
  INSERT in application \n 
  """
  try:
    # locator = CPF do paciente
    locator = 72815157071

    # inserção de registro médico na base de dados da aplicação
    insert_health_record(locator)

    # chamada ao endpoint do PrivacyChain para registro seguro na blockchain.
    # Obs. payload inclui a chave locator
    indexSecureOnChain(payload)
  except:
    print("Ocorreu um erro")
  else: 
    print("Registro efetuado com sucesso.")

  return True
```
---
```python
# Sample client code for consumption of indexSecureOnChain endpoint

import requests

url = "http://localhost:8000/indexSecureOnChain/"

payload = {
    "to_wallet": "0x1eca7eD6322B410219Ef953634442AF33aB05BA3",
    "from_wallet": "0x190e97032E45A1c3E1D7E2B1460b62098A5419ab",
    "content": "{cpf:72815157071, exam:HIV, datetime:2021-09-14T19:50:47.108814, result:POS}",
    "locator": "72815157071",
    "datetime": "2021-09-25T10:58:00.000000",
    "salt": "e3719002-8c09-4c8f-8da3-9f5ce34c2d76"
}
headers = {"Content-Type": "application/json"}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)
```

#### Test endpoint /indexSecureOnChain/ ([Insomnia](https://insomnia.rest/))
 ![](video/indexSecureOnChain.gif)

---

### Right To Be Forgotten
#### Use endpoint /removeOnChain/
---
```python
# Pseudocode for Remove on-chain

def delete_health_record(locator: str) -> bool:
  """
  DELETE in application \n 
  """
  try:
    # locator = CPF do paciente
    locator = 72815157071

    # exclusão de registro médico na base de dados da aplicação
    delete_health_record(locator)

    # chamada ao endpoint do PrivacyChain para exclusão de registro na blockchain.
    # Obs. payload inclui a chave locator
    removeOnChain(payload)
  except:
    print("Ocorreu um erro")
  else: 
    print("Registro excluído com sucesso.")

  return True
```
---
---
```python
# Sample client code for consumption of removeOnchain endpoint

import requests

url = "http://localhost:8000/removeOnChain/"

payload = {
    "locator": "72815157071",
    "datetime": "2021-09-14T19:50:47.108814"
}
headers = {"Content-Type": "application/json"}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)
```

#### Test endpoint /removeOnChain ([Insomnia](https://insomnia.rest/)): ![](video/removeOnChain.gif)
---

### Right to Rectification
#### Use endpoint /rectifyOnChain/
---
```python
# Pseudocode for Rectify on-chain

def update_health_record(locator: str) -> bool:
  """
  UPDATE in application \n 
  """
  try:
    # locator = CPF do paciente
    locator = 72815157071

    # retificação de registro médico na base de dados da aplicação
    update_health_record(locator)

    # chamada ao endpoint do PrivacyChain para retificar registro na blockchain.
    # Obs. payload inclui a chave locator
    rectifyOnChain(payload)
  except:
    print("Ocorreu um erro")
  else: 
    print("Registro retificado com sucesso.")

  return True
```

---
```python

# Sample client code for consumption of rectifyOnchain endpoint

import requests

url = "http://localhost:8000/rectifyOnChain/"

payload = {
    "content": "{cpf:72815157071, exam:HIV, datetime:2021-09-14T19:50:47.108814, result:POS}",
    "salt": "e3719002-8c09-4c8f-8da3-9f5ce34c2d76",
    "to_wallet": "0x1eca7eD6322B410219Ef953634442AF33aB05BA3",
    "from_wallet": "0x190e97032E45A1c3E1D7E2B1460b62098A5419ab",
    "locator": "72815157071",
    "datetime": ""
}
headers = {"Content-Type": "application/json"}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)
```

#### Test endpoint /rectifyOnChain ([Insomnia](https://insomnia.rest/))
![](video/rectifyOnChain.gif)
---


## License

MIT