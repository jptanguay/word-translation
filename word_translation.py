'''

    extraire des mots d'un texte grec, et fournir la traduction
    formaté pour être utilisable dans learn.tcl

'''

import os

from mistralai import Mistral, UserMessage
import streamlit as st


############################
# config
############################
st.set_option('client.showErrorDetails', False)


try:
    api_key = st.secrets["api_key"]
except FileNotFoundError:
    st.error('Using environment')
    api_key = os.environ["api_key"]

    
model = "mistral-small-latest"

client = Mistral(api_key=api_key)


template = """
## Directives
### Étape #1
À partir du "texte à analyser" présenté plus bas,
établir une liste des mots avec leur fonction sytaxique.
Ex.:
- Die: article,
- globale: adjectif
- estar: verbe
- table: nom

### Étape #2
En utilisant cette liste, extraire tous les mots
dont la fonction syntaxique est {category}.

### Étape #3

En utilisant la liste de mots extraits à l'étape #2,
Pour chaque mot de cette liste écrire une ligne comprenant
le mot dans langue originale du texte et la traduction française,
en suivant ce format: "mot;traduction;0;0"

### Étape 4

Ne pas répèter les lignes identiques;
enlever les doublons de la liste produite à l'étape #3

### Directives supplémentaires
- N'écrire aucun commentaire.
- Ne pas oublier que la traduction doit être en français!

Merci

## Texte à analyser
{text}
"""

# - Fournir seulement le résultat de l'étape #3


############################
# fonctions
############################

def GetTranslation(prompt, model="mistral-small-latest"):    
    messages = [
        {
            "role": "user",
            "content": prompt,
        },
    ]
    # Or using the new message classes
    # messages = [
    #     UserMessage(content="What is the best French cheese?"),
    # ]

    chat_response = client.chat.complete(
        model=model,
        messages=messages,
    )
    return chat_response.choices[0].message.content


############################
# MAIN
############################
text = """
Τα πλεονεκτήματα που έχουν στην υγεία τα εναλλακτικά προϊόντα καπνού, σε σύγκριση με το τσιγάρο και τη βοήθεια που μπορούν να προσφέρουν στην πλήρη διακοπή πρόσληψης νικοτίνης, ανέφεραν μεταξύ άλλων ειδικοί στο πλαίσιο του 7ου επιστημονικού συνεδρίου για τη Μείωση της Βλάβης από τον Καπνό με τίτλο «Τι χρειάζεται για να αναδειχθούν τα οφέλη της στρατηγικής Μείωσης της Βλάβης;».
"""

st.title("Extraction de mots")

st.header("Utilise Mistral.small pour extraire des mots et fournir les traductions")

con1 = st.container()
with con1:
    word_type = st.radio(
        "Types de mots",
        ["nom", "adjectif", "verbe", "adverbe", "conjonction", "pronom", "préposition"],
        horizontal=True
    )
    c1, c2 = st.columns(2)
    with c1:
        show_query = st.checkbox("Afficher la requête?")
    with c2:
        show_all_steps = st.checkbox("Afficher toutes les étapes de la réponse ?")
        
    prompt = st.chat_input("Texte à analyser")
    if prompt:
        st.write(f"### Texte envoyé")
        st.write(prompt)

        #word_types = ", ".join(options)
        #query = template.format(word_type, word_type, word_type, word_type, prompt)
        query = template.replace("{category}", word_type)
        query = query.replace("{text}", prompt)

        if show_query:
            con = st.container(border=True)
            con.write(query)

        st.subheader("Résultat")
        
        #with st.spinner('En cours...'):
        result = GetTranslation(query)

        if show_all_steps:
            s = result
        else:
            s = result.split("Étape #4",1)[1]
        
        st.text(s)

        #st.text_area("Résultat", value=s)

st.markdown("<hr>", unsafe_allow_html=True)

#st.write(text)



