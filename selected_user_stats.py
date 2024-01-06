from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()


def fetch_stats(selected_user, df):

    if selected_user != 'overall':
        df = df[df['UserS'] == selected_user]
    # fetch num of messages
    num_messages = df.shape[0]
    # fetch num of words
    words = []
    for message in df['Messages']:
        words.extend(message.split())
    # fetch the num of media messages
    num_media_msgs = df[df['Messages'] == '<Media omitted>\n'].shape[0]

    # fetch links
    links = []
    for message in df['Messages']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_msgs, len(links)


def most_busy_users(df):

    x = df['Users'].value_counts()
    df = (round((df['Users'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'Name', 'Users': 'Percent'}))

    return x, df


def create_wordcloud(selected_user, df):
    if selected_user != 'overall':
        df = df[df['Users'] == selected_user]

    wc = WordCloud(width=500, height=500, background_color='pink')
    df_wc = wc.generate(df['Messages'].str.cat(sep=""))
    return df_wc


def most_common_words(selected_user, df):
    f = open('stop_words.txt', 'r')
    stop_words = f.read()

    if selected_user != 'overall':
        df = df[df['Users'] == selected_user]

    temp = df[df['Users'] != 'group_notification']
    temp = temp[temp['Messages'] != '<Media omitted>\n']

    words = []
    for message in temp['Messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_helper(selected_user, df):
    if selected_user != 'overall':
        df = df[df['Users'] == selected_user]

    emojis = []
    for message in df['Messages']:
        emojis.extend([c for c in message if emoji.emoji_count(c) > 0])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != 'overall':
        df = df[df['Users'] == selected_user]

    timeline = df.groupby(['Year', 'Month_Num', 'Month']).count()['Messages'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + "-" + str(timeline['Year'][i]))
    timeline['Time'] = time
    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'overall':
        df = df[df['Users'] == selected_user]

    d_timeline = df.groupby('Date').count()['Messages'].reset_index()
    return d_timeline


def week_activity(selected_user, df):
    if selected_user != 'overall':
        df = df[df['Users'] == selected_user]
    return df['Day'].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != 'overall':
        df = df[df['Users'] == selected_user]
    return df['Month'].value_counts()


def activity_heatmap(selected_user, df):
    if selected_user != 'overall':
        df = df[df['Users'] == selected_user]
    user_heatmap = df.pivot_table(index='Day', columns='Period', values='Messages', aggfunc='count').fillna(0)
    return user_heatmap





























