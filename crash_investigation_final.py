import pandas as pd
from datetime import date
import calendar
import matplotlib.pyplot as plt
import numpy as np
import math

"""
Authors: Chaitanya Patel and Herat Patel
"""


def getIntersection(interX, interY):
    inter = ''
    if not isinstance(interX, float) and not isinstance(interY, float):
        # if not math.isnan(interX) and not math.isnan(interY):
        inter = str(interX).strip() + ' X ' + str(interY).strip()
    return inter


def read_data():
    df = pd.read_csv("Motor_Vehicle_Collisions_-_Crashes.csv")
    print("Total", df.shape)
    # Relevant Columns : boroughs, month, year, type of accident, latitude, longitude

    # Split the date in to month, year and  columns
    # Add day of the week column
    df['CRASH YEAR'] = [int(dt.split('/')[2]) for dt in df['CRASH DATE']]
    df['CRASH MONTH'] = [int(dt.split('/')[0]) for dt in df['CRASH DATE']]
    df['CRASH DAY OF WEEK'] = [getDay(dt) for dt in df['CRASH DATE']]

    # Quantize time by the hour
    df['CRASH TIME'] = [int(t.split(':')[0]) for t in df['CRASH TIME']]

    sum_of_count(df, df['NUMBER OF PERSONS INJURED'], df['NUMBER OF PERSONS KILLED'], 'PERSONS INVOLVED')
    sum_of_count(df, df['NUMBER OF PEDESTRIANS INJURED'], df['NUMBER OF PEDESTRIANS KILLED'], 'PEDESTRIANS INVOLVED')
    sum_of_count(df, df['NUMBER OF CYCLIST INJURED'], df['NUMBER OF CYCLIST KILLED'], 'CYCLIST INVOLVED')
    sum_of_count(df, df['NUMBER OF MOTORIST INJURED'], df['NUMBER OF MOTORIST KILLED'], 'MOTORIST INVOLVED')

    # Intersection is the ON STREET NAME X CROSS STREET NAME
    df['INTERSECTION'] = [getIntersection(interX, interY) for interX, interY in zip(df['ON STREET NAME'], df['CROSS STREET NAME'])]

    # Drop unwanted columns like reason of crash and people involved
    columns_to_delete = ['CRASH DATE', 'LOCATION', 'COLLISION_ID', 'ZIP CODE',
                         'OFF STREET NAME', 'CONTRIBUTING FACTOR VEHICLE 2', 'CONTRIBUTING FACTOR VEHICLE 3',
                         'CONTRIBUTING FACTOR VEHICLE 4', 'CONTRIBUTING FACTOR VEHICLE 5',
                         'VEHICLE TYPE CODE 2', 'VEHICLE TYPE CODE 3', 'VEHICLE TYPE CODE 4', 'VEHICLE TYPE CODE 5',
                         'NUMBER OF PERSONS INJURED', 'NUMBER OF PERSONS KILLED', 'NUMBER OF PEDESTRIANS INJURED',
                         'NUMBER OF PEDESTRIANS KILLED', 'NUMBER OF CYCLIST INJURED', 'NUMBER OF CYCLIST KILLED',
                         'NUMBER OF MOTORIST INJURED', 'NUMBER OF MOTORIST KILLED']
    df = df.drop(columns_to_delete, axis=1)
    print("Total Cleaned", df.shape)
    return df

def getDay(dt):
    month, day, year = (int(x) for x in dt.split('/'))
    ans = date(year, month, day)
    return calendar.day_name[ans.weekday()]

def sum_of_count(df, x, y, z):
    z_values = []
    for i, j in zip(x, y):
        i = i if i > 0 else 0
        j = j if j > 0 else 0
        z_values.append(int(i)+int(j))
    df[z] = z_values


