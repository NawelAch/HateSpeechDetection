# import time
# from pytrends.request import TrendReq
# import random

# def get_google_trends(search_terms):
#     # Create the TrendReq object
#     pytrend = TrendReq(hl='ar')  # Arabic language
#     terms = [term.strip() for term in search_terms if term.strip()]

#     if not terms:
#         raise ValueError("No valid search terms provided")

#     retries = 0
#     max_retries = 5  # Max retries before giving up
#     wait_time = 10  # Initial wait time before retry

#     while retries < max_retries:
#         try:
#             # Request Google Trends data
#             pytrend.build_payload(terms, timeframe='now 7-d')
#             df = pytrend.interest_over_time()

#             # If data is empty
#             if df.empty:
#                 raise ValueError("No data found for the provided search terms.")

#             # Drop the 'isPartial' column if it exists
#             if 'isPartial' in df.columns:
#                 df = df.drop(columns=['isPartial'])

#             # Organize the data
#             google_trends_data = {
#                 "dates": df.index.strftime("%Y-%m-%d %H:%M:%S").tolist(),
#                 "data": {col: df[col].tolist() for col in df.columns}
#             }

#             return {
#                 "google_trends": google_trends_data
#             }

#         except Exception as e:
#             # If a 429 error or other error occurs, handle it
#             print(f"Error: {e}")
            
#             if '429' in str(e):  # Handle rate-limiting
#                 retries += 1
#                 print(f"Rate limit reached. Retrying in {wait_time} seconds...")
#                 time.sleep(wait_time)
#                 wait_time = min(wait_time * 2, 60)  # Exponential backoff (doubling the wait time)

#             else:
#                 raise ValueError(f"Error retrieving Google Trends data: {e}")

#     # If we exhausted retries, raise an error
#     raise ValueError("Max retries reached. Could not fetch Google Trends data.")


import time
from pytrends.request import TrendReq
import random

def get_google_trends(search_terms, category=""):
    # Create the TrendReq object
    pytrend = TrendReq(hl='ar')  # Arabic language
    terms = [term.strip() for term in search_terms if term.strip()]

    if not terms:
        raise ValueError("No valid search terms provided")

    retries = 0
    max_retries = 5  # Max retries before giving up
    wait_time = 10  # Initial wait time before retry

    while retries < max_retries:
        try:
            # Request Google Trends data
            pytrend.build_payload(terms, timeframe='now 7-d')
            df = pytrend.interest_over_time()

            # If data is empty
            if df.empty:
                raise ValueError("No data found for the provided search terms.")

            # Drop the 'isPartial' column if it exists
            if 'isPartial' in df.columns:
                df = df.drop(columns=['isPartial'])

            # Organize the data
            google_trends_data = {
                "dates": df.index.strftime("%Y-%m-%d %H:%M:%S").tolist(),
                "data": {col: df[col].tolist() for col in df.columns}
            }

            # Return the trend data along with its category
            trends_with_category = []
            for term in terms:
                trends_with_category.append({
                    "trend": term,
                    "category": category
                })

            return {
                "google_trends": google_trends_data,
                "trends_with_category": trends_with_category
            }

        except Exception as e:
            # If a 429 error or other error occurs, handle it
            print(f"Error: {e}")
            
            if '429' in str(e):  # Handle rate-limiting
                retries += 1
                print(f"Rate limit reached. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                wait_time = min(wait_time * 2, 60)  # Exponential backoff (doubling the wait time)

            else:
                raise ValueError(f"Error retrieving Google Trends data: {e}")

    # If we exhausted retries, raise an error
    raise ValueError("Max retries reached. Could not fetch Google Trends data.")


