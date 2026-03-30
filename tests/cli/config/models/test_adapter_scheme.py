from tests.cli.config.models.utils import make_profile

class TestAdapterScheme:
    def test_mysql_scheme(self):
        assert make_profile(adapter="mysql").adapter_scheme == "mysql+pymysql"

    def test_postgres_scheme(self):
        assert make_profile(adapter="postgres").adapter_scheme == "postgresql+psycopg2"