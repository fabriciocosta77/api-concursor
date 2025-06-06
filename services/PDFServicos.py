import PyPDF2
from fastapi import HTTPException
from openai import OpenAI
from ..config.APIConfig import OPENAI_API_KEY

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

        client = OpenAI(api_key=OPENAI_API_KEY)

        response = client.responses.create(
            model="gpt-4o",
            instructions=(
                "Você é um aplicativo que resume PDFs de editais enviados por clientes. "
                "Seu objetivo é extrair todas as informações do texto e retornar apenas o resumo da forma mais eficaz e sem omitir informações."
            ),
            input="Resuma o seguinte edital, extraindo todas as informações úteis e pertinentes de maneira compreensiva e completa:\n" + texto_total
        )

        return {"response": response.output_text}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
