from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import qrcode
from qrcode.image.svg import SvgPathImage


@dataclass(frozen=True)
class QrAssetManifest:
    url: str
    png_path: str
    svg_path: str

    def to_dict(self) -> dict[str, str]:
        return {
            "url": self.url,
            "png_path": self.png_path,
            "svg_path": self.svg_path,
        }


def generate_qr_assets(
    url: str,
    output_dir: str | Path,
    *,
    stem: str = "printnet_website",
    box_size: int = 10,
    border: int = 4,
) -> QrAssetManifest:
    normalized_url = str(url or "").strip()
    if not normalized_url:
        raise ValueError("url is required")

    target_dir = Path(output_dir).expanduser().resolve()
    target_dir.mkdir(parents=True, exist_ok=True)

    normalized_stem = str(stem or "printnet_website").strip() or "printnet_website"
    png_path = target_dir / f"{normalized_stem}.png"
    svg_path = target_dir / f"{normalized_stem}.svg"

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=max(1, int(box_size)),
        border=max(1, int(border)),
    )
    qr.add_data(normalized_url)
    qr.make(fit=True)

    png_image = qr.make_image(fill_color="black", back_color="white")
    png_image.save(png_path)

    svg_image = qr.make_image(image_factory=SvgPathImage)
    svg_image.save(svg_path)

    return QrAssetManifest(
        url=normalized_url,
        png_path=str(png_path),
        svg_path=str(svg_path),
    )
