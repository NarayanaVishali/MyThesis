README

My Thesis has 4 models implemented:
1. Indegree_Retweets_Mentions_Model
2. Topic_Diffusion_Model
3. TWEET_PROPAGATION
4. USER_INFLUENCE

1) Indegree_Retweets_Mentions_Model
This is one of the models developed from the literature review. The users are ranked based on the number of followers, retweets and mentions.
It has 3 sub-folders:

	a. CODE
	The CODE folder contains the necessary code files for the implementation of this model. They are executed in this order:
	ExtractFields.py is used to extract the necessary fields from the raw json data.
	ChangeDateFormat is used to change the date format.
	Twitter.java and User.java are executed combinely to rank the users based on the number of followers, retweets and mentions.

	b. RESULTS
	The RESULTS folder contains the results of this model for three domains: FLU, FOOD_POISONING, TRUMP_POLITICS

	c. CORRELATION_RESULTS
	The CORRELATION_RESULTS folder contains the correlation results of flu data and food poisoning data between followers, retweets and mentions.

2) Topic_Diffusion_Model
This is one of the models developed from the literature review. The daily retweet connections are count.It has 2 sub-folders:

	a. ConnectionsCount.java
	This is the code developed to count the number of connections on every day.

	b. RESULTS
	This contains the results of this model for three domains: FLU, FOOD_POISONING, TRUMP_POLITICS and their graphs.

3) 	TWEET_PROPAGATION
This folder has the necessary code for tweet_propagation computation with results and graphs included.

	a. TWEET_PROPAGATION_CODE
	The TWEET_PROPAGATION_CODE  folder has 3 sub-folders which are executed in this order:
		i) Data Filtering
		ii) Tweet_Level_Computation
		iii) Topic_Potential_Computation
	b. TWEET_PROPAGATION_RESULTS
	The TWEET_PROPAGATION_RESULTS folder contains the results of TWEET_PROPAGATION_CODE for for three domains: FLU, FOOD_POISONING, TRUMP_POLITICS
	
4) USER_INFLUENCE
The USER_INFLUENCE folder has 2 sub-folders:
	a. USER_INFLUENCE_CODE
	This has all the code necessary for user influence computation. The files are executed in this order:
		i) DataFilteringMapper.py
		ii) Tweet_Level_Computation.py
		iii) Topic_Potential_Computation
		iv) Multi-Level-Marketing / Root-User-Benefits (based on your choice)
	b. USER_INFLUENCE_RESULTS
	This has the results of USER_INFLUENCE model for three domains: FLU, FOOD_POISONING, TRUMP_POLITICS. A comparison of Multi-level-marketing and Root-User-Benefits models is made.