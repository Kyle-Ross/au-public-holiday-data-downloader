# au-public-holiday-data-downloader
A function in `Main.py` which grabs, combines and processes csv files from the https://date.nager.at/ resource which contain all public holidays for a range of years. Includes transformation modes which pivot the data.

## How to use

Clone the repo and adjust the function example at the bottom of the `Main.py` script.

The function `get_pub_hols` can be adjusted with the following arguments:
1. `start_year` (Inclusive)
2. `end_year` (Inclusive)
3. `output_folder_target` folder for csv outputs, not including ending slash
4. `mode`: Either `'binary'` or `'raw'`

## Output Modes

See included csv files for output examples.

### Binary

Indicates if a state has a holiday with a 1 or a 0, combining information by date and holiday across states.

### Raw

Data in the format directly from the source, which has each holiday and state combination on its own row.