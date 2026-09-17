import os

from dotenv import load_dotenv


load_dotenv()


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


DATA_DIR = os.path.join(BASE_DIR, "data")

REPOSITORIES_DIR = os.path.join(
    DATA_DIR,
    "repositories"
)

INDEXES_DIR = os.path.join(
    DATA_DIR,
    "indexes"
)