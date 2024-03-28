import pandas as pd
import re

def remove_contractions(data: pd.DataFrame) -> pd.DataFrame:
    # Define contraction mapping
    contractions_mapping = {
        'I \'m': 'I am', 'I \'ve': 'I have', 'I \'ll': 'I will', 'I \'d': 'I would', 'I \'re': 'I are', 'I \'s': 'I is', 'You \'re': 'You are', 'You \'ve': 'You have',
        'You \'ll': 'You will', 'You \'d': 'You would', 'You \'s': 'You is', 'He \'s': 'He is', 'He \'ll': 'He will', 'He \'d': 'He would', 'She \'s': 'She is',
        'She \'ll': 'She will', 'She \'d': 'She would', 'It \'s': 'It is', 'It \'ll': 'It will', 'It \'d': 'It would', 'We \'re': 'We are', 'We \'ve': 'We have',
        'We \'ll': 'We will', 'We \'d': 'We would', 'We \'s': 'We is', 'They \'re': 'They are', 'They \'ve': 'They have', 'They \'ll': 'They will', 'They \'d': 'They would',
        'They \'s': 'They is', 'Isn \'t': 'Is not', 'Aren \'t': 'Are not', 'Wasn \'t': 'Was not', 'Weren \'t': 'Were not', 'Haven \'t': 'Have not', 'Hasn \'t': 'Has not',
        'Hadn \'t': 'Had not', 'Won \'t': 'Will not', 'Wouldn \'t': 'Would not', 'Don \'t': 'Do not', 'Doesn \'t': 'Does not', 'Didn \'t': 'Did not', 'Can \'t': 'Can not',
        'Couldn \'t': 'Could not', 'Shouldn \'t': 'Should not', 'Mightn \'t': 'Might not', 'Mustn \'t': 'Must not', 'Would \'ve': 'Would have', 'Should \'ve': 'Should have',
        'Let \'s': 'Let us', 'That \'s': 'That is', 'Who \'s': 'Who is', 'What \'s': 'What is', 'Here \'s': 'Here is', 'There \'s': 'There is', 'When \'s': 'When is',
        'How \'s': 'How is', 'Why \'s': 'Why is', 'That \'d': 'That would', 'Who \'d': 'Who would', 'What \'d': 'What would', 'Where \'d': 'Where would', 'How \'d': 'How would',
        'That \'ll': 'That will', 'Ca n\'t': 'Can not', 'Wo n\'t': 'Will not', 'N\'t': 'not',
    }

    # Add the lower case version of the keys to the mapping
    for key in list(contractions_mapping.keys()):
        contractions_mapping[key.lower()] = contractions_mapping[key].lower()

    data_no_contractions = data.copy()

    # We replace the contractions
    for k, v in contractions_mapping.items():
        data_no_contractions['text'] = data_no_contractions['text'].str.replace(k, v)

    return data_no_contractions


def remove_h_tags(data: pd.DataFrame) -> pd.DataFrame:
    # Remove <h> tags
    data_no_h = data.copy()
    data_no_h['text'] = data_no_h['text'].str.replace('<h>', '')
    
    return data_no_h


def remove_mentions(data: pd.DataFrame) -> pd.DataFrame:
    data_no_mentions = data.copy()

    # We replace the mentions starting with @ until the next space with an empty string
    to_replace = []
    for index in range(len(data_no_mentions['text'].tolist())):
        if '@' in data_no_mentions['text'].tolist()[index][:5]:
            data_no_mentions.at[index, 'text'] = re.sub(r'@([[a-z]|[A-Z]|[1-9]|0])+\s', '', data_no_mentions['text'][index][:5])

    # Replace @ surrounded by spaces with an empty string
    data_no_mentions['text'] = data_no_mentions['text'].str.replace(' @ ', '')

    # Replace @ at the end of the text with an empty string
    for index in range(len(data_no_mentions['text'].tolist())):
        if '@' in data_no_mentions['text'].tolist()[index][-5:]:
            data_no_mentions.at[index, 'text'] = re.sub(r'@', '', data_no_mentions['text'][index])

    return data_no_mentions


def remove_multiple_quotations(data: pd.DataFrame) -> pd.DataFrame:
    # Remove multiple consecutive " characters
    data_no_quotes = data.copy()

    # We replace the multiple consecutive " characters with a single "
    for index in range(len(data_no_quotes['text'].tolist())):
        data_no_quotes.at[index, 'text'] = re.sub(r'["]+', '"', data_no_quotes['text'][index])

    # We do the same for the ' character
    for index in range(len(data_no_quotes['text'].tolist())):
        data_no_quotes.at[index, 'text'] = re.sub(r'[\']+', '\'', data_no_quotes['text'][index])

    return data_no_quotes


def remove_ampersands(data: pd.DataFrame) -> pd.DataFrame:
    data_processed_amps = data.copy()

    # Remove More&gt;&gt;
    data_processed_amps['text'] = data_processed_amps['text'].str.replace(' More&gt;&gt;', '')

    # Replace &amp; with &
    data_processed_amps['text'] = data_processed_amps['text'].str.replace('&amp;', '&')

    # Replace &gt; with <, &lt; with > and &quot; with "
    data_processed_amps['text'] = data_processed_amps['text'].str.replace('&gt;', '>')
    data_processed_amps['text'] = data_processed_amps['text'].str.replace('&lt;', '<')
    data_processed_amps['text'] = data_processed_amps['text'].str.replace('&quot;', '"')

    return data_processed_amps


def lowercase(data: pd.DataFrame) -> pd.DataFrame:
    data_lower = data.copy()
    data_lower['text'] = data_lower['text'].str.lower()
    return data_lower


def remove_extra_spaces(data: pd.DataFrame) -> pd.DataFrame:
    data_no_spaces = data.copy()

    # We replace the multiple consecutive spaces with a single space
    for index in range(len(data_no_spaces['text'].tolist())):
        data_no_spaces.at[index, 'text'] = re.sub(r'[ ]+', ' ', data_no_spaces['text'][index])

    # We remove the spaces at the beginning and end of the text
    for index in range(len(data_no_spaces['text'].tolist())):
        if data_no_spaces['text'][index].startswith(' '):
            data_no_spaces.at[index, 'text'] = data_no_spaces['text'][index][1:]
        if data_no_spaces['text'][index].endswith(' '):
            data_no_spaces.at[index, 'text'] = data_no_spaces['text'][index][:-1]
        index -= 1

    return data_no_spaces