def q_1(df_preCovid, df_postCovid):
    plt.subplot(1, 2, 1)
    df_preCovid.groupby(['BOROUGH']).size().plot(kind='bar')
    plt.title('Crashes by area pre COVID')

    plt.subplot(1, 2, 2)
    df_postCovid.groupby(['BOROUGH']).size().plot(kind='bar')
    plt.title('Crashes by borough post COVID')
    plt.savefig('1_crashes_by_area.png')
    plt.show()


def q_2(df_preCovid, df_postCovid):
    plt.subplot(1, 2, 1)
    df_preCovid.groupby(['CRASH MONTH']).size().plot(kind='bar')
    plt.title('Crashes by month pre COVID')

    plt.subplot(1, 2, 2)
    df_postCovid.groupby(['CRASH MONTH']).size().plot(kind='bar')
    plt.title('Crashes by month post COVID')
    plt.savefig('2_crashes_by_month.png')
    plt.show()


def q_3(df_preCovid, df_postCovid):
    plt.figure(figsize=(23, 20))
    plt.subplot(1, 2, 1)
    df_preCovid.groupby(['VEHICLE TYPE CODE 1']).size().plot(kind='bar')
    plt.title('Types of accidents pre COVID')

    # # Alternate method
    # g = df_preCovid.groupby(['VEHICLE TYPE CODE 1'])
    # print(g.filter(lambda x: len(x) > 1000))
    # k = 0
    # for xy in df_preCovid.groupby(['VEHICLE TYPE CODE 1']).size():
    #     if xy > 1000:
    #         print(df_preCovid.groupby(['VEHICLE TYPE CODE 1']).size()[k])
    #     k += 1
    # if df_preCovid.groupby(['VEHICLE TYPE CODE 1']).size() > 1000:
    # print(df_preCovid.groupby(['VEHICLE TYPE CODE 1']).apply(lambda x: (x['VEHICLE TYPE CODE 1'] > 1000).sum())
    #       .reset_index(name='count'))

    plt.subplot(1, 2, 2)
    df_postCovid.groupby(['VEHICLE TYPE CODE 1']).size().plot(kind='bar')
    plt.title('Types of accidents post COVID')
    plt.savefig('3_types_of_accidents.png')
    plt.show()


def q_4(df_preCovid, df_postCovid):
    d = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    plt.subplot(1, 2, 1)
    df_preCovid.groupby(['CRASH DAY OF WEEK']).size().reindex(d).plot(kind='bar')
    plt.title('Crashes by day pre-covid')
    plt.xticks(rotation=50)

    plt.subplot(1, 2, 2)
    df_postCovid.groupby(['CRASH DAY OF WEEK']).size().reindex(d).plot(kind='bar')
    plt.title('Crashes by day post-covid')
    plt.savefig('4_crashes_by_day_of_week.png')
    plt.xticks(rotation=50)
    plt.tight_layout()
    plt.show()

def q_5(df_preCovid, df_postCovid):
    plt.subplot(1, 2, 1)
    df_preCovid.groupby(['CRASH TIME']).size().plot(kind='bar')
    plt.title('Crashes by Hour pre-covid')

    plt.subplot(1, 2, 2)
    df_postCovid.groupby(['CRASH TIME']).size().plot(kind='bar')
    plt.title('Crashes by Hour post-covid')
    plt.savefig('5_crashes_by_hour.png')
    plt.tight_layout()
    plt.show()

def q_6(df_preCovid, df_postCovid):
    boroughs = ['BRONX', 'BROOKLYN', 'MANHATTAN', 'QUEENS', 'STATEN ISLAND']
    hours = [h for h in range(24)]

    def draw_graph(df, when):
        df_by_borough = df[df['BOROUGH'] == 'BRONX']
        x = df_by_borough.groupby(['CRASH TIME']).size()
        print('BRONX', x.values)
        plt.bar(hours, x.values, label='BRONX')
        bottom_sum = np.array(x.values)

        for b in boroughs[1:]:
            df_by_borough = df[df['BOROUGH'] == b]
            x = df_by_borough.groupby(['CRASH TIME']).size()
            print(b, x.values)
            plt.bar(hours, x.values, bottom=bottom_sum, label=b)
            bottom_sum = bottom_sum + np.array(x.values)

        plt.title('Crashes by Hour With Stacked by Borough '+when+' Covid')
        plt.legend()
        plt.savefig('6_crashes_by_hour_with_each_bor_'+when+'_covid.png')
        plt.show()

    draw_graph(df_preCovid, 'pre')
    draw_graph(df_postCovid, 'post')

