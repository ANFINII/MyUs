from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ChannelInDTO:
    name: str
    description: str
