import world_trade_data as wits
from requests import HTTPError
import csv
import os


def get_country_exports(country_id: str, year: int = 2021):
    request_result = wits.get_indicator(
        "MPRT-TRD-VL",
        reporter=country_id,
        partner="ALL",
        year=str(year),
        name_or_id="id",
        product="Total",
    )
    all_index_dict = request_result["Value"].to_dict()

    partner_id_trade_dict = {
        (index[1], index[2]): value for index, value in all_index_dict.items()
    }
    return partner_id_trade_dict


# Dict with Tuple (from, to) as key, the value as the value?
def get_trade_data(country_ids: list[str], year: int = 2021):
    total_dict = {}

    for id in country_ids:
        try:
            country_dict = get_country_exports(id, year)
            total_dict.update(country_dict)
        except HTTPError:
            print(f"No succes getting the data for {id}")

    return total_dict


def save_data_dict_as_csv(
    data_dict: dict,
    path: str = os.getcwd(),
    column_names: list = [
        "Reporting_country",
        "Partner_country",
        "Export_value",
    ],
):
    saving_path = os.path.join(path, "data.csv")

    # Open the file in write mode
    with open(saving_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        # Write the header
        writer.writerow(column_names)

        # Write the data
        for key, value in data_dict.items():
            writer.writerow([key[0], key[1], value])


# Example
if __name__ == "__main__":
    all_countries_df = wits.get_countries()

    id_to_name_dict = all_countries_df["name"].to_dict()

    country_ids = id_to_name_dict.keys()

    data_dict = get_trade_data(country_ids)

    save_data_dict_as_csv(data_dict)
