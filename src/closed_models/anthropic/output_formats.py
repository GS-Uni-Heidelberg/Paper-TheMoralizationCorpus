output_json_explain = {
  "name": "MoralisierungOutput",
  "input_schema": {
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
                "text": { "type": "string" },
                "moral_foundations_theory_kategorien": {
                  "type": "array",
                  "items": {
                    "type": "string",
                    "enum": [
                      "Fürsorge", "Schaden",
                      "Fairness", "Betrug",
                      "Loyalität", "Verrat",
                      "Autorität", "Untergrabung von Autorität",
                      "Reinheit", "Verfall",
                      "Freiheit", "Unterdrückung"
                    ]
                  }
                }
              },
              "required": ["text", "moral_foundations_theory_kategorien"]
            }
          },
          "forderung": { "type": "string" },
          "begruendung": { "type": "string" },
          "enthaelt_moralisierung": { "type": "boolean" }
        },
        "required": ["moral_werte", "forderung", "begruendung", "enthaelt_moralisierung"]
      },
      "protagonisten": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "text": { "type": "string" },
            "kategorie": {
              "type": "string",
              "enum": ["Individuum","Menschen","Institution","Soziale Gruppe","OTHER"]
            },
            "rollen": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "Forderer:in","Adressat:in",
                  "Benefizient:in","Malefizient:in",
                  "Bezug unklar","NONE"
                ]
              }
            }
          },
          "required": ["text", "kategorie", "rollen"]
        }
      }
    },
    "required": ["moralisierung", "protagonisten"]
  }
}

output_json_no_explain = {
  "name": "MoralisierungOutput",
  "input_schema": {
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
                "text": { "type": "string" },
                "moral_foundations_theory_kategorien": {
                  "type": "array",
                  "items": {
                    "type": "string",
                    "enum": [
                      "Fürsorge", "Schaden",
                      "Fairness", "Betrug",
                      "Loyalität", "Verrat",
                      "Autorität", "Untergrabung von Autorität",
                      "Reinheit", "Verfall",
                      "Freiheit", "Unterdrückung"
                    ]
                  }
                }
              },
              "required": ["text", "moral_foundations_theory_kategorien"]
            }
          },
          "forderung": { "type": "string" },
          "enthaelt_moralisierung": { "type": "boolean" }
        },
        "required": ["moral_werte", "forderung", "enthaelt_moralisierung"]
      },
      "protagonisten": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "text": { "type": "string" },
            "kategorie": {
              "type": "string",
              "enum": ["Individuum","Menschen","Institution","Soziale Gruppe","OTHER"]
            },
            "rollen": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "Forderer:in","Adressat:in",
                  "Benefizient:in","Malefizient:in",
                  "Bezug unklar","NONE"
                ]
              }
            }
          },
          "required": ["text", "kategorie", "rollen"],
        }
      }
    },
    "required": ["moralisierung", "protagonisten"]
  }
}
