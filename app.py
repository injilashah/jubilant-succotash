import streamlit as st
import preprocessor
import selected_user_stats
import matplotlib.pyplot as plt
import seaborn as sns


st.sidebar.title(":green[Whatsapp-Chat-Analysis]")

uploaded_file = st.sidebar.file_uploader(":orange[Upload text file]")

if uploaded_file is not None:
    # Read content from the uploaded file
    data = uploaded_file.getvalue()
    newdata = data.decode('utf-8')

    df = preprocessor.preprocess(newdata)
    st.subheader(":blue[Chat Data]")

    st.dataframe(df)
    print(df)
    # st.table(df)
    # fetch unique users in group
    user_list = df['Users'].unique().tolist()
    # user_list.remove('group_notification')

    user_list.sort()
    user_list.insert(0, "overall")
    selected_user = st.sidebar.selectbox("Users", user_list)

    if st.sidebar.button("Show Analysis"):
        st.title(":blue[Top Statistics]")

        # Stats Area
        num_messages, words, num_media_msgs, num_links = selected_user_stats.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header(":green[Total Messages]")
            st.title(num_messages)
        with col2:
            st.header(":green[Total words]")
            st.title(words)
        with col3:
            st.header(":green[Shared media]")
            st.title(num_media_msgs)
        with col4:
            st.header(":green[links shared]")
            st.title(num_links)

        # monthly timeline
        st.title(":blue[Monthly timeline]")
        timeline = selected_user_stats.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        plt.plot(timeline['Time'], timeline['Messages'], color='brown')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title(":blue[Daily timeline]")
        daily_timeline = selected_user_stats.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        plt.plot(daily_timeline['Date'], daily_timeline['Messages'], color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity Map
        st.title(':blue[Activity Map]')
        col1, col2 = st.columns(2)

        with col1:
            st.header(':blue[Most busy day]')
            busy_day = selected_user_stats.week_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values,
                   color=['green', 'yellow', 'pink', 'red', 'purple', 'brown', 'skyblue'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header(':blue[Most busy month]')
            busy_month = selected_user_stats.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color=['yellow', 'pink'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title(":blue[Weekly Activity Map]")
        user_heatmap = selected_user_stats.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        if selected_user == 'overall':
            st.title(":blue[Most busy person]")
            x, new_df = selected_user_stats.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                c = ["red", "green", "yellow", "purple", "brown"]
                ax.bar(x.index, x.values, color=c)
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)
        # wordcloud
        st.title(":blue[Wordcloud]")
        df_wc = selected_user_stats.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.title(':blue[ Most common words]')
        most_common_df = selected_user_stats.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        # st.dataframe(most_common_df)    //data frame for most commonly used words

        # emoji analysis
        emoji_df = selected_user_stats.emoji_helper(selected_user, df)
        st.title(':blue[Emoji Analysis]')

        col1, col2, col3 = st.columns(3)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            st.title(":blue[emoji] ")

            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct='%0.2f')
            st.pyplot(fig)
        with col3:
            st.title(":blue[Most frequent emoji] ")
            # x = helper.emoji_helper(selected_user, df)
            fig, ax = plt.subplots()
            c = ["red", "green", "yellow", "purple", "brown"]
            ax.bar(emoji_df[0].head(), emoji_df[1].head(), color=c)
            st.pyplot(fig)


















