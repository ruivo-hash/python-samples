from collections import Counter
import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    #corpus = crawl("corpus0")
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
    prob_distrb = dict() # ou {}
    
    if len(corpus[page]) > 0:
        prob_d = damping_factor / len(corpus[page])
        prob_one_d = (1 - damping_factor) / len(corpus)
    else:
        prob_one_d = 1 / len(corpus)

    for pages in corpus:
        prob_distrb[pages] = prob_one_d
        if pages in corpus[page]:
            prob_distrb[pages] += prob_d

    return prob_distrb



def sample_pagerank(corpus, damping_factor, num_samples):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Simulação de navegação
    visit_counts = Counter()
    pages = list(corpus.keys())
    current_page = random.choice(pages)

    for _ in range(num_samples):
        probabilities = transition_model(corpus, current_page, damping_factor)
        # Seleciona o primeiro elemento de pages com base nos pesos passados
        next_page = random.choices(pages, weights=[probabilities[p] for p in pages])[0]
        visit_counts[next_page] += 1
        current_page = next_page

    page_rank_estimate = {page: visit_counts[page] / num_samples for page in pages}

    return page_rank_estimate

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_pages = len(corpus)
    pagerank = {page: 1 / num_pages for page in corpus.keys()}
    prob_one_d = (1 - damping_factor) / num_pages

    for page in corpus:
        if not corpus[page]:
            corpus[page] = set(corpus.keys())

    while True:
        new_pagerank = {}
        for page in corpus:
            sum_links = 0
            for link_to_page in corpus:
                # Verifica se tem link para page nos valores(links) das chaves(páginas) do corpus
                if page in corpus[link_to_page]:
                    sum_links += pagerank[link_to_page] / len(corpus[link_to_page])
            new_pagerank[page] = prob_one_d + damping_factor * sum_links
        
        converged = all(abs(new_pagerank[page] - pagerank[page]) < 0.001 for page in pagerank)
        pagerank = new_pagerank
        if converged:
            break
    
    total = sum(pagerank.values())
    pagerank = {page: rank / total for page, rank in pagerank.items()}

    return pagerank

if __name__ == "__main__":
    main()
