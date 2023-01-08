from typing import Union, Optional

class Settings:
    """Represents the user Settings."""

    def __init__(self, data: dict) -> None:
        self._data: dict = data
        self.credentials = Credentials(self._data.get("credentials", {}))
        self.options = Options(self._data.get("options", {}))
        self.miscellaneous = Miscellaneous(self._data.get("miscellaneous", {}))


class Credentials:
    """Represents the Credentials set by the user."""

    def __init__(self, data: dict) -> None:
        self._data: dict = data
        self.token: str = self._data.get("token", "")
        self.channel_id: int = int(self._data.get("channel_id", ""))


class Miscellaneous:
    """Represents the Miscellaneous settings."""
    def __init__(self, data: dict) -> None:
        self._data: dict = data
        self.premium: bool = data.get('premium', False)
        self.postmemes_platform: str = data.get('postmemes-platform', "")
        self.postmemes_memeType: str = data.get('postmemes-memetype', "")

class Options:
    """Represents the options set by the user."""

    def __init__(self, data: dict) -> None:
        self._data: dict = data
        self.normal = NormalOptions(self._data.get("normal", {}))
        self.button = ButtonOptions(self._data.get("button", {}))
        self.powerup = PowerupOptions(self._data.get("powerup", {}))
        self.other = OtherOptions(self._data.get("other", {}))
        self.types = [self.normal, self.button, self.powerup, self.other]


class NormalOptions:
    """Represents the normal options set by the user."""

    def __init__(self, data: dict) -> None:
        self._data: dict = data
        self.fish: Option = Option(self._data, "fish", NormalOptions)
        self.hunt: Option = Option(self._data, "hunt", NormalOptions)
        self.beg: Option = Option(self._data, "beg", NormalOptions)
        self.commands = [self.fish, self.hunt, self.beg]


class ButtonOptions:
    """Represents the button options set by the user."""

    def __init__(self, data: dict) -> None:
        self._data: dict = data
        self.search: Option = Option(self._data, "search", ButtonOptions, 2)
        self.crime: Option = Option(self._data, "crime", ButtonOptions, 2)
        # self.postmemes: Option = Option(self._data, "postmemes", ButtonOptions, 2)
        self.commands = [self.search, self.crime]


class PowerupOptions:
    """Represents the powerup options set by the user."""

    def __init__(self, data: dict) -> None:
        self._data: dict = data
        self.ammo: Option = Option(
            self._data,
            "ammo",
            PowerupOptions,
        )
        self.taco: Option = Option(
            self._data,
            "taco",
            PowerupOptions,
        )
        self.pizza: Option = Option(
            self._data,
            "pizza",
            PowerupOptions,
        )
        self.apple: Option = Option(
            self._data,
            "apple",
            PowerupOptions,
        )
        self.whiskey: Option = Option(
            self._data,
            "whiskey",
            PowerupOptions,
        )
        self.robbers_mask: Option = Option(
            self._data,
            "robbers_mask",
            PowerupOptions,
            "robbersmask"
        )
        self.fishing_bait: Option = Option(
            self._data,
            "fishing_bait",
            PowerupOptions,
            "fishingbait"
        )
        self.prestige_coin: Option = Option(
            self._data,
            "prestige_coin",
            PowerupOptions,
            "prestigecoin"
        )
        self.commands: list[Option] = [
            self.ammo,
            self.taco,
            self.pizza,
            self.apple,
            self.whiskey,
            self.robbers_mask,
            self.fishing_bait,
            self.prestige_coin,
        ]


class OtherOptions:
    """Represents the other options set by the user."""

    def __init__(self, data: dict) -> None:
        self._data: dict = data
        self.postmemes: Option = Option(self._data, "postmemes", OtherOptions)
        self.commands: list[Option] = [self.postmemes]


AllOptions = Union[NormalOptions, ButtonOptions, PowerupOptions, OtherOptions]


class Option:
    """Represents an option."""

    def __init__(
        self,
        data: dict,
        name: str, 
        type_: AllOptions,
        button_count: Optional[int] = None,
        custom_id: Optional[str] = None
    ) -> None:
        self.name: str = name
        self.type: AllOptions = type_
        self.state: bool = data.get(name, False)
        self.button_count: Optional[int] = button_count
        if isinstance(type, PowerupOptions):
            self.custom_id: Optional[str] = custom_id or name

class Cooldowns:
    """Represents the cooldowns of commands."""

    def __init__(self, data: dict) -> None:
        self.normal = NormalCooldowns(data.get("normal", {}))
        self.premium = PremiumCooldowns(data.get("premium", {}))


class NormalCooldowns:
    """Represents the normal cooldowns of commands."""

    def __init__(self, data: dict) -> None:
        self.fish: int = data.get("fish", 0)
        self.hunt: int = data.get("hunt", 0)
        self.dig: int = data.get("dig", 0)
        self.beg: int = data.get("beg", 0)
        self.deposit: int = data.get("deposit", 0)
        self.crime: int = data.get("crime", 0)
        self.postmemes: int = data.get("postmemes", 0)
        self.search: int = data.get("search", 0)
        self.trivia: int = data.get("trivia", 0)
        self.highlow: int = data.get("highlow", 0)
        self.raw: dict = data


class PremiumCooldowns:
    """Represents the premium cooldowns of commands."""

    def __init__(self, data: dict) -> None:
        self.fish: int = data.get("fish", 0)
        self.hunt: int = data.get("hunt", 0)
        self.dig: int = data.get("dig", 0)
        self.beg: int = data.get("beg", 0)
        self.deposit: int = data.get("deposit", 0)
        self.crime: int = data.get("crime", 0)
        self.postmemes: int = data.get("postmemes", 0)
        self.search: int = data.get("search", 0)
        self.trivia: int = data.get("trivia", 0)
        self.highlow: int = data.get("highlow", 0)
        self.raw: dict = data
