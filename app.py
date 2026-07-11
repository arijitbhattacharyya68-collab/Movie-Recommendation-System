import streamlit as st
import pickle
import pandas as pd
import requests
import time

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)
st.markdown("""
<style>

/* Main background */
.stApp{
    background-color:#141414;
}

/* Main title */
h1{
    color:white;
    text-align:center;
}

/* Markdown text */
h2,h3,h4,h5,p{
    color:white;
}

/* Sidebar */
[data-testid="stSidebar"]{
    background-color:#000000;
}

/* Button */
.stButton>button{
    background-color:#E50914;
    color:white;
    border:none;
    border-radius:10px;
    height:50px;
    font-size:20px;
    font-weight:bold;
}

.stButton>button:hover{
    background-color:#B20710;
}

/* Select Box */
[data-baseweb="select"]{
    color:black;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
st.sidebar.title("🎬 Movie Recommendation")

st.sidebar.markdown("""
### 🤖 AI Powered Recommendation System

### Technologies Used

- Python
- Streamlit
- Pandas
- Scikit-Learn
- TMDB API

### Machine Learning

- NLP
- CountVectorizer
- Cosine Similarity
""")

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
movies_dict = pickle.load(open("movies.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))

# -------------------------------------------------
# FETCH MOVIE DETAILS
# -------------------------------------------------
def fetch_movie_details(movie_id):

    api_key = st.secrets["TMDB_API_KEY"]

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"

    response = requests.get(url)

    if response.status_code != 200:

        return {
            "poster":None,
            "rating":"N/A",
            "release":"N/A",
            "overview":"No Overview Available",
            "language":"N/A",
            "runtime":"N/A",
            "popularity":"N/A",
            "genres":"N/A"
        }

    data=response.json()

    poster=None

    if data.get("poster_path"):
        poster="https://image.tmdb.org/t/p/w500"+data["poster_path"]

    genres="N/A"

    if data.get("genres"):
        genres=", ".join([g["name"] for g in data["genres"]])

    return{

        "poster":poster,

        "rating":data.get("vote_average","N/A"),

        "release":data.get("release_date","N/A"),

        "overview":data.get("overview","No Overview Available"),

        "language":data.get("original_language","N/A").upper(),

        "runtime":data.get("runtime","N/A"),

        "popularity":round(data.get("popularity",0),2),

        "genres":genres

    }
# -------------------------------------------------
# FETCH TRAILER
# -------------------------------------------------
def fetch_trailer(movie_id):

    api_key = st.secrets["TMDB_API_KEY"]

    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={api_key}&language=en-US"

    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    for video in data.get("results", []):

        if video["site"] == "YouTube" and video["type"] == "Trailer":

            return f"https://www.youtube.com/watch?v={video['key']}"

    return None
# -------------------------------------------------
# RECOMMEND FUNCTION
# -------------------------------------------------
def recommend(movie):

    movie_index = movies[movies["title"] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_details = []
    recommended_trailers = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]]["id"]

        recommended_movies.append(
            movies.iloc[i[0]]["title"]
        )

        recommended_details.append(
            fetch_movie_details(movie_id)
        )

        recommended_trailers.append(
            fetch_trailer(movie_id)
        )

    return recommended_movies, recommended_details, recommended_trailers

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown("""
<div style="
background: linear-gradient(90deg,#000000,#141414,#1f1f1f);
padding:35px;
border-radius:15px;
text-align:center;
">

<h1 style="color:#E50914;font-size:55px;">
🎬 Movie Recommendation System
</h1>

<h3 style="color:white;">
Discover Movies You'll Love with Artificial Intelligence
</h3>

<p style="color:#bbbbbb;font-size:18px;">
Content-Based Recommendation • NLP • Cosine Similarity • TMDB API
</p>

</div>
""", unsafe_allow_html=True)

st.write("")

# -------------------------------------------------
# SELECT MOVIE
# -------------------------------------------------
st.subheader("🎥 Choose Your Favourite Movie")

selected_movie = st.selectbox(
    "",
    movies["title"].values,
    index=0
)

# -------------------------------------------------
# BUTTON
# -------------------------------------------------
recommend_button = st.button(
    "🚀 Recommend Movies",
    use_container_width=True
)

# -------------------------------------------------
# SHOW RECOMMENDATIONS
# -------------------------------------------------
if recommend_button:

    with st.spinner("🍿 AI is searching for similar movies..."):

        time.sleep(1)

        names, details, trailers = recommend(selected_movie)
        st.balloons()

    st.success("🍿 Here are your recommendations!")

    st.markdown(
        """
        ## 🎥 Recommended Movies
        """
    )

    st.markdown("---")

    cols = st.columns(5)

    for i in range(5):

        with cols[i]:

            if details[i]["poster"]:
                st.image(
                    details[i]["poster"],
                    use_container_width=True
                )

            st.markdown(
                f"""
                <h4 style='text-align:center;color:white;'>
                🎬 {names[i]}
                </h4>
                """,
                unsafe_allow_html=True
            )

            st.markdown(f"⭐ **Rating:** {details[i]['rating']}")

            st.markdown(f"📅 **Release:** {details[i]['release']}")

            st.markdown(f"🌍 **Language:** {details[i]['language']}")

            st.markdown(f"🎭 **Genre:** {details[i]['genres']}")

            st.markdown(f"🔥 **Popularity:** {details[i]['popularity']}")

            st.markdown(f"⏱ **Runtime:** {details[i]['runtime']} min")

            overview = details[i]["overview"]

            if len(overview) > 120:
                overview = overview[:120] + "..."

            st.caption(overview)
            if trailers[i]:
                st.link_button(
                    "▶ Watch Trailer",
                    trailers[i],
                    use_container_width=True
                )
st.markdown("---")

st.caption("Powered by Streamlit • TMDB API • Scikit-Learn")