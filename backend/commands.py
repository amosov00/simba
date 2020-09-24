import asyncio
import argparse

from database.crud import UserCRUD
from schemas.user import UserCreationNotSafe


async def createsuperuser(email, password, **kwargs):
    assert email is not None and password is not None
    user = UserCreationNotSafe(
        email=email,
        password=password,
        repeat_password=password,
        is_manager=True,
        is_superuser=True,
    )
    await UserCRUD.create_not_safe(user)  # noqa
    print("Sucessfully created superuser")
    return


FUNC_MAP = {
    "createsuperuser": createsuperuser,
}


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help="commands", dest="command")

    parser_createsuperuser = subparsers.add_parser(
        "createsuperuser", help="Create superuser"
    )
    parser_createsuperuser.add_argument(
        "--email", help="User email", dest="email", required=False
    )
    parser_createsuperuser.add_argument(
        "--password", help="User password", dest="password", required=False
    )

    kwargs = vars(parser.parse_args())
    command = kwargs.pop("command")
    asyncio.get_event_loop().run_until_complete(FUNC_MAP[command](**kwargs))


if __name__ == "__main__":
    main()
