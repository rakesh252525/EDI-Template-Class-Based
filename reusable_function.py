from datetime import datetime

def find_datetime_format(string):
    formats = [
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%S"

        # Add more formats if needed
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(string, fmt)
            return fmt
        except ValueError:
            pass

    return None

# Example usage
# string1 = "2022-12-06T01:46:34.611512316161Z"
# str2="2022-06-13T01:52:25"
# format = find_datetime_format(string1)
# if format:
#     print("Datetime format found:", format)
# else:
#     print("No matching datetime format found.")
