from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.projects import Project
from .schemas import ProjectCreate
from datetime import datetime
from uuid import UUID

async def fetch_all_projects(db: AsyncSession):

    res = await db.execute(
        select(Project).where(Project.is_published==True)
    )

    projects = res.scalars().all()

    return projects

async def add_project_to_db(project_data: ProjectCreate, db: AsyncSession, current_user):

    new_project = Project(
        **project_data.model_dump(),
        created_by=current_user.id
    )

    if new_project.is_published:
        new_project.published_at = datetime.utcnow()

    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)

    return new_project
    
async def fetch_project_by_id(project_id: UUID, db: AsyncSession):

    result = await db.execute(
        select(Project).where(Project.id==(project_id))
        )
    project = result.scalar_one_or_none()

    return project