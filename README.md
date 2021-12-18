# TwitterNetworkAnalysis
Twitter API v2 is used fetch Tweets that could potentially be misinformed regarding the COVID pandemic. The authors of such tweets, the content, descriptions of the authors' the  followers, and the network of the Authors within Twitter are analyzed using Visualization tools in Python. 

To access Twitter data, the project uses OAuth2 with Bearer Tokens for API v2 authentication. 

External Packages used:
1. networkx - to create Graphs with the nodes as Twitter users fetched from the API
2. nltk - for tokenizing words from the content of the Tweets and Descriptions of users to get the frequency of the words 
3. matplotlib - to visualize graphs of the word frequencies, Retweet statistics, Public metrics (Following and Follower counts) of the authors
4. seaborn - to create a stipplot of the retweet frequncies, grouped by the search terms

Interacting with the program:

Users can interact with the CLI to choose from on of the options-
1. Word Frequencies from Users' Descriptions 
2. Word Frequencies from Tweet Content
3. Retweet Statistics
4. Primary Node Statistics
5. Network Graph
