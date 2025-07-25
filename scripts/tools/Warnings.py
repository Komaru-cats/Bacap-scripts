from enum import Enum, auto


class AdvWarningType(Enum):
    REWARD_FUNCTION = auto()
    REWARD_FUNCTION_DOESNT_SET = auto()
    REWARD_FUNCTION_DOESNT_MATCH = auto()
    INVALID_PARENT = auto()
    EMPTY_FILES = auto()
    DONT_FILES_EXIST = auto()
    UNKNOWN_FRAME = auto()
    UNKNOWN_COLOR = auto()
    UNKNOWN_TYPE = auto()
    UNMATCHED_COLOR = auto()
    UNMATCHED_FRAME = auto()
    NO_TRANSLATE = auto()
    MISSPELLING_ERROR = auto()
    MISSING_BRANCH = auto()
    CANT_PARSE_JSON = auto()
    WRONG_SYMBOLS = auto()
    TOO_LONG_TITLE = auto()
    MISSING_TRANSLATION = auto()
    INVALID_ADVANCEMENT_IN_RELEASE = auto()


class AdvWarning:
    def __init__(self, warning_type: AdvWarningType, reason: str):
        if not reason:
            raise ValueError("Reason cannot be empty")
        self._warning_type = warning_type
        self._reason = reason

    @property
    def reason(self):
        return self._reason

    @property
    def warning_type(self):
        return self._warning_type

    def __str__(self):
        return f"[{self.warning_type.name}] {self._reason}"

    def __repr__(self):
        return f"AdvWarning(type={self.warning_type.name}, reason={self._reason})"

    @warning_type.setter
    def warning_type(self, value):
        self._warning_type = value


# USAGE EXAMPLE
if __name__ == "__main__":
    warning = AdvWarning(AdvWarningType.REWARD_FUNCTION, "Reward function is not set")
    print(warning)
