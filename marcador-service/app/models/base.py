from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column


class SoftDeleteMixin:
    """Mismo patrón que backend.utils.models.SoftDeleteModel del proyecto principal."""

    status: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    def soft_delete(self) -> None:
        self.status = False
        self.deleted_at = datetime.now().astimezone()

    def restore(self) -> None:
        self.status = True
        self.deleted_at = None
