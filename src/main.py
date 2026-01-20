import pandas as pd

from config import DATA_DIR
from src.reports import spending_by_category
from src.services import get_simple_search
from src.views import get_main_json_answer

dframe = pd.read_excel(DATA_DIR)
dframe_as_list = dframe.to_dict(orient="records")

main_json_answer = get_main_json_answer("2021-11-15 06:00:00", DATA_DIR)

simple_search = get_simple_search("Перевод", dframe_as_list)

spending = spending_by_category(dframe, "Супермаркеты", "2021-11-15 06:00:00")

print(main_json_answer, simple_search, spending, sep=f'\n{"#" * 100}\n')