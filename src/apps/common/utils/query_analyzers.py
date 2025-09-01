import logging

from sqlalchemy import Select, func, select, text
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def explain_analyze(query: Select, session: AsyncSession) -> None:
    """Логирует в stdout EXPLAIN ANALYZE для запроса"""
    if not isinstance(query, Select):
        raise TypeError("Only Select queries are supported")

    compiled = query.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True})
    sql = str(compiled)

    result = await session.scalars(text(f"EXPLAIN ANALYZE {sql}"))
    plan = "\n".join(list(result))

    msg_parts = [
        "",
        f"{'=' * 80}",
        "SQL QUERY:",
        f"{sql}\n",
        "EXPLAIN ANALYZE:",
        f"{plan}",
        f"{'=' * 80}",
        "",
    ]
    logger.info("\n".join(msg_parts))


async def get_selectivity(query: Select, session: AsyncSession) -> None:
    """Логирует в stdout значение селективности запроса.
    Имеет смысл использовать на простых запросах с фильтрацией, без Subquery/Join
    """
    if not isinstance(query, Select):
        raise TypeError("Only Select queries are supported")

    filtered_count_query = select(func.count()).select_from(query.subquery())
    filtered_count = await session.scalar(filtered_count_query)

    all_query = select(func.count()).select_from(query.get_final_froms()[0])
    all_count = await session.scalar(all_query)

    selectivity = filtered_count / all_count if all_count else 0
    selectivity_result = (
        "HIGH ✅" if selectivity < 0.05 else "MEDIUM ⚠️" if selectivity < 0.3 else "LOW ⛔️"
    )

    msg_parts = [
        "",
        f"{'=' * 80}",
        "SQL QUERY:",
        f"{str(query.compile(dialect=postgresql.dialect(), compile_kwargs={'literal_binds': True}))}\n",
        f"ALL ROWS: {all_count}",
        f"ROWS SELECTED BY QUERY: {filtered_count}",
        f"SELECTIVITY: {round(selectivity, 3)} - {selectivity_result}",
        f"{'=' * 80}",
        "",
    ]
    logger.info("\n".join(msg_parts))
