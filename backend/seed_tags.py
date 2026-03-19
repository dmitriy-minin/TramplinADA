"""
Скрипт для наполнения БД начальными данными (теги технологий).
Запуск: python seed_tags.py
"""
import asyncio
import sys
sys.path.insert(0, '.')

from app.db.database import AsyncSessionLocal, create_db_tables
from app.models.opportunity import Tag

DEFAULT_TAGS = [
    # Tech
    ("Python", "tech"), ("JavaScript", "tech"), ("TypeScript", "tech"),
    ("React", "tech"), ("Vue.js", "tech"), ("Angular", "tech"),
    ("Node.js", "tech"), ("FastAPI", "tech"), ("Django", "tech"),
    ("PostgreSQL", "tech"), ("MongoDB", "tech"), ("Redis", "tech"),
    ("Docker", "tech"), ("Kubernetes", "tech"), ("Git", "tech"),
    ("AWS", "tech"), ("GCP", "tech"), ("Linux", "tech"),
    ("Java", "tech"), ("Go", "tech"), ("Rust", "tech"),
    ("C++", "tech"), ("C#", "tech"), ("Swift", "tech"),
    ("Kotlin", "tech"), ("Flutter", "tech"), ("React Native", "tech"),
    ("Next.js", "tech"), ("GraphQL", "tech"), ("REST API", "tech"),
    ("Machine Learning", "tech"), ("Data Science", "tech"),
    ("TensorFlow", "tech"), ("PyTorch", "tech"),
    ("Figma", "tech"), ("UI/UX", "tech"),
    # Level
    ("Junior", "level"), ("Middle", "level"), ("Senior", "level"),
    # Format
    ("Офис", "format"), ("Удалёнка", "format"), ("Гибрид", "format"),
]


async def seed():
    await create_db_tables()
    async with AsyncSessionLocal() as session:
        from sqlalchemy import select
        existing = await session.execute(select(Tag))
        existing_names = {t.name for t in existing.scalars().all()}

        added = 0
        for name, category in DEFAULT_TAGS:
            if name not in existing_names:
                session.add(Tag(name=name, category=category))
                added += 1

        await session.commit()
        print(f"✅ Добавлено тегов: {added}")


if __name__ == "__main__":
    asyncio.run(seed())
