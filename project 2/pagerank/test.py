import pagerank
'''
# Test transition model
dist = pagerank.transition_model(
    {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}},
    "1.html", .85
)
print(dist)


# Test get_next
dist = {"1.html": .05, "2.html": .475, "3.html": .475}
results = {"1.html": 0, "2.html": 1, "3.html": 0}
current = "2.html"
for i in range(1, 1000):
    current = pagerank.get_next(dist)
    results[current] += 1
# results should be ~{'1.html': 50, '2.html': 475, '3.html': 475}
print(results)
'''

# Test sample_pagerank
corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html", "1.html"}, "3.html": {"2.html"}}
damping_factor = .85
n = 1000

print(pagerank.sample_pagerank(corpus, damping_factor, n))


