from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
REPO_ROOT = PROJECT_ROOT.parent
DEFAULT_INPUT = PROJECT_ROOT / "build" / "app_config.bin"
DEFAULT_PRIVATE_KEY = REPO_ROOT / "chery_private.pem"
DEFAULT_PUBLIC_KEY = REPO_ROOT / "chery_pubkey.pem"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Sign a build artifact with RSA-PSS + SHA-256.")
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        default=DEFAULT_INPUT,
        help=f"Artifact path to sign. Default: {DEFAULT_INPUT}",
    )
    parser.add_argument(
        "--private-key",
        type=Path,
        default=DEFAULT_PRIVATE_KEY,
        help=f"PEM private key path. Default: {DEFAULT_PRIVATE_KEY}",
    )
    parser.add_argument(
        "--public-key",
        type=Path,
        default=DEFAULT_PUBLIC_KEY,
        help=f"PEM public key path used for verification. Default: {DEFAULT_PUBLIC_KEY}",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Signature output path. Default: replace the input suffix with .sig",
    )
    parser.add_argument(
        "--txt",
        action="store_true",
        help="Also write the signature as comma-separated 0xXX text beside the .sig file.",
    )
    return parser


def require_existing_file(path: Path, description: str) -> None:
    if not path.is_file():
        raise SystemExit(f"{description} not found: {path}")


def resolve_output_path(input_path: Path, output_path: Path | None) -> Path:
    if output_path is not None:
        return output_path
    return input_path.with_suffix(".sig")


def write_signature_text(signature: bytes, output_path: Path) -> None:
    output_path.write_text(",".join(f"0x{byte:02X}" for byte in signature), encoding="utf-8")


def main() -> None:
    args = build_parser().parse_args()
    input_path = args.input.resolve()
    private_key_path = args.private_key.resolve()
    public_key_path = args.public_key.resolve()
    output_path = resolve_output_path(input_path, args.output).resolve()

    require_existing_file(input_path, "Input artifact")
    require_existing_file(private_key_path, "Private key")
    require_existing_file(public_key_path, "Public key")

    data = input_path.read_bytes()
    private_key = serialization.load_pem_private_key(private_key_path.read_bytes(), password=None)
    public_key = load_pem_public_key(public_key_path.read_bytes())

    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=32,
        ),
        hashes.SHA256(),
    )

    public_key.verify(
        signature,
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=32,
        ),
        hashes.SHA256(),
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(signature)

    print(f"input: {input_path}")
    print(f"sha256: {hashlib.sha256(data).hexdigest()}")
    print(f"signature: {output_path}")
    if args.txt:
        txt_output_path = output_path.with_suffix(".txt")
        write_signature_text(signature, txt_output_path)
        print(f"signature txt: {txt_output_path}")
    print("verify: ok")


if __name__ == "__main__":
    main()
