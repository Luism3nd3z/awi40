import json

texto ='''{
  "error": {
    "code": 400,
    "message": "CONTRASEÑA INVALIDA",
    "errors": [
      {
        "message": "CONTRASEÑA INVALIDA",
        "domain": "global",
        "reason": "invalid"
      }
    ]
  }
}'''

formato = json.loads(texto)
error = formato['error']
print(error['message'])