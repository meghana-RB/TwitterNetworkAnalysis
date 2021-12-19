import requests
import json
import secrets
import Graph
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import ngrams
from collections import Counter
import seaborn as sns
import regex as re
import Graph_Json as gj

CACHE_FILENAME = "twitter_cache.json"
CACHE_DICT = {}

bearer_token = secrets.TWITTER_BEARER_TOKEN
search_url = "https://api.twitter.com/2/tweets/search/recent"
List_of_keywords =  ["scamdemic", "stop complying", "no masks", "#covidhoax", "do not comply", "#novaccineforme"]
#"stop complying", "no masks"['#covidhoax', '#masksoff', '#notolockdown', '#novaccineforme', '#rejectthevaccine', "scamdemic" "scamdemic", "plandemic", "#plandemic", 
#"#COVID19coverup", "stop complying", "do not comply", "#donotcomply", "#stopcomplying", "#hydroxychloroquine"]
#'masksoff', 'scamdemic', 'no masks', '#covidhoax', '']

def open_cache():
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 

def construct_unique_key(baseurl, params):
    param_strings = []
    connector = '_'
    for k in params.keys():
        param_strings.append(f'{k}_{params[k]}')
    param_strings.sort()
    unique_key = baseurl + connector +  connector.join(param_strings)
    return unique_key

def construct_param(keyword):
    query_params = {'query': keyword +' -is:retweet', 'max_results':'10', 'tweet.fields': 'author_id,public_metrics'}
    return query_params

def create_url_retweets(id):
    user_fields = {"user.fields":"created_at,description"}
    url = "https://api.twitter.com/2/tweets/{}/retweeted_by".format(id)
    return url, user_fields

def create_url_followers(id, isPrimaryNode=False):
    user_fields = {"user.fields": "created_at,url,description,public_metrics"}
    url_followers = "https://api.twitter.com/2/users/{}/followers".format(id)
    url_id = "https://api.twitter.com/2/users/{}".format(id)
    return url_followers,url_id,user_fields

