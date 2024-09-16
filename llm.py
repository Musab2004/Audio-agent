import os
import time
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)

store = {}


def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


class LLM:
    def _setup_chain(self):
        SYSTEM_MESSAGE = (
            "system",
            """ You are a human and you are in a conversation. Answer like a normal human being. your'e a female""",
        )
        HUMAN_MESSAGE = ("human", """{query}""")

        prompt = ChatPromptTemplate.from_messages(
            [
                SYSTEM_MESSAGE,
                MessagesPlaceholder(variable_name="history"),
                HUMAN_MESSAGE,
            ]
        )
        runnable = prompt | self.llm | StrOutputParser()
        chain = RunnableWithMessageHistory(
            runnable,
            get_session_history,
            input_messages_key="query",
            history_messages_key="history",
        )
        return chain

    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            model_name="llama-3.1-8b-instant",
            groq_api_key=os.getenv("GROQ_API_KEY"),
        )
        self.chain = self._setup_chain()

    def process(self, text):
        start_time = time.time()

        # Go get the response from the LLM
        response = self.chain.invoke(
            {"query": text}, config={"configurable": {"session_id": "abc123"}}
        )
        end_time = time.time()

        elapsed_time = int((end_time - start_time) * 1000)
        print(f"AI :  ({elapsed_time}ms): {response}")
        return response


# if __name__ == "__main__":
#     chat = LLM()
#     print(chat.process("How are you ? , My name is Aqib "))
#     print(chat.process("what is my name btw ?"))
