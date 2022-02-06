from enum import Enum, unique

@unique
class Blockchain(str, Enum):
    HYPERLEDGER = 1
    ETHEREUM = 2
    BITCOIN = 3

@unique
class TypeClassification(str, Enum):
    EXPANDED = 1
    SUMMARIZED = 2

@unique
class TypeAnonimization(str, Enum):
    SIMPLE = 1
    SECURE = 2

@unique
class HashMethod(str, Enum):
    MD5 = 1
    SHA1 = 2
    SHA256 = 3
    SHA512 = 4
    
    