from langgraph.graph import StateGraph, END
from services.graph.chat_state import ChatState
from services.graph.nodes.product_retriever import product_retriever_node
from services.graph.nodes.llm_node import llm_node
from services.graph.nodes.twilio_sender import twilio_sender_node

workflow = StateGraph(ChatState)

workflow.add_node("retriever", product_retriever_node)
workflow.add_node("llm", llm_node)
workflow.add_node("sender", twilio_sender_node)

workflow.set_entry_point("retriever")
workflow.add_edge("retriever", "llm")
workflow.add_edge("llm", "sender")
workflow.add_edge("sender", END)

app = workflow.compile()