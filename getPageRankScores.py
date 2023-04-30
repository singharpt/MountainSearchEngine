import json

page_rank_score_file = "pagerank_score"


f = open(page_rank_score_file, "r")

pagerank_score_dict = {}

line = f.readline()

while (line):
    lineItem = line.replace("\n", "").split("\t")
    pagerank_score_dict[lineItem[0]] = lineItem[1]
    line = f.readline()
    
print(len(pagerank_score_dict))
json_object = json.dumps(pagerank_score_dict)

with open("pagerank_scores", "w") as outfile:
    outfile.write(json_object)





