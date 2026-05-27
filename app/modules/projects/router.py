from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .services import fetch_all_projects, add_project_to_db, fetch_project_by_id
from app.core.dependencies import get_current_user
from app.core.database import get_db
from .schemas import ProjectCreate, ProjectRead, ProjectUpdate
from typing import List
from uuid import UUID


router = APIRouter(prefix='/projects')

@router.get('/', response_model = List[ProjectRead])
async def get_all_projects(db: AsyncSession = Depends(get_db)):
    return await fetch_all_projects(db)

@router.get('/{id}', response_model = ProjectRead)
async def get_project_by_id(project_id: UUID, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):

    return await fetch_project_by_id(project_id, db)


@router.post('/', response_model = ProjectRead)
async def create_project(project_data: ProjectCreate, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    
    project = await add_project_to_db(project_data, db, current_user)

    return project

@router.patch('/{projects_id}', response_model=ProjectRead)
async def update_project(project_id: UUID, project_update: ProjectUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):

    db_project = await fetch_project_by_id(project_id, db)

    if not db_project:
        raise HTTPException(status_code=404, detail='Project not Found!')
    
    if db_project.created_by != current_user.id:
        raise HTTPException(status_code=403, detail='Not Authorized!')
    
    update_data = project_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_project, key, value)

    await db.commit()
    await db.refresh(db_project)

    return db_project