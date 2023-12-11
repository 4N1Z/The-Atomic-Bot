import streamlit as st
import cohere

import random
import time
co = cohere.Client(st.secrets["COHERE_API_KEY"])
# Streamlit header
st.set_page_config(page_title="Co:Chat - An LLM-powered chat bot")
st.title("The Atomic Bot")


preamble_prompt = """You are a AI assistant of "The Atomic Workspace" located at Trivandrum. You will answer any queries related to the hotel.ALWAYS BE POLIETE You should always through out the conversation act accordingly. Take note that, you have been provided with documents and citations, 'documents:'. Do not speak outside this context.
You should help customers to book rooms at the Atomic. Gather all the necessary information such as name, date of check-in and check-out, number of people, type of room, and any extras they may want to add to their stay. 
Ask these questions one after another. DO NOT ASK EVERYTHING AT ONCE. Get the information one at a time.
Finally when it is time to book, ask the customer to confirm the booking. If they say yes, then confirm the booking by displaying the booking details back to them in a formatted way. If they say no, then cancel the booking and start over.
If you don't know the answer to any query, just say you don't know. DO NOT try to make up an answer.
If the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context."""


docs = [
    {
        "title": "The Atomic Workspace",
        "snippet": "The Atomic workspace, a shared, flexible, and convenient working space for individuals, teams, and enterprises aiming to foster innovation through collaboration and creativity.",
        "image": "https://theatomic.space/img/hero.jpg"
    },
    {
        "title": "Space1 - Private Desk",
        "snippet": "Do great work together. Ideal for teams and enterprises requiring a convenient and secure workspace to spark ideas and start conversations.",
        "image": "https://theatomic.space/img/private-desk.jpg"
    },
    {
        "title": "Space2 -  Events",
        "snippet": "Our spaces are open to public bookings throughout the year. Anything from board meetings to seminars to get-togethers can be organized conveniently.",
        "image": "https://theatomic.space/img/events.jpg"
    },
    {
        "title": "Space3 - Hot Desk",
        "snippet": "Perfect for the modern-day nomad - flexible and at your convenience. Find your desk, plug in, and take the new world of work one day at a time.",
        "image": "https://theatomic.space/img/hot-desk.jpg"
    },
    {
        "title": "Space4 - Dedicated Desk",
        "snippet": "Designed for those who require more gear to get the job done. Do your own thing while being part of The Atomic's diverse community.",
        "image": "https://theatomic.space/img/dedicated-desk.jpg"
    },
    {
        "title": "Space5 - Private Desk",
        "snippet": "Do great work together. Ideal for teams and enterprises requiring a convenient and secure workspace to spark ideas and start conversations.",
        "image": "https://theatomic.space/img/private-desk.jpg"
    },
    {
        "title": "What We Believe - Our Motto",
        "snippet": "Be surrounded by interesting people doing interesting things. We believe people can be more together. We empower members to think creatively as individuals all the while drawing from and building upon the surrounding community.",
    },
    {
        "title": "CONFIRM BOOKING",
        "snippet": "Give The summary of the booking details so far",
        "Url": "Also if confirm booking show this link https://bento.me/aniz",
        "message": "Summarize the conversation so far and ask for confirmation"
    },

]


def cohereReply(prompt):

    # Extract unique roles using a set
    unique_roles = set(item['role'] for item in st.session_state.messages)

    if {'USER', 'assistant'} <= unique_roles:
        # st.write("INITIAL_________________")
        llm_response = co.chat(
            message=prompt,
            documents=docs,
            model='command',
            preamble_override=preamble_prompt,
            chat_history=st.session_state.messages,
        )
    else:

        llm_response = co.chat(
            message=prompt,
            documents=docs,
            model='command',
            preamble_override=preamble_prompt,

        )

    print(llm_response)
    return llm_response.text


def initiailize_state():
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []


def main():

    initiailize_state()
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["message"])

    # React to user input
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        st.chat_message("USER").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "USER", "message": prompt})
        # print(st.session_state.messages)

        llm_reponse = cohereReply(prompt)
        with st.chat_message("assistant"):
            st.markdown(llm_reponse)
        st.session_state.messages.append(
            {"role": "assistant", "message": llm_reponse})
  
 


if __name__ == "__main__":
    main()
