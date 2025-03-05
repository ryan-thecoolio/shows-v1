from flask import Flask, render_template, request
import requests

app = Flask(__name__)
apikey = "ENTER API KEY 🤫"

def get_info(title):
    url = f"http://www.omdbapi.com/?apikey={apikey}&t={title}"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        if data.get("Response") == "True":  # Check if valid data is returned
            return data
        else:
            return {"Title": "No results found"}  #Sets result.Title = "No results found"
    else:
        print("2")
        return {"Title": f"Error: {r.status_code}"}  # Handle API errors

# def get_dog_placeholder():
#     url = 'https://dog.ceo/api/breeds/image/random'
#     r = requests.get(url)
#     data = (r.json())['message']
#     return data
# DOGS!!!!

def get_actor_images(list, title):
    google_apikey = 'ENTER API KEY 🤫'
    search_engine_id = 'ENTER SEARCH ENGINE ID 🤫'
    actor_list = {}
    for actor in list:
        actor_list[actor] = ''
    for actor in (actor_list.keys()):
        item = f'{actor} in {title}'
        search_query = item

        url = 'https://www.googleapis.com/customsearch/v1'
        params = {
            'q': search_query,
            'key': google_apikey,
            'cx': search_engine_id,
            'searchType': 'image',
        }
        r = requests.get(url, params=params)
        data = r.json()
        if 'items' in data:
            actor_list[actor] = (data['items'][0]['link'])
    return actor_list


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None  # Ensure no default invalid message
    # placeholder = None
    images = {}
    if request.method == 'POST':
        title = request.form.get('input', '').strip()
        if title:
            result = get_info(title)
            actors_list = [actor.strip() for actor in result['Actors'].split(',')]
            images = get_actor_images(actors_list, title)
            # placeholder = get_dog_placeholder()
    return render_template('index.html', result=result, images=images)

if __name__ == "__main__":
    app.run(debug=True)
