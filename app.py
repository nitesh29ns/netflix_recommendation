from flask import Flask, request
from flask import send_file, abort, render_template

from netflix.component.recommendation import Recommendation
from netflix.component.NLP_recommendation import similar_recommendation, recommendation

GENRE_KEY = "genre"
MESSAGE_KEY = "output"
MOVIE_1 = "movie_1"
MOVIE_2 = "movie_2"
MOVIE_3 = "movie_3"
MOVIE_4 = "movie_4"
MOVIE_5 = "movie_5"
INVALID = "invalid"

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')


@app.route('/genre_based', methods=['GET', 'POST'])
def genre_based():
    context = {
        INVALID : None,
        GENRE_KEY : None,
        MESSAGE_KEY : None,
        MOVIE_1 : None,
        MOVIE_2 : None,
        MOVIE_3 : None,
        MOVIE_4 : None,
        MOVIE_5 : None
    }
    
    if request.method == "POST":
        type = str(request.form['type'])
        genre = str(request.form['genre'])
        re = Recommendation(type)
        output = re.recommendation(genre) ###re.recommendation(genre)  ## output to be used in html
        context = {
            INVALID : output.message,
            GENRE_KEY : type,
            MESSAGE_KEY : output.message,
            MOVIE_1 : output.recom_1,
            MOVIE_2 : output.recom_2,
            MOVIE_3 : output.recom_3,
            MOVIE_4 : output.recom_4,
            MOVIE_5 : output.recom_5
            }
        return render_template('genre_based.html', context=context)
    return render_template('genre_based.html', context=context)


@app.route('/similar', methods=['GET', 'POST'])
def similar():
    context = {
        INVALID : None,
        GENRE_KEY : None,
        MESSAGE_KEY : None,
        MOVIE_1 : None,
        MOVIE_2 : None,
        MOVIE_3 : None,
        MOVIE_4 : None,
        MOVIE_5 : None,
    }

    if request.method == 'POST':
        type = str(request.form['type']) # 'type' come from name="type" from html file
        movie = str(request.form['movie_name']) # 'movie_name' come from name="movie_name" from html file
        test = similar_recommendation(type) 
        output = test.recommend(movie)
        context = {
                INVALID : output.message,
                GENRE_KEY : type,
                MESSAGE_KEY : output.message,
                MOVIE_1 : output.recom_1,
                MOVIE_2 : output.recom_2,
                MOVIE_3 : output.recom_3,
                MOVIE_4 : output.recom_4,
                MOVIE_5 : output.recom_5
        }
        return render_template('similar.html', context=context)
    return render_template('similar.html', context=context)



if __name__ == "__main__":
    app.run()