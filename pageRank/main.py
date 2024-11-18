import requests
from bs4 import BeautifulSoup
import pandas as pd
import networkx as nx
from urllib.parse import urljoin

def get_links(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    links = [urljoin(url, link.get('href')) for link in soup.find_all('a', href=True) if urljoin(url, link.get('href')).startswith('http')]
    return links

def crawl_links(start_url, max_depth=2):
    link_data = []
    urls_to_crawl = [(start_url, 0)]
    visited = set()

    while urls_to_crawl:
        current_url, depth = urls_to_crawl.pop(0)
        if depth > max_depth or current_url in visited:
            continue

        visited.add(current_url)
        links = get_links(current_url)

        for link in links:
            link_data.append({'zdrojová stránka': current_url, 'cílová stránka': link})
            if depth + 1 <= max_depth:
                urls_to_crawl.append((link, depth + 1))

    return link_data

def save_initial_links_to_csv(initial_links, filename):
    df = pd.DataFrame(initial_links, columns=['URL'])
    df = df.drop_duplicates()
    df.to_csv(filename, index=False)

def save_crawled_links_to_csv(link_data, filename):
    df = pd.DataFrame(link_data)
    df = df.drop_duplicates()
    df = df[~df['cílová stránka'].str.contains('/upload/')]
    df.to_csv(filename, index=False)
    return df

def create_graph(df):
    G = nx.DiGraph()
    for _, row in df.iterrows():
        source = row['zdrojová stránka']
        target = row['cílová stránka']
        G.add_edge(source, target)
    return G

def compute_pagerank(graph, max_iter=50):
    pagerank = nx.pagerank(graph, max_iter=max_iter)
    return pagerank

def save_pagerank_to_csv(pagerank, filename):
    sorted_pagerank = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)
    df = pd.DataFrame(sorted_pagerank, columns=['URL', 'PageRank'])
    df.to_csv(filename, index=False)

def print_pagerank_results(pagerank):
    sorted_pagerank = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)
    for url, rank in sorted_pagerank:
        print(f"{url}: {rank:.5f}")

def main():
    start_url = "https://leonholub.cz/"

    initial_links = get_links(start_url)
    save_initial_links_to_csv(initial_links, 'init_links.csv')

    link_data = crawl_links(start_url)
    crawled_df = save_crawled_links_to_csv(link_data, 'links.csv')

    graph = create_graph(crawled_df)
    pagerank = compute_pagerank(graph)

    print_pagerank_results(pagerank)
    save_pagerank_to_csv(pagerank, 'pagerank_results.csv')

if __name__ == "__main__":
    main()
