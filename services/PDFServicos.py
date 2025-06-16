import PyPDF2
from fastapi import HTTPException
import requests
import json


async def EnviaPDF(file):
    try:
        leitor = PyPDF2.PdfReader(file.file)
        texto_total = ""

        for pagina in leitor.pages:
            texto = pagina.extract_text()
            if texto:
                texto_total += texto + "\n"

        if not texto_total.strip():
            raise HTTPException(status_code=400, detail="Não foi possível ler o PDF!")

        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model' : 'qwen3:1.7b',
                'prompt' : f'Resuma este arquivo. Seja direto e objetivo: {texto_total}' 
            },
            stream=True
        )

        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        return data.get('response', '') 
                    except json.JSONDecodeError as e:
                        return f'\nErro ao decodificar JSON: {e}'
        else:
            return response.status_code
        

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
