import pandas as pd
import re


def preprocess(data):
    pattern = r'\d{2}/\d{2}/\d{2}, \d{2}:\d{2} - '
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({
        'User_Messages': messages,
        'Chat_Dates': dates
    })
    df['Chats'] = pd.to_datetime(df['Chat_Dates'], format='%d/%m/%y, %H:%M - ')
    # df.head()

    users = []
    messages = []
    for message in df['User_Messages']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[2:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['Users'] = users
    df['Messages'] = messages
    df.drop(columns=['User_Messages'], inplace=True)
    pd.Series(df['Users'])
    df['Year'] = df['Chats'].dt.year
    df['Month_Num'] = df['Chats'].dt.month
    df['Month'] = df['Chats'].dt.month_name()
    df['Day'] = df['Chats'].dt.day_name()
    df['Date'] = df['Chats'].dt.date
    df['Hour'] = df['Chats'].dt.hour
    df['Minute'] = df['Chats'].dt.minute

    df.drop(columns=['Chats'], inplace=True)

    period = []
    for hour in df[['Day', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str(00))
        elif hour == 0:
            period.append(str(00) + "-" + str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour+1))

    df['Period'] = period
    return df

