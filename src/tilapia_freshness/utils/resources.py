"""Resource management utilities."""

from pathlib import Path
from typing import Optional


def get_asset_path(filename: str) -> Optional[str]:
    """Get path to asset file.

    Args:
        filename: Asset filename

    Returns:
        Full path to asset or None if not found
    """

    package_dir = Path(__file__).parent.parent
    asset_path = package_dir / "assets" / filename

    if asset_path.exists():
        return str(asset_path)

    root_path = package_dir.parent.parent / filename
    if root_path.exists():
        return str(root_path)

    return None


def get_icon_path() -> Optional[str]:
    """Get application icon path.

    Returns:
        Path to icon file or None if not found
    """
    return get_asset_path("icon.png")
