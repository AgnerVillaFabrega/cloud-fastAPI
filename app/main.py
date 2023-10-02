from fastapi import FastAPI, File, Response, UploadFile, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from botocore.exceptions import NoCredentialsError
from uuid import uuid4
import boto3

app = FastAPI()

aws_access_key_id = 'AKIAWWSPTKUX*'
aws_secret_access_key = 'zoNgf/L*yAzArnOh'
aws_bucket_name = 'unicesar-a202302'

s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_extension = file.filename.split(".")[-1]
        file_name = f'{uuid4()}.{file_extension}'

        s3.upload_fileobj(file.file, aws_bucket_name, file_name)
        return {'message': 'Archivo subido exitosamente', 'file_name': file_name}
        
    except NoCredentialsError:
        raise HTTPException(
            status_code=500,
            detail='No se encontraron credenciales de AWS. Verifica tu configuración de credenciales.'
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'Error al subir el archivo: {str(e)}'
        )

@app.get("/list_files")
async def list_files():
    try:
        response = s3.list_objects_v2(Bucket=aws_bucket_name)
        files = [obj['Key'] for obj in response.get('Contents', [])]
        return {"files": files}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'Error al listar archivos: {str(e)}'
        )

@app.get('/download/{file_name}')
async def download(file_name: str):
    try:
        
        response = s3.get_object(Bucket=aws_bucket_name, Key=file_name)
        file_data = response['Body'].read()

        return Response(
            content=file_data,
            headers={
                'Content-Disposition': f'attachment; filename={file_name}',
                'Content-Type': 'application/octet-stream',
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'Error al descargar el archivo: {str(e)}'
        )