def q_8(df_preCovid, df_postCovid):

    type_of_accident = ['Car Only', 'Car Pedestrian']
    car_only_pre, car_ped_pre = 0, 0
    for index, row in df_preCovid.iterrows():
        if row['PERSONS INVOLVED'] > 0:
            car_ped_pre += 1
        else:
            car_only_pre += 1
    plt.subplot(1, 2, 1)
    plt.bar(type_of_accident, [car_only_pre, car_ped_pre])
    plt.title("Type of Accident by people involved Pre-Covid")

    car_only_post, car_ped_post = 0, 0
    for index, row in df_postCovid.iterrows():
        if row['PERSONS INVOLVED'] > 0:
            car_ped_post += 1
        else:
            car_only_post += 1
    plt.subplot(1, 2, 2)
    plt.bar(type_of_accident, [car_only_post, car_ped_post])
    plt.title("Type of Accident by people involved Post-Covid")
    plt.tight_layout()
    plt.savefig('8_type_of_accident_by_people_involved.png')
    plt.show()

def q_9(df_preCovid, df_postCovid):
    # First approach
    plt.subplot(1, 2, 1)
    df_preCovid = df_preCovid[df_preCovid['INTERSECTION'].str.len() > 3]
    grouped = df_preCovid.groupby(['INTERSECTION']).size()
    grouped.sort_values(ascending=False)
    grouped.head().plot(kind='bar')
    plt.title('Most Crashes at intersections pre COVID')
    plt.xticks(rotation=90)

    plt.subplot(1, 2, 2)
    df_postCovid = df_postCovid[df_postCovid['INTERSECTION'].str.len() > 3]
    grouped = df_postCovid.groupby(['INTERSECTION']).size()
    grouped.sort_values(ascending=False)
    grouped.head().plot(kind='bar')
    plt.title('Most Crashes at intersections post COVID')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('9_1_crashes_by_intersection.png')
    plt.show()

    # Second approach
    per = df_preCovid['PERSONS INVOLVED'].to_numpy().sum()
    ped = df_preCovid['PEDESTRIANS INVOLVED'].to_numpy().sum()
    cyc = df_preCovid['CYCLIST INVOLVED'].to_numpy().sum()
    mot = df_preCovid['MOTORIST INVOLVED'].to_numpy().sum()

    per1 = df_postCovid['PERSONS INVOLVED'].to_numpy().sum()
    ped1 = df_postCovid['PEDESTRIANS INVOLVED'].to_numpy().sum()
    cyc1 = df_postCovid['CYCLIST INVOLVED'].to_numpy().sum()
    mot1 = df_postCovid['MOTORIST INVOLVED'].to_numpy().sum()

    injured_killed = ['PERSONS', 'PEDESTRIANS', 'CYCLIST', 'MOTORIST']
    injured_killed_total = [per, ped, cyc, mot]
    injured_killed_total_2020 = [per1, ped1, cyc1, mot1]

    plt.subplot(1, 2, 1)
    plt.bar(injured_killed, injured_killed_total)
    plt.title("Injured and killed Pre-Covid")
    plt.xticks(rotation=30)

    plt.subplot(1, 2, 2)
    plt.bar(injured_killed, injured_killed_total_2020)
    plt.xticks(rotation=50)
    plt.title("Injured and killed Post-Covid")
    plt.savefig('9_2_injured_and_killed.png')
    plt.show()

