import pandas as pd
from ast import literal_eval
import pathlib

# Setting print options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.precision', 2)

def get_pub_hols(start_year, end_year, output_folder_target, mode="binary"):
    # Defining states Lists
    states_list_str = "AU-WA,AU-ACT,AU-SA,AU-TAS,AU-VIC,AU-NT,AU-QLD,AU-NSW"
    states_list_str_alt = "['AU-WA','AU-ACT','AU-SA','AU-TAS','AU-VIC','AU-NT','AU-QLD','AU-NSW']"

    # Defining states conversion dict
    states_conv_dict = {"AU-WA": "WA",
                        "AU-ACT": "SA",
                        "AU-SA": "SA",
                        "AU-TAS": "TAS",
                        "AU-VIC": "VIC",
                        "AU-NT": "NT",
                        "AU-QLD": "QLD",
                        "AU-NSW": "NSW"}

    # List to store dataframes in
    df_list = []

    # Generate the output file name
    output_filename = f"{output_folder_target}\\AU Pub Hols Data {start_year}-{end_year} - {mode}.csv"

    # Getting the csvs for each year for nager
    for year in range(start_year, end_year + 1):
        csv_url = f"https://date.nager.at/PublicHoliday/Country/AU/{year}/CSV/"
        df = pd.read_csv(csv_url)
        df_list.append(df)

    # Combine the dataframes in the list
    combo_df = pd.concat(df_list)

    # Converting date to date type
    combo_df['Date'] = combo_df['Date'].apply(lambda x: pd.to_datetime(x, format='%Y-%m-%d'))

    # Sorting the df by date
    combo_df = combo_df.sort_values("Date")

    if mode == "binary":

        # Replacing NaNs for 'Counties'
        combo_df['Counties'] = combo_df['Counties'].fillna(states_list_str)

        # Dropping unneeded columns
        combo_df = combo_df.drop(['CountryCode', 'Fixed', 'Global', 'LaunchYear', 'Type', 'Name'], axis=1)

        # Renaming columns
        combo_df = combo_df.rename(columns={"LocalName": "Holiday Name",
                                            "Counties": "States"})

        # unpack data and create new columns for each value
        combo_df_unpacked = combo_df['States'].str.get_dummies(sep=',')

        # merge the new columns with the original DataFrame
        combo_df_dummies = pd.concat([combo_df, combo_df_unpacked], axis=1)

        # Renaming the state columns
        combo_df_dummies = combo_df_dummies.rename(columns=states_conv_dict)

        # Dropping state field
        combo_df_final = combo_df_dummies.drop(['States'], axis=1)

        # Sorting the df by date
        combo_df_final = combo_df_final.sort_values("Date")

        # Outputting the result
        combo_df_final.to_csv(output_filename, index=False)

    elif mode == "db_friendly":

        # Rename columns we want to keep
        friendly_df = combo_df.rename(columns={"Date": "CAL_DATE",
                                               "Counties": "REGION",
                                               "LocalName": "PUBLIC_HOLIDAY_DESC"})

        # Replacing NaNs for 'REGION_UNPIVOTED'
        friendly_df['REGION'] = friendly_df['REGION'].fillna(states_list_str)

        # Drop un-needed columns
        friendly_df = friendly_df.drop(['CountryCode', 'Fixed', 'Global', 'LaunchYear', 'Type', 'Name'], axis=1)

        # Creating New Columns
        friendly_df['IS_PUBLIC_HOLIDAY'] = True
        friendly_df['IS_SCHOOL_HOLIDAY'] = False
        friendly_df['SPCL_EVNT_DESC'] = pd.NA

        # Splitting the region column by comma and turning it into a list of values
        friendly_df['REGION'] = friendly_df['REGION'].str.split(",")

        # Creating a new row for every comma delimited value in 'REGION', which is now a list
        friendly_df_exploded = friendly_df.explode('REGION')

        # Renaming state values in REGION
        friendly_df_exploded['REGION'] = friendly_df_exploded['REGION'].replace(states_conv_dict)

        # Outputting the result
        friendly_df_exploded.to_csv(output_filename, index=False)

    elif mode == "raw":

        # Outputting the result
        combo_df.to_csv(output_filename, index=False)

    else:
        print("Choose one of the available modes")


# Get path of this script
script_location = pathlib.Path(__file__).parent.resolve()

# Calling the function
get_pub_hols(2010, 2026, script_location, mode="binary")
