from .base import BaseExcelWriter


class UsersToExcel(BaseExcelWriter):
    EXCLUDE_FIELDS = (
        "verification_code",
        "telegram_id",
        "telegram_chat_id",
        "ethereum_wallet",
        "btc_wallet",
        "simba_wallet",
        "password",
        "user_eth_addresses",
        "user_btc_addresses",
        "secret_2fa",
        "signed_addresses",
        "recover_code",
    )

    def _prepare_addresses(self):
        for row in self.data:
            for field in ("user_eth_addresses", "user_btc_addresses"):
                for i, val in enumerate(row.get(field, [])):
                    row[f"{field}/{i + 1}"] = val.get("address")

        return

    def proceed(self):
        self._prepare_addresses()

        x = 1
        y = 0
        for user in self.data:
            y = self._write_header(list(user.keys()), x=0, y=y, level=0, exclude_keys=self.EXCLUDE_FIELDS)
            self._write_row(user, x, level=0, exclude_keys=self.EXCLUDE_FIELDS)
            x += 1

        self.wb.close()
        return self.output.getvalue()
