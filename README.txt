Data Structures Used:
1. Graph (class) in Graph.py - graph class with parameters of id, name, url,descriptione,public_metrics, isPrimary, associated_Keyword, and connectedTo. ID and name are the twitter usernames and IDs of the retrieved users. URL is the associated website associated with the account. 'description' is from the user's Twitter Description. The public metrics are the number of followers and the accounts the user is following. isPrimary is a boolean var to check if the user is an author of a tweet or not (true for authors). associated_Keyword is the Keyword whose query retrieved the user's id. ConnectedTo is a list that gets populated with the nodes the user is connected to.
2. graph - Networkx object created from the nodes of class Graph with nodes from retrieved follwers and authors, and undirected edges
3. Twitter_Graph.json - a json with the graph of nodes and edges
4. labels - the dictionary of nodes with their IDs and their usernames used for labelling the nodes on the graph
5. tweet_data - a list of dictionaries with the data from the cache or the responses of the API call for querying a keyword, key and value are the keyword and the list of tweets asscoiated with the keyword
6. Twitter_Users_Description.csv - an dictionary of the Twitter authors and their followers descritions with ID loaded to a CSV
7. Tweet_Description.csv - A dictionary of author IDs and the text of the tweet loaded to a CSV file
8. Retweet_Data.json - A json file of the list of dictionaries associated with the retweet metrics of each retrieved tweet
9. Primary_Nodes.json - A json file of the list of dictionaries. Each dictionary in the list has the data of primary nodes of the username, public_metrics, description of each of the authors of the tweets
