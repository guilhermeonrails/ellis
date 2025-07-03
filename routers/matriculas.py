from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Union
from schemas import Matricula
from models import Matricula as ModelMatricula, Aluno as ModelAluno, Curso as ModelCurso # Importe os modelos
from database import get_db

matriculas_router = APIRouter()

@matriculas_router.post("/matriculas", response_model=Matricula, status_code=status.HTTP_201_CREATED)
def create_matricula(matricula: Matricula, db: Session = Depends(get_db)):
    
    db_aluno = db.query(ModelAluno).filter(ModelAluno.id == matricula.aluno_id).first()
    db_curso = db.query(ModelCurso).filter(ModelCurso.id == matricula.curso_id).first()

    if db_aluno is None or db_curso is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno ou Curso não encontrado")

    db_matricula = ModelMatricula(**matricula.dict())
    db.add(db_matricula)
    db.commit()
    db.refresh(db_matricula)
    return Matricula.from_orm(db_matricula)



@matriculas_router.get("/matriculas/aluno/{nome_aluno}", response_model=Dict[str, Union[str, List[str]]])
def read_matriculas_por_nome_aluno(nome_aluno: str, db: Session = Depends(get_db)):
    db_aluno = db.query(ModelAluno).filter(ModelAluno.nome.ilike(f"%{nome_aluno}%")).first()

    if not db_aluno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")

    cursos_matriculados = []
    for matricula in db_aluno.matriculas:
        curso = matricula.curso  
        if curso:  
            cursos_matriculados.append(curso.nome)

    if not cursos_matriculados:
        raise HTTPException(status_code=404, detail=f"O aluno '{nome_aluno}' não possui matrículas cadastradas.")

    return {"aluno": db_aluno.nome, "cursos": cursos_matriculados}

@matriculas_router.get("/matriculas/curso/{codigo_curso}", response_model=Dict[str, Union[str, List[str]]])
def read_alunos_matriculados_por_codigo_curso(codigo_curso: str, db: Session = Depends(get_db)):
    """Retorna o nome do curso e uma lista com os nomes dos alunos matriculados."""
    db_curso = db.query(ModelCurso).filter(ModelCurso.codigo == codigo_curso).first()

    if not db_curso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")

    alunos_matriculados = []
    for matricula in db_curso.matriculas:  # Itera pelas matrículas do curso
        aluno = matricula.aluno  # Acessa o aluno diretamente pelo relacionamento
        if aluno:  # Verifica se o aluno existe (pode ter sido excluído)
            alunos_matriculados.append(aluno.nome)

    if not alunos_matriculados:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Nenhum aluno matriculado no curso '{db_curso.nome}'.")

    return {"curso": db_curso.nome, "alunos": alunos_matriculados}