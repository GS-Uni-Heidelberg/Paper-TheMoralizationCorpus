from pydantic import BaseModel
from typing import List

class Moralwert(BaseModel):
    text: str
    moral_foundations_theory_kategorien: List[str]

class Protagonist(BaseModel):
    text: str
    kategorie: str 
    rollen: List[str] 

class Moralisierung(BaseModel):
    moral_werte: List[Moralwert]
    forderung: str
    begruendung: str
    enthaelt_moralisierung: bool

class MoralisierungOutput(BaseModel):
    moralisierung: Moralisierung
    protagonisten: List[Protagonist]


output_json_explain = {
    "type": "json_schema",
    "json_schema": {
        "name": "MoralisierungOutput",
        "schema": {
            "type": "object",
            "properties": {
                "moralisierung": {
                    "type": "object",
                    "properties": {
                        "moral_werte": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "text": {"type": "string"},
                                        "moral_foundations_theory_kategorien": {"type": "array", "items": {"type": "string", "enum": [
                                            "Fürsorge", "Schaden",
                                            "Fairness", "Betrug",
                                            "Loyalität", "Verrat",
                                            "Autorität", "Untergrabung von Autorität",
                                            "Reinheit", "Verfall",
                                            "Freiheit", "Unterdrückung"
                                        ]}}
                                },
                                "required": ["text", "moral_foundations_theory_kategorien"],
                                "additionalProperties": False
                            }
                        },
                        "forderung": {"type": "string"},
                        "begruendung": {"type": "string"},
                        "enthaelt_moralisierung": {"type": "boolean"}
                    },
                    "required": ["moral_werte", "forderung", "begruendung", "enthaelt_moralisierung"],
                    "additionalProperties": False,
                },
                "protagonisten": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "kategorie": {"type": "string", "enum": [
                                "Individuum",
                                "Menschen",
                                "Institution",
                                "Soziale Gruppe",
                                "OTHER"
                            ]},
                            "rollen": {"type": "array", "items": {"type": "string", "enum": [
                                "Forderer:in",
                                "Adressat:in",
                                "Benefizient:in",
                                "Malefizient:in",
                                "Bezug unklar",
                                "NONE"
                            ]}},
                        },
                        "required": ["text", "kategorie", "rollen"],
                        "additionalProperties": False,
                    },
                },
            },
            "required": ["moralisierung", "protagonisten"],
            "additionalProperties": False,
        },
        "strict": True,
    }}


class MoralisierungOhneBegruendung(BaseModel):
    moral_werte: List[Moralwert]
    forderung: str
    enthaelt_moralisierung: bool

class MoralisierungOutputOhneBegruendung(BaseModel):
    moralisierung: MoralisierungOhneBegruendung
    protagonisten: List[Protagonist]

output_json_no_explain = {
    "type": "json_schema",
    "json_schema": {
        "name": "MoralisierungOutput",
        "schema": {
            "type": "object",
            "properties": {
                "moralisierung": {
                    "type": "object",
                    "properties": {
                        "moral_werte": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "text": {"type": "string"},
                                        "moral_foundations_theory_kategorien": {"type": "array", "items": {"type": "string", "enum": [
                                            "Fürsorge", "Schaden",
                                            "Fairness", "Betrug",
                                            "Loyalität", "Verrat",
                                            "Autorität", "Untergrabung von Autorität",
                                            "Reinheit", "Verfall",
                                            "Freiheit", "Unterdrückung"
                                        ]}}
                                },
                                "required": ["text", "moral_foundations_theory_kategorien"],
                                "additionalProperties": False
                            }
                        },
                        "forderung": {"type": "string"},
                        "enthaelt_moralisierung": {"type": "boolean"}
                    },
                    "required": ["moral_werte", "forderung", "enthaelt_moralisierung"],
                    "additionalProperties": False,
                },
                "protagonisten": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "kategorie": {"type": "string", "enum": [
                                "Individuum",
                                "Menschen",
                                "Institution",
                                "Soziale Gruppe",
                                "OTHER"
                            ]},
                            "rollen": {"type": "array", "items": {"type": "string", "enum": [
                                "Forderer:in",
                                "Adressat:in",
                                "Benefizient:in",
                                "Malefizient:in",
                                "Bezug unklar",
                                "NONE"
                            ]}},
                        },
                        "required": ["text", "kategorie", "rollen"],
                        "additionalProperties": False,
                    },
                },
            },
            "required": ["moralisierung", "protagonisten"],
            "additionalProperties": False,
        },
        "strict": True,
    }
}