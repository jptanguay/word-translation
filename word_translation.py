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


api_key = st.secrets["api_key"]
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

### Directives supplémentaires

- Ne pas répèter les mots qui ont déjà été traité(e)s
- Fournir seulement le résultat de l'étape #3
- N'écrire aucun commentaire.
- Ne pas oublier que la traduction doit être en français!

Merci

## Texte à analyser
{text}
"""




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
    prompt = st.chat_input("Texte à analyser")
    if prompt:
        st.write(f"Texte envoyé:\n {prompt}")

        #word_types = ", ".join(options)
        #query = template.format(word_type, word_type, word_type, word_type, prompt)
        query = template.replace("{category}", word_type)
        query = query.replace("{text}", prompt)
        con = st.container(border=True)
        con.write(query)

        st.subheader("Résultat")
        s = GetTranslation(query)
        st.text(s)


st.markdown("<hr>", unsafe_allow_html=True)

#st.write(text)



