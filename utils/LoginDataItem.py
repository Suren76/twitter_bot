from pathlib import Path


class LoginDataItem:
    login: str
    password: str
    mail: str
    mailpassword: str
    useragent: str
    token: str

    def __init__(self, login, password, mail, mailpassword, useragent, token):
        self.login = login
        self.password = password
        self.mail = mail
        self.mailpassword = mailpassword
        self.useragent = useragent
        self.token = token

    @staticmethod
    def from_raw(raw_format_data: str = None) -> 'LoginDataItem':
        splitted_account_data = raw_format_data.split(":")

        return LoginDataItem(
            login=splitted_account_data[0],
            password=splitted_account_data[1],
            mail=splitted_account_data[2],
            mailpassword=splitted_account_data[3],
            useragent=splitted_account_data[4],
            token=splitted_account_data[5]
        )

    def to_dict(self) -> dict:
        return {
            "login": self.login,
            "password": self.password,
            "mail": self.mail,
            "mailpassword": self.mailpassword,
            "useragent": self.useragent,
            "token": self.token
        }

    @staticmethod
    def from_dict(account: dict) -> 'LoginDataItem':
        return LoginDataItem(
            login=account.get("login"),
            password=account.get("password"),
            mail=account.get("mail"),
            mailpassword=account.get("mailpassword"),
            useragent=account.get("useragent"),
            token=account.get("token")
        )

    def to_raw(self):
        return ":".join([
            self.login,
            self.password,
            self.mail,
            self.mailpassword,
            self.useragent,
            self.token
        ])

    @staticmethod
    def get_accounts_list_from_raw_accounts_list(accounts_data_list: list[str]) -> list['LoginDataItem']:
        return [LoginDataItem.from_raw(data) for data in accounts_data_list]

    @staticmethod
    def get_accounts_list_from_dict_accounts_list(accounts_data_list: list[dict]) -> list['LoginDataItem']:
        return [LoginDataItem.from_dict(data) for data in accounts_data_list]

    @staticmethod
    def get_accounts_list_on_json_format(accounts_list: list['LoginDataItem']) -> list[dict]:
        return [account_data.to_dict() for account_data in accounts_list]

    @staticmethod
    def get_accounts_list_on_raw_format(accounts_list: list['LoginDataItem']) -> str:
        return "\n".join([account_data.to_raw() for account_data in accounts_list])

    def __str__(self):
        return (
            "("
            f"login={self.login}, "
            f"password={self.password}, "
            f"mail={self.mail}, "
            f"mailpassword={self.mailpassword}, "
            f"useragent={self.useragent}, "
            f"token={self.token}, "
            ")"
        )

    def __eq__(self, other: 'LoginDataItem'):
        if isinstance(other, LoginDataItem):
            return (
                    self.login == other.login and
                    self.password == other.password and
                    self.mail == other.mail and
                    self.mailpassword == other.mailpassword and
                    self.useragent == other.useragent and
                    self.token == other.token
            )
        return NotImplemented





