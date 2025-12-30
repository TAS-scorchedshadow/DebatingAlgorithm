from typing import List
from hardstucks_debating.debate_strategy_group_aware_impl import (
    DebateFormatStrategyGroupAware,
)


class BritishParliamentaryGroupAware(DebateFormatStrategyGroupAware):
    """8-role British Parliamentary debate format using generalized role-room pair approach."""

    @property
    def role_map(self) -> List[str]:
        return [
            "Prime Minister",
            "Leader of Opposition",
            "Deputy Prime Minister",
            "Deputy Leader of Opposition",
            "Member of Government",
            "Member of Opposition",
            "Government Whip",
            "Opposition Whip",
        ]
