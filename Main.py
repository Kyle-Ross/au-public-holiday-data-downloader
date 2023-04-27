import pandas as pd
import pathlib


def get_pub_hols(start_year, end_year, output_folder_target, mode="binary"):

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

    if mode == "binary":
        # Defining states List
        states_list_str = "AU-WA,AU-ACT,AU-SA,AU-TAS,AU-VIC,AU-NT,AU-QLD,AU-NSW"

        # Replacing NaNs for 'Counties'
        combo_df['Counties'] = combo_df['Counties'].fillna(states_list_str)

        # Dropping unneeded columns
        combo_df = combo_df.drop(['CountryCode', 'Fixed', 'Global', 'LaunchYear', 'Type', 'Name'], axis=1)

        # Renaming columns
        combo_df = combo_df.rename(columns={"LocalName": "Holiday Name",
                                            "Counties": "States"})

        # Converting date to date type
        combo_df['Date'] = combo_df['Date'].apply(lambda x: pd.to_datetime(x, format='%Y-%m-%d'))

        # unpack data and create new columns for each value
        combo_df_unpacked = combo_df['States'].str.get_dummies(sep=',')

        # merge the new columns with the original DataFrame
        combo_df_dummies = pd.concat([combo_df, combo_df_unpacked], axis=1)

        # Renaming the state columns
        combo_df_dummies = combo_df_dummies.rename(columns={"AU-WA": "WA",
                                                            "AU-ACT": "ACT",
                                                            "AU-SA": "SA",
                                                            "AU-TAS": "TAS",
                                                            "AU-VIC": "VIC",
                                                            "AU-NT": "NT",
                                                            "AU-QLD": "QLD",
                                                            "AU-NSW": "NSW"})

        # Dropping state field
        combo_df_final = combo_df_dummies.drop(['States'], axis=1)

        # Sorting the df by date
        combo_df_final = combo_df_final.sort_values("Date")

        # Outputting the result
        combo_df_final.to_csv(output_filename, index=False)

    elif mode == "raw":

        # Sorting the df by date
        combo_df = combo_df.sort_values("Date")

        # Outputting the result
        combo_df.to_csv(output_filename, index=False)

    else:
        print("Available modes are binary and raw")


# Get path of this script
script_location = pathlib.Path(__file__).parent.resolve()

# Calling the function
get_pub_hols(2015, 2023, script_location, mode="binary")
