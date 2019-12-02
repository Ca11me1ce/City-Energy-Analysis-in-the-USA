# Topic Modeling

# Text Dataset

We collected recent academic papers in google scholar and CNKI according to the keywords - electricity consumption or natural gas consumption. The number of paper is 100+. Please refer to ../papers/ to see the detailed papers.

# Implement

Because encoding problem, I cannot directly open pdf files and identify the textual contents. I extracted the titles and abstrcts of these papers and stored them in title.txt and abstract.txt individually. The method to find the most prevalent topics is LDA (Latent Dirchlet Allocation). 

According to the titles, top 10 related topics are:
Topic #0: scale multi future market utilization
Topic #1: consumption electricity study approach model
Topic #2: energy electricity analysis natural gas
Topic #3: electricity consumption energy based analysis
Topic #4: gas natural energy consumption electricity
Topic #5: consumption electricity residential china regression
Topic #6: electricity energy natural gas consumption
Topic #7: gas energy natural electricity consumption
Topic #8: electricity production generation low efficiency
Topic #9: consumption electricity term forecasting long

According to the abstracts, top 10 related topics are:
Topic #0: gas energy electricity based natural
Topic #1: consumption electricity energy forecasting model
Topic #2: electricity consumption temperature carbon load
Topic #3: electricity consumption economic energy emissions
Topic #4: consumption growth electricity energy sgd
Topic #5: electricity gas power energy exergy
Topic #6: gas fuel production natural expander
Topic #7: energy electricity gas power storage
Topic #8: consumption electricity energy data model
Topic #9: energy gas natural efficiency process 
