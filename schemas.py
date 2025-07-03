from pydantic import BaseModel, EmailStr
from typing import List

class Matricula(BaseModel):
    aluno_id: int
    curso_id: int

    class Config:
        from_attributes = True
        from_attributes = True

Matriculas = List[Matricula]

class Aluno(BaseModel):
    nome: str
    email: EmailStr
    telefone: str

    class Config:
        from_attributes = True

Alunos = List[Aluno]

class Curso(BaseModel):
    nome: str
    codigo: str
    descricao: str

    class Config:
        from_attributes = True

Cursos = List[Curso]