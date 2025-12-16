"""seed admin user

Revision ID: 46d2edc8a2e0
Revises: 1e1a6b37847d
Create Date: 2025-12-16 10:32:50.248155-06:00

"""

import os
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from dotenv import load_dotenv
from passlib.context import CryptContext

# revision identifiers, used by Alembic.
revision: str = "46d2edc8a2e0"
down_revision: Union[str, Sequence[str], None] = "1e1a6b37847d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

load_dotenv()

username = os.getenv("ADMIN_USERNAME")
email = os.getenv("ADMIN_EMAIL")
first_name = os.getenv("ADMIN_FIRST_NAME")
last_name = os.getenv("ADMIN_LAST_NAME")
password = os.getenv("ADMIN_PASSWORD")
if not all([username, email, first_name, last_name, password]):
    raise ValueError("Admin user environment variables are not fully set")

pwd_context = CryptContext(schemes=["bcrypt"])


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def upgrade() -> None:
    connection = op.get_bind()
    connection.execute(
        sa.text(
            """
            INSERT INTO users (username, email, first_name, last_name, password_hash, is_admin)
            VALUES (:username, :email, :first_name, :last_name, :password_hash, true)
            ON CONFLICT (email)
            DO UPDATE SET
                username = EXCLUDED.username,
                first_name = EXCLUDED.first_name,
                last_name = EXCLUDED.last_name,
                password_hash = EXCLUDED.password_hash,
                is_admin = true
            """
        ),
        {
            "username": username,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "password_hash": hash_password(password),  # type: ignore
        },
    )


def downgrade() -> None:
    connection = op.get_bind()
    connection.execute(
        sa.text("DELETE FROM users WHERE email = :email"),
        {"email": email},
    )
