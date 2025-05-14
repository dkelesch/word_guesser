import requests
import random
import re

# URL of the Turkish word list
WORD_LIST_URL = "https://raw.githubusercontent.com/ncarkaci/TDKDictionaryCrawler/master/TDK_S%C3%B6zl%C3%BCk_Kelime_Listesi.txt"

# Define the desired lengths and number of words per length
TARGET_LENGTHS = range(3, 11)  # 3 to 10 letter words
WORDS_PER_LENGTH = 7

def fetch_word_list(url):
    """Fetches the word list from the given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        # The file seems to be UTF-8 encoded, requests usually handles this well with response.text
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching word list from {url}: {e}")
        return None

def clean_word(word):
    """
    Cleans a word:
    - Converts to lowercase.
    - Removes leading/trailing whitespace.
    - Ensures it only contains Turkish alphabet letters.
    """
    word = word.lower().strip()
    # Turkish alphabet + standard Latin letters
    # Adjust this regex if the word list contains other valid characters you want to keep
    if re.fullmatch(r"[a-zçğıöşü]+", word):
        return word
    return None


def generate_words_by_length_from_url(url=WORD_LIST_URL, 
                                      target_lengths=TARGET_LENGTHS, 
                                      words_per_length=WORDS_PER_LENGTH):
    """
    Generates a dictionary of words categorized by length, fetched from a URL.
    """
    raw_text = fetch_word_list(url)
    if not raw_text:
        return {}

    all_fetched_words = raw_text.splitlines()
    
    categorized_words = {length: [] for length in target_lengths}
    
    # Process and categorize words
    for raw_word in all_fetched_words:
        word = clean_word(raw_word)
        if word:
            length = len(word)
            if length in categorized_words:
                categorized_words[length].append(word)

    # Randomly select words for the final dictionary
    final_word_dict = {}
    for length in target_lengths:
        available_words = categorized_words.get(length, [])
        if len(available_words) >= words_per_length:
            final_word_dict[length] = random.sample(available_words, words_per_length)
        else:
            print(f"Warning: Not enough words of length {length}. Found {len(available_words)}, needed {words_per_length}.")
            # Optionally, take all available words if fewer than required
            final_word_dict[length] = random.sample(available_words, len(available_words)) if available_words else []
            # Or, if you strictly need 7 and can't find them, you might raise an error or return an empty list for that length.
            # For now, we'll take what we can get or an empty list.

    return final_word_dict

if __name__ == "__main__":
    # This part runs only when the script is executed directly
    # Useful for testing the module
    print("Generating word list from TDK source...")
    generated_words = generate_words_by_length_from_url()

    if generated_words:
        print("\nGenerated WORDS_BY_LENGTH structure:")
        for length, words in generated_words.items():
            print(f"{length}: {words}")
        
        print("\nVerifying counts:")
        all_selected_words = []
        for length_category in generated_words.values():
            all_selected_words.extend(length_category)
        print(f"Total words selected: {len(all_selected_words)}")

        # Check if we have 56 words (7 words * 8 categories)
        expected_total = len(TARGET_LENGTHS) * WORDS_PER_LENGTH
        if len(all_selected_words) != expected_total:
             print(f"Warning: Expected {expected_total} words, but got {len(all_selected_words)} due to insufficient words in some categories.")

    else:
        print("Could not generate word list.")