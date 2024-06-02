from dataclasses import dataclass, asdict, is_dataclass, fields
import json
from typing import Type, TypeVar
import re

T = TypeVar("T")  # Needed for type inference


@dataclass
class UserSettings:
    detection_color_cars: list[int, int, int] = (0, 255, 255)
    detection_color_people: list[int, int, int] = (0, 255, 0)
    detection_color_warning_signs: list[int, int, int] = (255, 255, 0)
    detection_color_stop_signs: list[int, int, int] = (255, 0, 0)

    detection_thickness_cars: int = 2
    detection_thickness_people: int = 2
    detection_thickness_warning_signs: int = 2
    detection_thickness_stop_signs: int = 2

    # detections sounds??

    warning_signs_alert_type: str = "box"  # none, box, sound, ???
    cars_alert_type: str = "box"
    people_alert_type: str = "box"
    stop_signs_alert_type: str = "box"

    lines_is_on: bool = False
    lines_max_thickness: int = 30
    lines_min_thickness: int = 10
    lines_pivot_distance_from_edge: float = 0.05  # between 0 - 1
    lines_color: list[int, int, int] = (255, 255, 255)
    lines_angle: int = 32
    lines_length: int = 700

    def to_json(self, include_null=False) -> dict:
        """Converts this to json.

        Args:
            include_null (bool, optional): Whether null values are included. Defaults to False.

        Returns:
            dict: Json dictionary
        """
        return asdict(
            self,
            dict_factory=lambda fields: {
                key: value
                for (key, value) in fields
                if value is not None or include_null
            },
        )

    @classmethod
    def from_json(cls: Type[T], json: dict) -> T:
        """Constructs `this` from given json.

        Args:
            json (dict): Json dictionary

        Raises:
            ValueError: When `this` isn't a dataclass

        Returns:
            T: New instance
        """
        if not is_dataclass(cls):
            raise ValueError(f"{cls.__name__} must be a dataclass")
        field_names = {field.name for field in fields(cls)}
        kwargs = {
            key: value
            for key, value in json.items()
            if key in field_names
        }
        return cls(**kwargs)


__user_settings = UserSettings()


def get_current_settings():
    """
    Returns:
        Currently used settings object.
    """
    return __user_settings


def save_settings_to_json_file(settings: UserSettings, path: str) -> bool:
    """
    Method will save UserSettings object into json file

    Args:
        settings: UserSettings object to save
        path: Path where settings will be saved

    Returns: true if success. false otherwise

    """
    text = settings.to_json()
    try:
        with open(path, 'w') as fp:
            # json.dump(text, fp)
            fp.write(json.dumps(text, indent=4))
        return True
    except OSError:
        return False


def read_settings_from_json_file(path: str) -> bool:
    """
    Method will read settings from given file and parse them into UserSettings.
    If success data will be assigned to global application settings

    Args:
        path: Path for file with settings

    Raises:
        ValueError: When parsing error occurs and file can't be loaded as UserSettings
        OSError: When given path is invalid

    Returns:
        True if success, false otherwise
    """
    try:
        global __user_settings
        f = open(path)
        data = json.load(f)
        __user_settings = UserSettings.from_json(data)
        return True
    except OSError:
        print("Invalid path")
        return False
    except ValueError:
        print("Parsing error")
        return False
