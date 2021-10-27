import csv
import json


def json_to_csv():
    with open("result.json") as json_file:
        data = json.load(json_file)

    with open("result.csv", "w") as csv_file:
        csv_writer = csv.writer(csv_file)

        # write headers
        csv_writer.writerow(
            [
                "locality",
                "price",
                "et_type",
                "size",
                "company_name",
            ]
        )

        csv_writer.writerows(
            [
                [
                    estate["locality"]["district"],
                    estate["price"],
                    estate["et_type"],
                    estate["size"],
                    estate["company"]["name"] if estate["company"] else None,
                ]
                for estate in data["estates"]
            ]
        )


if __name__ == "__main__":
    json_to_csv()
