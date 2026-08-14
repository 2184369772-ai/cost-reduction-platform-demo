import json
import sqlite3
import uuid
from datetime import date
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "demo.db"

FACTORIES = [
    {"name": "Factory Alpha", "region": "East Campus", "code": "ALPHA"},
    {"name": "Factory Beta", "region": "North Campus", "code": "BETA"},
    {"name": "Factory Gamma", "region": "South Campus", "code": "GAMMA"},
]

SEED_PROJECTS = [
    {
        "project_code": "ALPHA-2026-001",
        "title": "Compressed Air Leak Sweep",
        "factory_code": "ALPHA",
        "category": "Energy",
        "status": "Active",
        "owner": "Iris Cole",
        "estimated_savings": 124000,
        "currency": "CNY",
        "start_date": "2026-01-15",
        "target_date": "2026-10-30",
        "description": "Synthetic initiative to reduce utility loss by repairing compressed air leaks in packaging and assembly areas.",
    },
    {
        "project_code": "ALPHA-2026-002",
        "title": "Packaging Film Width Optimization",
        "factory_code": "ALPHA",
        "category": "Material",
        "status": "Planned",
        "owner": "Noah Grant",
        "estimated_savings": 86000,
        "currency": "CNY",
        "start_date": "2026-03-01",
        "target_date": "2026-11-15",
        "description": "Synthetic film consumption reduction trial through width standardization and scrap controls.",
    },
    {
        "project_code": "BETA-2026-001",
        "title": "Forklift Route Redesign",
        "factory_code": "BETA",
        "category": "Logistics",
        "status": "Completed",
        "owner": "Mia Turner",
        "estimated_savings": 57000,
        "currency": "CNY",
        "start_date": "2026-02-10",
        "target_date": "2026-06-30",
        "description": "Synthetic logistics project that shortens internal travel distance and reduces handling wait time.",
    },
    {
        "project_code": "BETA-2026-002",
        "title": "Cooling Water Setpoint Review",
        "factory_code": "BETA",
        "category": "Energy",
        "status": "Active",
        "owner": "Luca Reed",
        "estimated_savings": 142000,
        "currency": "CNY",
        "start_date": "2026-04-05",
        "target_date": "2026-12-20",
        "description": "Synthetic utility optimization review with operator approval checkpoints built into execution.",
    },
    {
        "project_code": "GAMMA-2026-001",
        "title": "Returnable Pallet Expansion",
        "factory_code": "GAMMA",
        "category": "Material",
        "status": "Active",
        "owner": "Ava Brooks",
        "estimated_savings": 93000,
        "currency": "CNY",
        "start_date": "2026-05-12",
        "target_date": "2026-09-30",
        "description": "Synthetic packaging reuse initiative expanding returnable pallets between warehouse and line-side staging.",
    },
    {
        "project_code": "GAMMA-2026-002",
        "title": "Changeover Checklist Simplification",
        "factory_code": "GAMMA",
        "category": "Productivity",
        "status": "On Hold",
        "owner": "Ethan Vale",
        "estimated_savings": 41000,
        "currency": "CNY",
        "start_date": "2026-06-08",
        "target_date": "2026-12-05",
        "description": "Synthetic procedural simplification project focused on shorter line changeover preparation.",
    },
]


