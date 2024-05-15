from dataclasses import dataclass, asdict, is_dataclass, fields
import json
from typing import Type, TypeVar
import re

T = TypeVar("T") # Needed for type inference


@dataclass
class UserSettings:
    detection_color_cars: tuple[int, int, int] = (0, 255, 255)
    detection_color_people: tuple[int, int, int] = (0, 255, 0)
    detection_color_warning_signs: tuple[int, int, int] = (255,255, 0)
    detection_color_stop_signs: tuple[int, int, int] = (255, 0, 0)

    detection_thickness_cars: int = 2
    detection_thickness_people: int = 2
    detection_thickness_warning_signs: int = 2
    detection_thickness_stop_signs: int = 2

    # detections sunds??

    lines_is_on: bool = False
    lines_max_thickness: int = 30
    lines_min_thickness: int = 10
    lines_pivot_distance_from_edge = 0.05  # between 0 - 1
    lines_color: tuple[int, int, int] = (255, 255, 255)
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
    return __user_settings
