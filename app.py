import requests, random, re, schedule, time
from credentials import mobile_number, api_key
from flask import Flask
app = Flask(__name__)


#@app.route('/dict')
def getWord(inputWord):
    url = f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{inputWord}?key={api_key}'

    try:
        # Make a GET request to the API endpoint
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract a random word from the response
            if data:
                return data[0]['shortdef'][0]
                #[0]['def'][0]['sseq'][0][0][1]['dt'][0][1]
        else:
            print(f"Error: {response.status_code} - {response.reason}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None





def sendText():

    term = generate_random_word()
    definition = getWord(term)
    resp = requests.post('https://textbelt.com/text', {
    'phone': mobile_number,
    'message': "Daily Word Is..\n\n' " + term + " '\n\nDefinition: ' " + definition + " '",
    'key': 'textbelt',
    })
    print(resp.json())




def generate_random_word():
    file_path = '/Users/matthew/Downloads/dictionary.txt'
    selected_words = []

    # Read words from file
    with open(file_path, 'r') as f:
        words = f.readlines()
    
    # Remove leading/trailing whitespace and newline characters
    words = [word.strip() for word in words]
    
    # Check if all words have been selected
    if len(selected_words) == len(words):
        print("All words have been selected.")
        return None

    # Select a random word that hasn't been selected yet
    while True:
        random_word = random.choice(words)
        if random_word not in selected_words:
            selected_words.append(random_word)
            break

    # Write remaining words back to file
    with open(file_path, 'w') as f:
        for word in words:
            if word != random_word:
                f.write(word + '\n')

    return random_word


schedule.every().day.at('09:00').do(sendText)

#print(generate_random_word())



while True:
    schedule.run_pending()
    time.sleep(1)

# if __name__ == '__main__':
#     app.run(debug=True)