def get_connection() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS factories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                region TEXT NOT NULL,
                code TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_code TEXT NOT NULL UNIQUE,
                title TEXT NOT NULL,
                title_normalized TEXT NOT NULL,
                factory_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                status TEXT NOT NULL,
                owner TEXT NOT NULL,
                estimated_savings REAL NOT NULL,
                currency TEXT NOT NULL,
                start_date TEXT NOT NULL,
                target_date TEXT NOT NULL,
                description TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(factory_id) REFERENCES factories(id)
            );

            CREATE INDEX IF NOT EXISTS idx_projects_factory_id ON projects(factory_id);
            CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status);
            CREATE INDEX IF NOT EXISTS idx_projects_category ON projects(category);
            CREATE INDEX IF NOT EXISTS idx_projects_title_norm ON projects(title_normalized);

            CREATE TABLE IF NOT EXISTS import_batches (
                id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                confirmed_at TEXT
            );
            """
        )
        seed_factories(conn)
        seed_projects(conn)


def normalize_title(value: str) -> str:
    return " ".join(value.lower().split())


def seed_factories(conn: sqlite3.Connection) -> None:
    existing = conn.execute("SELECT COUNT(*) AS count FROM factories").fetchone()["count"]
    if existing:
        return
    conn.executemany(
        "INSERT INTO factories(name, region, code) VALUES(:name, :region, :code)",
        FACTORIES,
    )


def seed_projects(conn: sqlite3.Connection) -> None:
    existing = conn.execute("SELECT COUNT(*) AS count FROM projects").fetchone()["count"]
    if existing:
        return
    factories = {
        row["code"]: row["id"]
        for row in conn.execute("SELECT id, code FROM factories").fetchall()
    }
    rows = []
    for project in SEED_PROJECTS:
        rows.append(
            {
                **project,
                "factory_id": factories[project["factory_code"]],
                "title_normalized": normalize_title(project["title"]),
            }
        )
    conn.executemany(
        """
        INSERT INTO projects(
            project_code, title, title_normalized, factory_id, category, status,
            owner, estimated_savings, currency, start_date, target_date, description
        ) VALUES(
            :project_code, :title, :title_normalized, :factory_id, :category, :status,
            :owner, :estimated_savings, :currency, :start_date, :target_date, :description
        )
        """,
        rows,
    )


def list_factories() -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute("SELECT * FROM factories ORDER BY name").fetchall()


def factory_lookup() -> dict[int, dict[str, Any]]:
    return {row["id"]: dict(row) for row in list_factories()}


def factory_lookup_by_name() -> dict[str, sqlite3.Row]:
    return {row["name"].lower(): row for row in list_factories()}


def category_options() -> list[str]:
    return ["Energy", "Material", "Logistics", "Productivity", "Quality"]


def status_options() -> list[str]:
    return ["Planned", "Active", "On Hold", "Completed"]


def project_filters() -> dict[str, list[str]]:
    return {"categories": category_options(), "statuses": status_options()}


def dashboard_summary(factory_id: int | None = None) -> dict[str, Any]:
    where = ""
    params: list[Any] = []
    if factory_id:
        where = "WHERE p.factory_id = ?"
        params.append(factory_id)
    with get_connection() as conn:
        totals = conn.execute(
            f"""
            SELECT COUNT(*) AS total_projects,
                   COALESCE(SUM(p.estimated_savings), 0) AS total_savings
            FROM projects p
            {where}
            """,
            params,
        ).fetchone()
        statuses = conn.execute(
            f"""
            SELECT p.status, COUNT(*) AS count
            FROM projects p
            {where}
            GROUP BY p.status
            ORDER BY count DESC, p.status
            """,
            params,
        ).fetchall()
        by_factory = conn.execute(
            """
            SELECT f.name, COUNT(p.id) AS count, COALESCE(SUM(p.estimated_savings), 0) AS total_savings
            FROM factories f
            LEFT JOIN projects p ON p.factory_id = f.id
            GROUP BY f.id
            ORDER BY f.name
            """
        ).fetchall()
        recent = conn.execute(
            f"""
            SELECT p.*, f.name AS factory_name
            FROM projects p
            JOIN factories f ON f.id = p.factory_id
            {where}
            ORDER BY p.updated_at DESC, p.id DESC
            LIMIT 5
            """,
            params,
        ).fetchall()
    return {
        "total_projects": totals["total_projects"],
        "total_savings": totals["total_savings"],
        "status_breakdown": statuses,
        "factory_breakdown": by_factory,
        "recent_projects": recent,
    }


def list_projects(filters: dict[str, str]) -> list[sqlite3.Row]:
    conditions = []
    params: list[Any] = []
    if filters.get("factory_id"):
        conditions.append("p.factory_id = ?")
        params.append(int(filters["factory_id"]))
    if filters.get("status"):
        conditions.append("p.status = ?")
        params.append(filters["status"])
    if filters.get("category"):
        conditions.append("p.category = ?")
        params.append(filters["category"])
    if filters.get("q"):
        conditions.append("(p.project_code LIKE ? OR p.title LIKE ? OR p.owner LIKE ? OR p.description LIKE ?)")
        query = f"%{filters['q'].strip()}%"
        params.extend([query, query, query, query])
    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    with get_connection() as conn:
        return conn.execute(
            f"""
            SELECT p.*, f.name AS factory_name, f.code AS factory_code
            FROM projects p
            JOIN factories f ON f.id = p.factory_id
            {where}
            ORDER BY p.updated_at DESC, p.id DESC
            """,
            params,
        ).fetchall()


def get_project(project_id: int) -> sqlite3.Row | None:
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT p.*, f.name AS factory_name, f.code AS factory_code, f.region AS factory_region
            FROM projects p
            JOIN factories f ON f.id = p.factory_id
            WHERE p.id = ?
            """,
            (project_id,),
        ).fetchone()


