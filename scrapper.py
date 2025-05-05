import json
import os

def extract(file_json, file_extract):
    with open(file_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    folder_name = os.path.splitext(file_json)[0] 
    folder_name = folder_name[3:]
    extracted_text = {}
    index = 0

    for event in data.get("events", []):
        if event is None:
            continue
        for page in event.get("pages", []):
            for command in page.get("list", []):
                if command.get("code") == 401:
                    texto = command["parameters"][0]
                    if texto.strip():
                        extracted_text[str(index)] = texto
                        index += 1

    os.makedirs(folder_name, exist_ok=True)
    file_extract = os.path.join(folder_name, os.path.basename(file_extract))

    with open(file_extract, "w", encoding="utf-8") as f:
        json.dump(extracted_text, f, ensure_ascii=False, indent=2)

    print(f"{index} falas exportadas para '{file_extract}'.")


def insert(file_json_original, file_translated, file_extract):
    with open(file_json_original, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(file_translated, "r", encoding="utf-8") as f:
        translated_text = json.load(f)

    index = 0
    changed = 0

    for event in data.get("events", []):
        if event is None:
            continue
        for page in event.get("pages", []):
            for command in page.get("list", []):
                if command.get("code") == 401:
                    new_text = translated_text.get(str(index), "").strip()
                    if new_text:
                        command["parameters"][0] = new_text
                        changed += 1
                    index += 1
    with open(file_extract, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"{changed} falas traduzidas inseridas no arquivo '{file_extract}'.")

def main():
    mode = input("Digite '1' para exportar ou '2' para reinserir o texto: ").strip().lower()

    if mode == "1":
        map_files = [f for f in os.listdir() if f.startswith("Map") and f.endswith(".json")]
        for map_file in map_files:
            output = 'dialogos_' + map_file
            extract(map_file, output)

    elif mode == "2":
        map_file = input("Arquivo de map original (.json) [ex: Map001.json]: ").strip()
        traduzido = 'dialogos_' + map_file
        output = 'traduzido_' + map_file
        insert(map_file, traduzido, output)

    else:
        print("Modo inválido. Use '1' ou '2'.")

if __name__ == "__main__":
    main()