def q_10(df):

    df2 = df.copy()
    df = df.loc[df['CROSS STREET NAME'] == 'HOPE STREET']
    key = ["Sedan - Station Wagon/SUV", "Sedan - Sedan", "Sedan - Other"]
    value = [5, 1, 5]

    plt.bar(key, value)
    plt.title("Accidents at Hope Street")
    plt.savefig('Hope_Street.png')
    print(df.to_markdown())
    plt.show()

    df2 = df2.loc[df2['CROSS STREET NAME'] == 'HUNTS POINT AVENUE']
    key = ["Sedan - Station Wagon/SUV", "Sedan - Sedan", "Sedan - Other"]
    value = [36, 81, 61]
    print(df2.to_markdown())

    plt.bar(key, value)
    plt.title("Accidents at Hunts Point Avenue")
    plt.savefig('Hunts_Point_Avenue.png')
    plt.show()

    # areas = ['HOPE STREET', 'Hunts Point', 'Central Brooklyn', 'Brairwood', 'West Bronx']
    #
    # def guess_by_area(df2, area_name):
    #     df2 = df2.loc[df2['CROSS STREET NAME'] == area_name]
    #     print(df2.head())
    #
    #     # injured_killed = ['PERSONS', 'PEDESTRIANS', 'CYCLIST', 'MOTORIST']
    #     # per = df2['PERSONS INVOLVED'].to_numpy().sum()
    #     # ped = df2['PEDESTRIANS INVOLVED'].to_numpy().sum()
    #     # cyc = df2['CYCLIST INVOLVED'].to_numpy().sum()
    #     # mot = df2['MOTORIST INVOLVED'].to_numpy().sum()
    #     # injured_killed_total = [per, ped, cyc, mot]
    #     # plt.subplot(1, 2, 1)
    #     # plt.bar(injured_killed, injured_killed_total)
    #     # plt.title("Injured and killed Pre-Covid")
    #     # plt.xticks(rotation=30)
    #
    #     # plt.subplot(1, 2, 2)
    #     # df2 = df2.loc[df2['CROSS STREET NAME'] == area_name]
    #     # grouped = df2.groupby(['VEHICLE TYPE CODE 1']).size()
    #     # grouped.sort_values(ascending=True)
    #     # grouped.head().plot(kind='bar')
    #     # plt.title("Accidents at "+area_name)
    #     # plt.tight_layout()
    #     # plt.savefig('10_'+area_name+'.png')
    #     # plt.show()
    #
    # for area_name in areas:
    #     print(area_name)
    #     guess_by_area(df.copy(), area_name)
    # #
    # # df2 = df2.loc[df2['CROSS STREET NAME'] == 'HUNTS POINT AVENUE']
    # # key = ["Sedan - Station Wagon/SUV", "Sedan - Sedan", "Sedan - Other"]
    # # value = [36, 81, 61]
    # # print(df2.to_markdown())
    # #
    # # plt.bar(key, value)
    # # plt.title("Accidents at Hunts Point Avenue")
    # # plt.savefig('Hunts_Point_Avenue.png')
    # # plt.show()


if __name__ == '__main__':
    df = read_data()

    print(df.columns)

    df_preCovid = df[df['CRASH YEAR'] < 2020]
    df_postCovid = df[df['CRASH YEAR'] == 2020]

    print("PRE 2020", df_preCovid.shape)
    print("POST 2020", df_postCovid.shape)

    q_1(df_preCovid, df_postCovid)
    q_2(df_preCovid, df_postCovid)
    q_3(df_preCovid, df_postCovid)
    q_4(df_preCovid, df_postCovid)
    q_5(df_preCovid, df_postCovid)
    q_6(df_preCovid, df_postCovid)
    q_8(df_preCovid, df_postCovid)
    q_9(df_preCovid, df_postCovid)
    q_10(df)