def project_exists_by_code(project_code: str, exclude_id: int | None = None) -> bool:
    query = "SELECT id FROM projects WHERE project_code = ?"
    params: list[Any] = [project_code]
    if exclude_id:
        query += " AND id != ?"
        params.append(exclude_id)
    with get_connection() as conn:
        return conn.execute(query, params).fetchone() is not None


def project_exists_by_title_factory(title: str, factory_id: int, exclude_id: int | None = None) -> bool:
    query = "SELECT id FROM projects WHERE title_normalized = ? AND factory_id = ?"
    params: list[Any] = [normalize_title(title), factory_id]
    if exclude_id:
        query += " AND id != ?"
        params.append(exclude_id)
    with get_connection() as conn:
        return conn.execute(query, params).fetchone() is not None


def create_project(payload: dict[str, Any]) -> int:
    data = dict(payload)
    data["title_normalized"] = normalize_title(data["title"])
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO projects(
                project_code, title, title_normalized, factory_id, category, status,
                owner, estimated_savings, currency, start_date, target_date, description,
                updated_at
            ) VALUES(
                :project_code, :title, :title_normalized, :factory_id, :category, :status,
                :owner, :estimated_savings, :currency, :start_date, :target_date, :description,
                CURRENT_TIMESTAMP
            )
            """,
            data,
        )
        return int(cursor.lastrowid)


def update_project(project_id: int, payload: dict[str, Any]) -> None:
    data = dict(payload)
    data["id"] = project_id
    data["title_normalized"] = normalize_title(data["title"])
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE projects
            SET project_code = :project_code,
                title = :title,
                title_normalized = :title_normalized,
                factory_id = :factory_id,
                category = :category,
                status = :status,
                owner = :owner,
                estimated_savings = :estimated_savings,
                currency = :currency,
                start_date = :start_date,
                target_date = :target_date,
                description = :description,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = :id
            """,
            data,
        )


def create_import_batch(filename: str, payload: dict[str, Any]) -> str:
    batch_id = uuid.uuid4().hex
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO import_batches(id, filename, payload_json) VALUES (?, ?, ?)",
            (batch_id, filename, json.dumps(payload)),
        )
    return batch_id


def get_import_batch(batch_id: str) -> dict[str, Any] | None:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM import_batches WHERE id = ?", (batch_id,)).fetchone()
    if not row:
        return None
    payload = json.loads(row["payload_json"])
    payload["id"] = row["id"]
    payload["filename"] = row["filename"]
    payload["confirmed_at"] = row["confirmed_at"]
    return payload


def confirm_import_batch(batch_id: str) -> int:
    batch = get_import_batch(batch_id)
    if not batch or batch.get("confirmed_at"):
        return 0
    inserted = 0
    valid_rows = [row["normalized"] for row in batch["rows"] if row["can_import"]]
    with get_connection() as conn:
        for payload in valid_rows:
            conn.execute(
                """
                INSERT INTO projects(
                    project_code, title, title_normalized, factory_id, category, status,
                    owner, estimated_savings, currency, start_date, target_date, description,
                    updated_at
                ) VALUES(
                    :project_code, :title, :title_normalized, :factory_id, :category, :status,
                    :owner, :estimated_savings, :currency, :start_date, :target_date, :description,
                    CURRENT_TIMESTAMP
                )
                """,
                payload,
            )
            inserted += 1
        conn.execute(
            "UPDATE import_batches SET confirmed_at = CURRENT_TIMESTAMP WHERE id = ?",
            (batch_id,),
        )
    return inserted


def today_iso() -> str:
    return date.today().isoformat()
