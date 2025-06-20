import PyPDF2
from fastapi import HTTPException, UploadFile
import requests
import json


def extrair_texto_do_PDF(file)-> str:
    try:
        leitor = PyPDF2.PdfReader(file.file)
        texto_total= ""

        for pagina in leitor.pages:
            texto = pagina.extract_text()
            if texto:
                texto_total += texto + '\n'

        if not texto_total.strip():
            raise ValueError("Não foi possivel extrair o texto do PDF.")
        
        print('Texto extraido')
        return texto_total[:4000]
    
    except Exception as e:
        raise RuntimeError(f"Erro ao ler o PDF: {e}")

def resumo_com_ollama(texto: str) -> str:
    try:
        print('Mandando texto para a puta q pariu')
        response = requests.post(
            'http://25.45.91.182:11434/api/generate',
            json={
                'model': 'qwen3:1.7b',
                'prompt': f'Resuma este arquivo. Seja direto e objetivo:\n\n{texto}'
            },
            stream=True,
            timeout=300
        )
        print(response.status_code)
        if response.status_code != 200:
            raise RuntimeError(f"Erro na API da IA: Status {response.status_code}")
        
        resposta_completa = ""

        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode('utf-8'))
                    resposta_completa +=  data.get('response', '')
                except json.JSONDecodeError:
                    continue
        
        return resposta_completa.strip()
    except Exception as e:
        raise RuntimeError(f"Erro ao conectar com a IA: {e}")


async def EnviaPDF(file: UploadFile):
    try:
        texto = extrair_texto_do_PDF(file)
        resumo = resumo_com_ollama(texto)
        return {"success":"sucesso",
                "summary": resumo}
    
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {e}")
    


