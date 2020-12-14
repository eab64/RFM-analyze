
# conditions = [(merged["days"] <= np.percentile(merged["days"], 33)),  # Меньше 109
#                   (merged["days"] <= np.percentile(merged["days"], 66)),  # Меньше 209
#                   (merged["days"] >= np.percentile(merged["days"], 66))  # Больше 209
#                   ]
#     values = ['3', '2', '1']
#     conditions2 = [(merged["Visit_count"] <= np.percentile(merged["Visit_count"], 33)),
#         (merged["Visit_count"] > np.percentile(merged["Visit_count"], 66)),
#         (merged["Visit_count"] > np.percentile(merged["Visit_count"], 33)) & (
#                     merged["Visit_count"] <= np.percentile(merged["Visit_count"], 66))
#     ]
#     values2 = ['1', '3', '2']
#     conditions3 = [(merged["Income"] <= np.percentile(merged["Income"], 33)),  # Меньше чем 12500
#         (merged["Income"] >= np.percentile(merged["Income"], 66)),  # Больше чем 31600
#         (merged["Income"] > np.percentile(merged["Income"], 33)) & (
#                 merged["Income"] < np.percentile(merged["Income"], 66))
#     ]
#     values3 = ['1', '3', '2']


def show_all():#Должен принимать дату, которая будет отсекать все что туда
    # не входит и служить конечной точкой отсчета merged["Days"]
    con = sqlalchemy.create_engine(
        'sqlite:////Users/Yeldos/PycharmProjects/no_related/no_relates/db.sqlite3')  # Connect to db
    dataframe = pd.read_sql("SELECT * FROM myapp_information WHERE Visit_status='Клиент пришёл'", con)#all client
    df_sum = dataframe[['Number','Visit_count','Income']].groupby(by='Number').sum()#Сложение income и visits_number
    df_sum.reset_index(inplace=True)
    df_by_data = dataframe[['Name','Number','Visit_data']].groupby(by='Number').max()
    merged = pd.merge(df_sum, df_by_data[['Name', 'Visit_data']], on='Number', how='inner')
    # today = date.today()# поменять на первое число
    day = '2020-12-01 13:15:00'
    merged["days"] = (pd.to_datetime(merged["Visit_data"]).sub(pd.Timestamp(day)).dt.days)*-1
    conditions = [(merged["days"] <= np.percentile(merged["days"], 33)),  # Меньше 109
                  (merged["days"] <= np.percentile(merged["days"], 66)),  # Меньше 209
                  (merged["days"] >= np.percentile(merged["days"], 66))  # Больше 209
                  ]
    values = ['3', '2', '1']
    conditions2 = [(merged["Visit_count"] == 1),
                   (merged["Visit_count"] == 2) | (merged["Visit_count"] == 3),
                   (merged["Visit_count"] >= 4)
                   ]
    values2 = ['1', '2', '3']
    conditions3 = [(merged["Income"] <= 20000),  # Меньше чем 20000
                   (merged["Income"] >= 80000),  # Больше чем 80000
                   (merged["Income"] > 20000) | (
                           merged["Income"] < 80000)
                   ]
    values3 = ['1', '3', '2']

    merged["R"] = np.select(conditions, values)
    merged["F"] = np.select(conditions2, values2)
    merged["M"] = np.select(conditions3, values3)
    merged["RFM"] = merged["R"]+merged["F"]+merged["M"]
    conditions4 = [(merged["RFM"] == '333'),
                   (merged["RFM"] == '121') | (merged["RFM"] == '122') | (merged["RFM"] == '211') | (merged["RFM"] == '212')| (merged["RFM"] == '221') | (merged["RFM"] == '231') | (merged["RFM"] == '222') | (merged["RFM"] == '321'),
                   (merged["RFM"] == '113'),
                   (merged["RFM"] == '112') | (merged["RFM"] == '131'),
                   (merged["RFM"] == '111'),
                   (merged["RFM"] == '311') | (merged["RFM"] == '312'),
                   (merged["RFM"] == '132') | (merged["RFM"] == '133') | (merged["RFM"] == '232') | (merged["RFM"] == '233') | (merged["RFM"] == '332')| (merged["RFM"] == '232')| (merged["RFM"] == '322')| (merged["RFM"] == '331'),
                   (merged["RFM"] == '123') | (merged["RFM"] == '213') | (merged["RFM"] == '223') | (merged["RFM"] == '313') | (merged["RFM"] == '323')
                   ]
    values4 = ['ЯДРО', 'Стандарт', 'Сонные киты', 'Сони', 'Потерянные', 'Новички', 'Лояльные', 'Киты']
    merged["LABEL"] = np.select(conditions4, values4)
    merged.to_excel("new_conditions.xlsx", sheet_name="Sheet1")
    print(merged)
    print(np.percentile(merged["days"], 66),np.percentile(merged["days"], 33))
    print(np.percentile(merged["Visit_count"], 66), np.percentile(merged["Visit_count"], 33))
    print(np.percentile(merged["Income"], 66), np.percentile(merged["Income"], 33))
    path = '/Users/Yeldos/PycharmProjects/no_related/no_relates/output2.xlsx' # this should live elsewhere, definitely
