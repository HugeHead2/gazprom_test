from test_notice.utils import get_env


SECRET_KEY = get_env("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 90