def bearer_oauth_followers(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FollowersLookupPython"
    return r

def bearer_oauth_users(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r

def bearer_oauth_recent_tweets(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def bearer_oauth_retweets(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RetweetedByPython"
    return r

def connect_to_endpoint(url, params, type):
    request_key = ''
    CACHE_DICT = open_cache()
    if type == "recent_tweets":
        request_key = construct_unique_key(url, params)
        if request_key in CACHE_DICT.keys():
            response =  CACHE_DICT[request_key]
        else:
            response = requests.get(url, auth=bearer_oauth_recent_tweets, params=params)
            CACHE_DICT[request_key] = response.json()
            save_cache(CACHE_DICT)
            print(response.status_code)
            if response.status_code != 200:
                raise Exception(response.status_code, response.text)
    if type == "retweets":
        request_key = construct_unique_key(url, params)
        if request_key in CACHE_DICT.keys():
            response =  CACHE_DICT[request_key]
        else:
            response = requests.get(url, auth=bearer_oauth_retweets, params=params)
            CACHE_DICT[request_key] = response.json()
            save_cache(CACHE_DICT)
            if response.status_code != 200:
                raise Exception(response.status_code, response.text)
    if type == "followers":
        request_key = construct_unique_key(url, params)
        if request_key in CACHE_DICT.keys():
            response =  CACHE_DICT[request_key]
        else:
            response = requests.get(url, auth=bearer_oauth_followers, params=params)
            if response.status_code != 200:
                raise Exception(response.status_code, response.text)
            else:
                CACHE_DICT[request_key] = response.json()
                save_cache(CACHE_DICT)
    if type == "users":
        request_key = construct_unique_key(url, params)
        if request_key in CACHE_DICT.keys():
            response =  CACHE_DICT[request_key]
        else:
            response = requests.get(url, auth=bearer_oauth_users, params=params)
            if response.status_code != 200:
                raise Exception(response.status_code, response.text)
            else:
                CACHE_DICT[request_key] = response.json()
                save_cache(CACHE_DICT)

    return CACHE_DICT[request_key]

def checkCommonFollowers(graph, listOfFollowers):
    set_of_node_ids = set([x.getId() for x in (graph.nodes())])
    set_of_follower_ids = set([x.getId() for x in listOfFollowers])
    common_followers = set_of_node_ids.intersection(set_of_follower_ids)

    return common_followers

def get_followers(id, graph, labels, keyword):
    list_of_followers = []
    response_dictionary = {}
    api_path_followers, api_path_user, fields = create_url_followers(id)
    response_json_id = connect_to_endpoint( api_path_user , fields, "users")
    fields['max_results'] = '10'
    response_json_followers = connect_to_endpoint( api_path_followers , fields, "followers")
    keys = ('username','url','description','public_metrics', 'name', 'created_at', 'id')

    primaryNode = Graph.Node(key = id, name = response_json_id['data']['username'], url = response_json_id['data']['url'], description = response_json_id['data']['description'], public_metrics = response_json_id['data']['public_metrics'], isPrimary=True, associated_Keyword=keyword)
    graph.add_node(primaryNode)
    labels[primaryNode] = keyword + "\n(" + primaryNode.getUsername() + ")"
    response_dictionary[primaryNode.getId()] = primaryNode.description

    secondaryNodes = []

    if 'data' in response_json_followers.keys():
        for iteration, followers in enumerate(response_json_followers['data']):
            if set(keys) == set(followers.keys()): 
                secondaryNodes.append(Graph.Node(followers['id'], followers['username'], followers['url'], followers['description'], followers['public_metrics'], isPrimary=False, associated_Keyword=keyword))
                list_of_followers.append(secondaryNodes[iteration])
                response_dictionary[secondaryNodes[iteration].getId()] = secondaryNodes[iteration].description

    common_followers = checkCommonFollowers(graph, list_of_followers)

    for followers in list_of_followers:
        if followers.getId() in common_followers:
            list_of_followers.remove(followers)
        else:
            graph.add_node(followers)
            labels[followers] = followers.getUsername()
            graph.add_edge(primaryNode, followers)
            followers.addNeighbor(primaryNode.getId())
            primaryNode.addNeighbor(followers.getId())

    for node in graph.nodes():
        if node.getId() in common_followers:
            node.addNeighbor(primaryNode.getId())
            primaryNode.addNeighbor(node.getId())
            graph.add_edge(primaryNode, node)
    
    #save_tweet_data(response_dictionary, 'Twitter_Users_Description.csv')
    return graph, labels, response_json_id

def save_tweet_data(tweet_data, filename):
    fieldnames = ['ID', 'Description']
    with open(filename, 'a', encoding="utf-8", newline='') as csvfile:
        writer = csv.writer(csvfile)
        if csvfile.tell() == 0:
            writer.writerow(["ID", "Description"])
        for row in tweet_data.items():
            writer.writerow(row)

def view_Primary_follower_counts(filename):

    with open(filename, 'r') as f:
        primaryNodeData = json.load(f)
    list_of_followers = []
    list_of_following = []
    tweet_count = []
    data = []
    usernames = []

    for primaryNodes in primaryNodeData:
        list_of_followers.append(primaryNodes['data']['public_metrics']['followers_count'])
        list_of_following.append(primaryNodes['data']['public_metrics']['following_count'])
        usernames.append(primaryNodes['data']['username'])
        tweet_count.append(primaryNodes['data']['public_metrics']['tweet_count'])
    
    data.append(list_of_followers)
    data.append(list_of_following)
    data.append(tweet_count)

    ind = np.arange(len(list_of_followers)) 
    width = 0.35

    fig1, ax = plt.subplots()
    plt.xticks(ind, labels = tuple(usernames), rotation = 90)
    fig2, ax_dash = plt.subplots()
    plt.xticks(ind, labels = tuple(usernames), rotation = 90)

    rects1 = ax_dash.bar(ind - width/2, list_of_followers, width,
                label='List of Followers')
    rects2 = ax_dash.bar(ind + width/2, list_of_following, width,
                label='List of Following')
    rects3 = ax.bar(ind + width/2, tweet_count, width,
                label='Tweet Count')

    ax_dash.set_ylabel('Counts')
    ax_dash.set_title('Primary Node Statistics')
    ax_dash.set_xticks(ind)
    ax_dash.set_xticklabels(tuple(usernames))
    ax_dash.legend()
 
    ax.set_ylabel('Tweet Counts')
    ax.set_title('Primary Node Statistics')
    ax.set_xticks(ind)
    ax.set_xticklabels(tuple(usernames))
    ax.legend()

    plt.show()

def word_frequencies(filename):
    fields = fields = ['Description']
    data = pd.read_csv(filename, encoding ="utf-8",  skipinitialspace=True, usecols=fields)
    Large_Description_String = ''
    for descriptions in data.Description:
        Large_Description_String = Large_Description_String + str(descriptions)
    
    articles_etc = ['like', 'ago', 'got', 'get', 'https', 'say', 'one', 'two', 'way', 'know', 'said']

    Large_Description_String = Large_Description_String.replace("\n", "")
    new_tokens = word_tokenize(Large_Description_String)
    new_tokens = [t.lower() for t in new_tokens]
    new_tokens =[t for t in new_tokens if t not in stopwords.words('english')]
    new_tokens = [t for t in new_tokens if t.isalpha()]
    new_tokens = [t for t in new_tokens if t not in articles_etc]
    new_tokens = [t for t in new_tokens if len(t) > 2]
    lemmatizer = WordNetLemmatizer()
    new_tokens =[lemmatizer.lemmatize(t) for t in new_tokens]
    counted = Counter(new_tokens)
    
    word_freq = pd.DataFrame(counted.items(),columns=['word','frequency']).sort_values(by='frequency',ascending=False)
    word_freq_relevant = word_freq.head(n=35)
    word_freq_relevant.plot.bar(x='word', y='frequency', rot=40)
    plt.show()

def save_data_to_Json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

def get_retweet_statistics(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    x_axis = [[] for x in range(len(List_of_keywords))]
    start = 0
    end = len(data)//len(List_of_keywords)
    retweet_dict = {}
    descriptions = {}
    for lists in x_axis:
        for i in range(start, end):
            if 'meta' in data[i].keys():
                lists.append(data[i]['meta']['result_count'])
            else:
                lists.append(0)
            if 'data' in data[i].keys():
                descriptions[data[i]['data'][0]['id']] = data[i]['data'][0]['description']
        start = end 
        end = end + len(data)//len(List_of_keywords)

    #save_tweet_data(descriptions, 'Retweet_Descriptions.csv')
 
    for x in range(len(List_of_keywords)):
        retweet_dict[List_of_keywords[x]] = x_axis[x]
    df = pd.DataFrame.from_dict(data=retweet_dict)
    sns.set(style = 'whitegrid')
    ax = sns.stripplot(data=df)
    ax.set(xlabel = "Search Terms", ylabel="Frequency of Retweets")
    plt.show()

def display_network_graph(graph, labels):
    color_map = []
    for node in graph:
        if node.isPrimary:
            color_map.append('blue')
        else: 
            color_map.append('green')   
    fig = plt.figure(1,figsize=(12,12))
    plt.title("Graph of Primary and Secondary Nodes")
    nx.draw_random(graph, labels=labels, node_color=color_map, node_size=50, font_size=7, font_family='sans-serif', width = 0.2)  
    color_map = ['Nodes: \nPrimary (blue): Twitter Users whose tweets were fetched by API for the query terms \nSecondary (green): Followers of Primary Nodes ','edges']
    plt.legend(color_map)
    plt.show()    

def main():
    # tweet_data = []
    # meta_data = []
    # retweet_data = []
    # keywords_with_ids = {}
    # graph = nx.Graph()
    # labels = {}
    # primaryNodes = []
    # ids_with_text = {}
    # ids_of_tweets = []
    
    # for keywords in List_of_keywords:
    #     json_response_tweets = connect_to_endpoint(search_url, construct_param(keywords), "recent_tweets")
    #     tweet_data.append({keywords : json_response_tweets.get('data')})
    #     meta_data.append(json_response_tweets.get('meta'))

    # for counter, data in enumerate(tweet_data):
    #     ids_of_authors = []
    #     for tweets in (data[List_of_keywords[counter]]):
    #         ids_of_authors.append(tweets.get('author_id'))
    #         ids_with_text[tweets.get('author_id')] = tweets.get('text')
    #         ids_of_tweets.append(tweets.get('id'))
    #     keywords_with_ids[List_of_keywords[counter]]  = ids_of_authors

    # #save_tweet_data(ids_with_text, 'Tweet_Description.csv')
    # for counter,keywords in enumerate(keywords_with_ids):
    #     for id in keywords_with_ids[keywords]:
    #         graph, labels, primaryNodeDetails = get_followers(id, graph, labels, List_of_keywords[counter])
    #         primaryNodes.append(primaryNodeDetails)

    #save_data_to_Json(primaryNodes, 'Primary_Nodes.json')
    # for id in ids_of_tweets:
    #     url, fields = create_url_retweets(id)
    #     json_response_retweets = connect_to_endpoint(url, fields, "retweets")
    #     retweet_data.append(json_response_retweets)

    #save_data_to_Json(retweet_data, 'Retweet_Data.json')
  
    print("Primary Nodes: authors of the tweets fetched by the query terms from the Twitter API \n Secondar Nodes: Followers of the Primary Nodes")
    while True:
        search_string = input("Enter the option for the type of the Analysis component you want to view.\n 1. Word Frequencies from Users' Descriptions \n 2. Word Frequencies from Tweet Content \n 3. Retweet Statistics \n 4. Primary Node Statistics  \n 5. Network Graph \n 6. EXIT")
        if search_string not in ['1', '2', '3', '4', '5']:
            print("Error! Invalid choice. Please enter a number between 1 to 4")
            continue
        if search_string == '6':
            break
        if search_string == '1':
            word_frequencies('Twitter_Users_Description.csv')
        if search_string == '2':
            word_frequencies('Tweet_Description.csv')
        if search_string == '3':
            get_retweet_statistics('Retweet_Data.json')
        if search_string == '4':
            view_Primary_follower_counts('Primary_Nodes.json')
        if search_string == '5':
            graph_from_json, labels1 = gj.load_graph_from_json('Twitter_Graph.json')
            display_network_graph(graph_from_json, labels1)
    
if __name__ == "__main__":
    main()
