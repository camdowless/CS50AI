import os
import random
import re
import sys
from random import choices

import numpy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    dist = dict()
    current_site_links = corpus.get(page)
    if current_site_links is None:
        total_pages = list(corpus)
        size = len(total_pages)
        prob = 1 / size
        for p in total_pages:
            dist[p] = prob
    else:
        size = len(current_site_links)
        dist[page] = round((1 - damping_factor) / (size + 1), 3)
        for p in current_site_links:
            dist[p] = round(damping_factor / size, 3)
    return dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    total_pages = list(corpus)
    first_page_index = random.randint(-1, len(total_pages) - 1)
    current_page = total_pages[first_page_index]
    estimate = dict()
    estimate[current_page] = 1
    for i in range(1, n):
        current_page = get_next(transition_model(corpus, current_page, damping_factor))
        if current_page in estimate:
            estimate[current_page] += 1
        else:
            estimate[current_page] = 1
    estimate.update((x, y / n) for x, y in estimate.items())
    return estimate


def get_next(dist):
    population = list(dist)
    values = list(dist.values())
    index = str(choices(population, values)).strip("['']")
    return str(index)


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    numLinks = dict() # looks like 'page': num links
    linked_pages = dict() # looks like 'page P': set of all pages that link to P

    for page in corpus:
        linked_pages[page] = set()
        if len(corpus[page]) == 0:
            corpus[page] = set(corpus.keys())

    for page in corpus:
        for link in corpus[page]:
            linked_pages[link].add(page)
        numLinks[page] = len(corpus[page])

    N = len(corpus)
    ranks = dict()
    highest_change = 1
    # set all ranks to 1 / N to start
    for page in corpus:
        ranks[page] = 1 / N
    while highest_change >= .001:
        changes = list()
        next = dict()
        for page in corpus:
            next[page] = (1 - damping_factor) / N
            for link in linked_pages[page]:
                next[page] += damping_factor * (ranks[link] / numLinks[link])
        for page in corpus:
            changes.append(abs(next[page] - ranks[page]))
            ranks[page] = next[page]
        highest_change = max(changes)
    return ranks

if __name__ == "__main__":
    main()
