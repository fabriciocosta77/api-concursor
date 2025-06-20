from fastapi import APIRouter, UploadFile, File, HTTPException
from services.PDFServicos import EnviaPDF

roteador = APIRouter()

@roteador.post("/resumo")
async def RecebePDF(file: UploadFile = File(...)):
    print('Bateu aqui mano')
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="O arquivo deve ser um PDF legível!")

    return await EnviaPDF(file)