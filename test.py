from googlesearch import search

def get_google_search_links(query, num_results= 5):
    links = []
    for result in search(query, num_results=num_results):
        links.append(result)
    return links

# Example usage:
query = 'google'
all_links = get_google_search_links(query)

# Print the links
for link in all_links:
    print(link)
