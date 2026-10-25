import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

MODEL = "gemini-3.8-flash"


@st.cache_resource
def get_client():
    return genai.Client()


def build_prompt(ingredients, cuisine, diet, max_words, servings, notes):
    prompt = f'''
Generate one food recipe using these ingredients: {', '.join(ingredients)}
Cuisine: {cuisine}
Diet: {diet}
Servings: {servings}
Recipe should not be more than {max_words} words.
Format it in markdown with a title, an ingredients list and numbered steps.
'''
    if notes:
        prompt += f"Extra instructions: {notes}\n"
    return prompt


st.set_page_config(page_title="Recipe Generator", page_icon="🍳")
st.title("🍳 Recipe Generator")
st.caption(f"Powered by {MODEL}")

ingredients_text = st.text_area(
    "Ingredients (comma separated)",
    value="spinach, paneer, onions, ghee, masala's",
)

col1, col2 = st.columns(2)
with col1:
    cuisine = st.selectbox(
        "Cuisine",
        ["Indian", "Italian", "Chinese", "Mexican", "Thai", "Japanese", "Mediterranean", "American", "Any"],
    )
    servings = st.number_input("Servings", min_value=1, max_value=12, value=2)
with col2:
    diet = st.selectbox(
        "Diet",
        ["Vegetarian", "Vegan", "Non-Vegetarian", "Eggetarian", "Keto", "Gluten-Free", "Any"],
    )
    max_words = st.slider("Max words", min_value=30, max_value=500, value=150, step=10)

notes = st.text_input("Anything else? (optional)", placeholder="e.g. quick, under 20 minutes, less spicy")

if st.button("Generate recipe", type="primary"):
    ingredients = [i.strip() for i in ingredients_text.split(",") if i.strip()]
    if not ingredients:
        st.warning("Please enter at least one ingredient.")
    else:
        prompt = build_prompt(ingredients, cuisine, diet, max_words, servings, notes)
        with st.spinner("Cooking up a recipe..."):
            try:
                interaction = get_client().interactions.create(model=MODEL, input=prompt)
                st.markdown(interaction.output_text)
            except Exception as e:
                st.error(f"Failed to generate recipe: {e}")
