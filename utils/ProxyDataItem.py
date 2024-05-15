class ProxyDataItem:
    ip: str
    port: int
    login: str
    password: str

    def __init__(self, ip, port, login, password):
        self.ip = ip
        self.port = port
        self.login = login
        self.password = password

    @staticmethod
    def from_raw(raw_format_data: str = None) -> 'ProxyDataItem':
        splitted_proxy_data = raw_format_data.split(":")

        return ProxyDataItem(
            ip=splitted_proxy_data[0],
            port=splitted_proxy_data[1],
            login=splitted_proxy_data[2],
            password=splitted_proxy_data[3]
        )


    def to_dict(self) -> dict:
        return {
            "ip": self.ip,
            "port": self.port,
            "login": self.login,
            "password": self.password
        }

    @staticmethod
    def from_dict(proxy: dict) -> 'ProxyDataItem':
        return ProxyDataItem(
            ip=proxy.get("ip"),
            port=proxy.get("port"),
            login=proxy.get("login"),
            password=proxy.get("password")
        )

    @staticmethod
    def get_proxys_list_from_raw_proxys_list(proxys_data_list: list[str]) -> list['ProxyDataItem']:
        return [ProxyDataItem.from_raw(item) for item in proxys_data_list]

    @staticmethod
    def get_proxys_list_on_json_format(proxys_list: list['ProxyDataItem']) -> list[dict]:
        return [proxy_data.to_dict() for proxy_data in proxys_list]


