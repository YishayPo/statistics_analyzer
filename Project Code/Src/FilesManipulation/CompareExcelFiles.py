##################################################################################
#                           Network workshop project                             #
#                                                                                #
# Authors: Nechama Weinberg, Yishay Polatov                                      #
#                                                                                #
# Description:                                                                   #
#                                                                                #
# Creation Date: 12/13/2020                                                      #
#                                                                                #
##################################################################################
import pandas as pd


def compare_excel_files(user_file: str, temp_file: str):
    # read the data from user excel file into pandas df
    user_excel_file = pd.ExcelFile(user_file)
    sheet = user_excel_file.sheet_names[0]
    user_data_frame = pd.read_excel(user_excel_file, sheet_name=sheet)
    # delete rows that appear twice
    user_data_frame = user_data_frame.drop_duplicates(subset=['date'], keep='first')

    # read the data from temp file (copy of shared folder) into pandas df
    temp_excel_file = pd.ExcelFile(temp_file)
    sheet = temp_excel_file.sheet_names[0]
    temp_data_frame = pd.read_excel(temp_excel_file, sheet_name=sheet)

    # data frame for the legal data - eventually will be written into the user file before push
    df_to_write = pd.DataFrame(columns=user_data_frame.columns)

    # get different data-frames for rows which are in both files and match values, rows in user file and rows in temp file
    rows_on_both_df, rows_on_user_only, rows_on_temp_only = dataframe_difference(user_data_frame, temp_data_frame)

    # add to legal df the data that's equal on both files
    df_to_write = pd.concat([df_to_write, rows_on_both_df], ignore_index=True)

    # what rows have the same dates but different in values
    rows_on_user_only['mismatch'] = rows_on_user_only.date.isin(rows_on_temp_only.date)

    # add the data that's on user file but don't contradict temp file
    df_to_write = pd.concat(
        [df_to_write, rows_on_user_only[rows_on_user_only['mismatch'] == False].drop('mismatch', axis=1)],
        ignore_index=True)

    df_to_write = pd.concat(
        [df_to_write, rows_on_temp_only], ignore_index=True)

    updated_file = pd.ExcelWriter(user_file)
    df_to_write.sort_values('date').to_excel(updated_file, sheet_name=user_excel_file.sheet_names[0], index=False)
    updated_file.save()

def solve_contradict(filename: str):
    # read the data from user excel file into pandas df
    user_excel_file = pd.ExcelFile(filename)
    sheet = user_excel_file.sheet_names[0]
    user_data_frame = pd.read_excel(user_excel_file, sheet_name=sheet)
    # delete rows that appear twice
    user_data_frame = user_data_frame.drop_duplicates(subset=['date'], keep='first')
    updated_file = pd.ExcelWriter(filename)
    user_data_frame.sort_values('date').to_excel(updated_file, sheet_name=user_excel_file.sheet_names[0], index=False)
    updated_file.save()


def dataframe_difference(df1: pd.DataFrame, df2: pd.DataFrame):
    """Find rows which are different between two DataFrames."""
    comparison_df = df1.merge(
        df2,
        indicator=True,
        how='outer'
    )
    rows_on_both = comparison_df[comparison_df['_merge'] == 'both'].drop('_merge', axis=1)
    rows_on_df1 = comparison_df[comparison_df['_merge'] == 'left_only'].drop('_merge', axis=1)
    rows_on_df2 = comparison_df[comparison_df['_merge'] == 'right_only'].drop('_merge', axis=1)
    return rows_on_both, rows_on_df1, rows_on_df2


if __name__ == '__main__':
    f1 = "excelFiles\\user.xlsx"
    f2 = "excelFiles\\temp.xlsx"
    compare_excel_files(f1, f2)

"""
if a row is in the temp but not in user data -> add that row to user df
if a row is in user data but not in temp -> leave the row in user data
if a row is both under user and temp -> let the user choose which version will be picked
"""
