
FROM python:3.12


WORKDIR /app


RUN pip install poetry

 
COPY ./pyproject.toml ./


RUN poetry config virtualenvs.create false


RUN poetry install 
 
COPY . .

CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8999"]
ENV PYTHONPATH "${PYTHONPATH}:/app/"
