from typing import List
from hardstucks_debating.debate_strategy_group_aware_impl import (
    DebateFormatStrategyGroupAware,
)


class TraditionalGroupAware(DebateFormatStrategyGroupAware):
    """6-role traditional debate format using generalized role-room pair approach."""

    @property
    def role_map(self) -> List[str]:
        return ["1st Aff", "1st Neg", "2nd Aff", "2nd Neg", "3rd Aff", "3rd Neg"]
