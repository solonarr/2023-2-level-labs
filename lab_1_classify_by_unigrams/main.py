"""
Lab 1
Language detection
"""
import json


def tokenize(text: str) -> list[str] | None:
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation, digits and other symbols
    :param text: a text
    :return: a list of lower-cased tokens without punctuation
    """
    if not isinstance(text, str):
        return None
    punc = ''''1234567890!"#$%&'()’*º+,-./:;<=>?@[\\]^_`{|}~'''
    text = text.replace(' ', '')
    text = text.replace('\n', '')
    return [token.lower() for token in text if token not in punc]


def calculate_frequencies(tokens: list[str] | None) -> dict[str, float] | None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    if not isinstance(tokens, list):
        return None
    for token in tokens:
        if not isinstance(token, str):
            return None
    return {token: tokens.count(token) / len(tokens) for token in tokens}


def create_language_profile(language: str, text: str) -> dict[str, str | dict[str, float]] | None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :return: a dictionary with two keys – name, freq
    """
    if not (isinstance(language, str) and isinstance(text, str)):
        return None
    text_to_proceed = tokenize(text)
    prof_dict = calculate_frequencies(text_to_proceed)
    if not prof_dict:
        return None
    return {"name": language, "freq": prof_dict}


def calculate_mse(predicted: list, actual: list) -> float | None:
    """
    Calculates mean squared error between predicted and actual values
    :param predicted: a list of predicted values
    :param actual: a list of actual values
    :return: the score
    """
    if not (isinstance(predicted, list)
            and isinstance(actual, list)
            and len(predicted) == len(actual)):
        return None
    mse_calculation = 0
    for num, act in enumerate(actual):
        mse_calculation += (act - predicted[num])**2
    return mse_calculation / len(actual)


def compare_profiles(
        unknown_profile: dict[str, str | dict[str, float]],
        profile_to_compare: dict[str, str | dict[str, float]]
) -> float | None:
    """
    Compares profiles and calculates the distance using symbols
    :param unknown_profile: a dictionary of an unknown profile
    :param profile_to_compare: a dictionary of a profile to compare the unknown profile to
    :return: the distance between the profiles
    """
    if not (isinstance(unknown_profile, dict)
            and isinstance(profile_to_compare, dict)
            and 'name' in unknown_profile
            and 'freq' in unknown_profile
            and 'name' in profile_to_compare
            and 'freq' in profile_to_compare):
        return None
    unknown_tokens = set(unknown_profile.get('freq').keys())
    compare_tokens = set(profile_to_compare.get('freq').keys())
    all_tokens = list(unknown_tokens | compare_tokens)
    list_actual = []
    list_predicted = []
    for token in all_tokens:
        if token not in unknown_profile["freq"]:
            list_actual.append(float(0))
            list_predicted.append(float(profile_to_compare['freq'][token]))
        elif token not in profile_to_compare['freq']:
            list_actual.append(float(unknown_profile["freq"][token]))
            list_predicted.append(float(0))
        else:
            list_actual.append(float(unknown_profile["freq"][token]))
            list_predicted.append(float(profile_to_compare['freq'][token]))
    return calculate_mse(list_predicted, list_actual)


def detect_language(
        unknown_profile: dict[str, str | dict[str, float]],
        profile_1: dict[str, str | dict[str, float]],
        profile_2: dict[str, str | dict[str, float]],
) -> str | None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary of a profile to determine the language of
    :param profile_1: a dictionary of a known profile
    :param profile_2: a dictionary of a known profile
    :return: a language
    """
    if not (isinstance(unknown_profile, dict)
            and isinstance(profile_1, dict)
            and isinstance(profile_2, dict)):
        return None
    unknown_and_1 = compare_profiles(unknown_profile, profile_1)
    unknown_and_2 = compare_profiles(unknown_profile, profile_2)
    if (isinstance(unknown_and_1, float)
            and isinstance(unknown_and_2, float)):
        if unknown_and_1 < unknown_and_2:
            return str(profile_1['name'])
        if unknown_and_2 < unknown_and_1:
            return str(profile_2['name'])
    detected = sorted([str(profile_1.get('name')), str(profile_2.get('name'))])[0]
    return detected


def load_profile(path_to_file: str) -> dict | None:
    """
    Loads a language profile
    :param path_to_file: a path to the language profile
    :return: a dictionary with at least two keys – name, freq
    """
    if not isinstance(path_to_file, str):
        return None
    with open(path_to_file, 'r', encoding='utf-8') as json_to_read:
        json_file = json.load(json_to_read)
    if not isinstance(json_file, dict):
        return None
    return json_file


def preprocess_profile(profile: dict) -> dict[str, str | dict] | None:
    """
    Preprocesses profile for a loaded language
    :param profile: a loaded profile
    :return: a dict with a lower-cased loaded profile
    with relative frequencies without unnecessary ngrams
    """
    if not (isinstance(profile, dict)
            and 'name' in profile
            and 'freq' in profile
            and 'n_words' in profile):
        return None
    freq_dict = {}
    for unigram in profile['freq']:
        if unigram.lower() in freq_dict:
            freq_dict[unigram.lower()] += int(profile['freq'][unigram]) / int(profile['n_words'][0])
        elif len(unigram) == 1:
            freq_dict[unigram.lower()] = int(profile['freq'][unigram]) / int(profile['n_words'][0])
    return {'name': profile['name'], 'freq': freq_dict}


def collect_profiles(paths_to_profiles: list) -> list[dict[str, str | dict[str, float]]] | None:
    """
    Collects profiles for a given path
    :paths_to_profiles: a list of strings to the profiles
    :return: a list of loaded profiles
    """


def detect_language_advanced(unknown_profile: dict[str, str | dict[str, float]],
                             known_profiles: list) -> list | None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary of a profile to determine the language of
    :param known_profiles: a list of known profiles
    :return: a sorted list of tuples containing a language and a distance
    """


def print_report(detections: list[tuple[str, float]]) -> None:
    """
    Prints report for detection of language
    :param detections: a list with distances for each available language
    """
