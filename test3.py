import wikipediaapi


def search_wikipedia(query, wiki_wiki):
    page = wiki_wiki.page(query)
    return page


def display_options():
    print("\nChoose an option:")
    print("1. Scroll through paragraphs of the current article")
    print("2. Go to a related page")
    print("3. Exit the program")


def main():
    user_agent = "WikiSearcher/1.0 (https://github.com/yourusername/WikiSearcher; valk773@gmail.com)"
    wiki_wiki = wikipediaapi.Wikipedia(
        language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI,
        user_agent=user_agent
    )

    initial_query = input("Enter your initial query: ")
    current_page = search_wikipedia(initial_query, wiki_wiki)

    if not current_page.exists():
        print(f"No article found for '{initial_query}'. Exiting.")
        return

    while True:
        display_options()
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            for paragraph in current_page.text.split('\n'):
                print(paragraph)
                cont = input("Press Enter to continue or type 'stop' to stop scrolling: ")
                if cont.lower() == 'stop':
                    break

        elif choice == '2':
            print("\nRelated pages:")
            links = current_page.links.keys()
            for idx, link in enumerate(links, 1):
                print(f"{idx}. {link}")

            link_choice = int(input("Enter the number of the relaAlbert Einsteinted page you want to visit: "))
            selected_link = list(links)[link_choice - 1]
            current_page = search_wikipedia(selected_link, wiki_wiki)

            if not current_page.exists():
                print(f"No article found for '{selected_link}'. Exiting.")
                return

        elif choice == '3':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please choose 1, 2, or 3.")


if __name__ == "__main__":
    main()
