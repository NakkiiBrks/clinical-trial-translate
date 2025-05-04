import json

def extrair_dialogos(arquivo_json, arquivo_saida="dialogos_extraidos.json"):
    with open(arquivo_json, "r", encoding="utf-8") as f:
        dados = json.load(f)

    dialogos = []
    for evento in dados.get("events", []):
        if evento is None:
            continue
        for pagina in evento.get("pages", []):
            for comando in pagina.get("list", []):
                if comando.get("code") == 401:
                    texto = comando["parameters"][0]
                    if texto.strip():
                        dialogos.append(texto)

    with open(arquivo_saida, "w", encoding="utf-8") as f:
        json.dump(dialogos, f, ensure_ascii=False, indent=2)

    print(f"{len(dialogos)} dialogos extraidos para '{arquivo_saida}'.")

extrair_dialogos("Map002.json", "dialogos_Map002.json")
