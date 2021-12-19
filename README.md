# TwitterNetworkAnalysis
Twitter API v2 is used fetch Tweets that could potentially be misinformed regarding the COVID pandemic. The authors of such tweets, the content, descriptions of the authors' the  followers, and the network of the Authors within Twitter are analyzed using Visualization tools in Python. 

To access Twitter data, the project uses OAuth2 with Bearer Tokens for API v2 authentication. 

Primary nodes - the authors of the tweets fetched by the API by querying a list of keywords
Second nodes - the followers of the authors or the Primary Nodes

External Packages used:
1. networkx - to create Graphs with the nodes as Twitter users fetched from the API
2. nltk - for tokenizing words from the content of the Tweets and Descriptions of users to get the frequency of the words 
3. matplotlib - to visualize graphs of the word frequencies, Retweet statistics, Public metrics (Following and Follower counts) of the authors
4. seaborn - to create a stipplot of the retweet frequncies, grouped by the search terms

Setting up OAuth2 BEARER Token:
To access tweets from Twitter API v2, the 'secrets.py' file must be set up. The file must contain the following line:
TWITTER_BEARER_TOKEN = <users_bearer_token>
To set up Bearer Token, please refer https://developer.twitter.com/en/docs/authentication/oauth-2-0/bearer-tokens

Interacting with the program:
To start the program, file 'TwitterProject.py' has to be run.

Users can interact with the CLI to choose from one of the options-

1. Word Frequencies from Users' Descriptions - a bar graph with the frequencies of terms in the 'Description' of Twitter Users. The Users include both authors of the tweets and ten of their followers
2. Word Frequencies from Tweet Content - a bar graph of the frequencies of terms in the text of the tweets fetched by querying for a list of keywords
3. Retweet Statistics - a stripplot of the number of retweets of the list of tweets collated from querying for a list of keywords, grouped by the keywords
4. Primary Node Statistics - a bargraph of the Tweet Count, and a side-by-side bar graph of the Followers and Following of the Primary Nodes
5. Network Graph - a visualization of the Primary and Secondary nodes with undirected edges connecting the nodes


