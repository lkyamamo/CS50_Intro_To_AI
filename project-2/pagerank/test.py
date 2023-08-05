import pagerank
import random

corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
page = "1.html"
damping_factor = 0.85

choices = pagerank.transition_model(corpus, page, damping_factor)
output = dict()
for item in corpus.items():
    output[item[0]] = 0

print(output)

current = random.choice(list(corpus.keys()))
print(current)
output[current] += 1
i = 1
while i < 10000:
    choices = pagerank.transition_model(corpus, current, damping_factor)
    current = random.choices(list(choices.keys()), tuple(choices.values()))[0]
    print(current)
    output[current] += 1
    i += 1

for item in output.items():
    output[item[0]] = item[1] / 10000

print(output)


