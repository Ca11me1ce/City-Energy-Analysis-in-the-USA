# Topic Modeling

# Text Dataset

We collected recent academic papers in google scholar and CNKI according to the keywords - electricity consumption or natural gas consumption. The number of paper is 100+. Please refer to ../papers/ to see the detailed papers.

# Implement

Because encoding problem, I cannot directly open pdf files and identify the textual contents. I extracted the textual contents of these papers into text.txt. The method to find the most prevalent topics is LDA (Latent Dirchlet Allocation). 

According to the textual content, top 10 related topics are:
Topic #0: gas energy natural power based electricity storage efficiency plant proposed

Topic #1: energy ng fraction urban combustion bus emission natural gas increases

Topic #2: consumption electricity lng bog energy laes power process storage cold

Topic #3: electricity consumption energy building appliances household residential results use demand

Topic #4: gas energy natural models demand electricity storage consumption using model

Topic #5: electricity data consumption clustering patterns load mining grid new analysis

Topic #6: electricity energy consumption model renewable china data gas economic based

Topic #7: cost rate efficiency exergy product analysis sng technique process cycle

Topic #8: consumption electricity energy data co2 analysis growth gas power demand

Topic #9: energy gas natural efficiency process co2 consumption economic liquefaction pipeline
