import pandas as pd

def load_ng_consumption(filepath):
    df = (
        pd.read_excel(filepath, sheet_name="Data 1", skiprows=2)
        .dropna(subset=['U.S. Natural Gas Total Consumption (MMcf)'])
        .assign(
            Date=lambda x: pd.to_datetime(x['Date']),
            Year=lambda x: x['Date'].dt.year,
            Month=lambda x: x['Date'].dt.month,
            Quarter=lambda x: x['Date'].dt.quarter,
            **{
                'U.S. Natural Gas Total Consumption (Bcf)': 
                lambda x: x['U.S. Natural Gas Total Consumption (MMcf)'] / 1000
            }
        )
        [['Date','U.S. Natural Gas Total Consumption (Bcf)','Year','Month','Quarter']]
        .set_index('Date')
    )

    # normalize to start of month 
    df.index = df.index.to_period('M')
    df.index = df.index.to_timestamp() 
    # set monthly frequency 
    df = df.asfreq('MS')

    return df


