"""CLI para cadastrar/atualizar líderes autorizados a autenticar na API.

Uso:
    python -m scripts.create_lider --nome "Fulano" [--inativo]

O PIN é solicitado via prompt oculto (getpass) e nunca é passado por
argumento de linha de comando nem gravado em texto puro — apenas o hash
bcrypt é persistido.
"""

import argparse
import asyncio
import getpass
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from passlib.context import CryptContext  # noqa: E402
from sqlalchemy import select  # noqa: E402

from database import AsyncSessionLocal  # noqa: E402
from db_models import Lider  # noqa: E402

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def criar_ou_atualizar_lider(nome: str, pin: str, ativo: bool) -> None:
    pin_hash = pwd_context.hash(pin)

    async with AsyncSessionLocal() as db:
        lider = await db.scalar(select(Lider).where(Lider.nome == nome))

        if lider is None:
            lider = Lider(nome=nome, pin_hash=pin_hash, ativo=ativo)
            db.add(lider)
            acao = "criado"
        else:
            lider.pin_hash = pin_hash
            lider.ativo = ativo
            acao = "atualizado"

        await db.commit()

    print(f"Líder '{nome}' {acao} com sucesso.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--nome", required=True, help="Nome do líder (identifica o login)")
    parser.add_argument(
        "--inativo", action="store_true", help="Cadastra o líder já desativado"
    )
    args = parser.parse_args()

    pin = getpass.getpass("PIN: ")
    confirmacao = getpass.getpass("Confirme o PIN: ")
    if pin != confirmacao:
        print("Os PINs não coincidem.", file=sys.stderr)
        sys.exit(1)
    if len(pin) < 4:
        print("O PIN deve ter no mínimo 4 dígitos/caracteres.", file=sys.stderr)
        sys.exit(1)

    asyncio.run(criar_ou_atualizar_lider(args.nome, pin, ativo=not args.inativo))


if __name__ == "__main__":
    main()
