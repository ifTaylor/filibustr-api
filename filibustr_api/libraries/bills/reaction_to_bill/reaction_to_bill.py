from uuid import UUID
from datetime import datetime
from typing import Literal, Optional

from .reaction_to_bill_models.bill_reaction_counts_model import BillReactionCounts
from .reaction_to_bill_tables.reaction_orm import BillReactionORM


class ReactionToBill:
    def __init__(self, db_session):
        self.db = db_session

    def set_reaction_to_bill(
        self,
        user_id: str,
        bill_id: int,
        reaction: Optional[Literal["support", "oppose", "unsure", "outrage", "boring"]],
    ) -> BillReactionCounts:
        """
        Set or remove the user's reaction to a bill.

        If reaction is None, the user's existing reaction is removed.
        Otherwise, it is added or updated.
        """
        existing = (
            self.db.query(BillReactionORM)
            .filter_by(user_id=user_id, bill_id=bill_id)
            .first()
        )

        if reaction is None:
            if existing:
                self.db.delete(existing)
                self.db.commit()
            return self._get_reaction_counts(bill_id)

        if existing:
            existing.reaction = reaction
            existing.created_at = datetime.utcnow()
        else:
            new_reaction = BillReactionORM(
                id=UUID(),  # Or generate however your DB expects
                bill_id=bill_id,
                user_id=user_id,
                reaction=reaction,
                created_at=datetime.utcnow(),
            )
            self.db.add(new_reaction)

        self.db.commit()
        return self._get_reaction_counts(bill_id)

    def _get_reaction_counts(self, bill_id: int) -> BillReactionCounts:
        rows = (
            self.db.query(BillReactionORM.reaction, self.db.func.count())
            .filter_by(bill_id=bill_id)
            .group_by(BillReactionORM.reaction)
            .all()
        )

        # Build the counts dict
        counts = {r: 0 for r in ["support", "oppose", "unsure", "outrage", "boring"]}
        for reaction, count in rows:
            counts[reaction] = count

        return BillReactionCounts(**counts)
