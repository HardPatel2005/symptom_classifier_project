# classifier_app/views.py

from django.shortcuts import render
from django.http import HttpRequest
from .forms import SymptomForm
from .models import SymptomEntry
import os
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# --- Global LLM Initialization (for efficiency) ---
llm = None
try:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0, google_api_key=api_key)
    print("Gemini LLM initialized successfully for Django app.")
except Exception as e:
    print(f"Error initializing Gemini LLM for Django app: {e}")
    print("Please ensure GOOGLE_API_KEY is set as an environment variable.")

# --- Define the AgentState for LangGraph ---
class AgentState(TypedDict):
    symptom: str
    classification: str
    messages: Annotated[list, add_messages]

# --- LangGraph Node Definitions ---
def get_symptom_initial_state(symptom_text: str) -> AgentState:
    return {"symptom": symptom_text, "messages": [HumanMessage(content=symptom_text)]}

def classify_symptom(state: AgentState) -> AgentState:
    symptom = state.get("symptom")
    if not symptom:
        return {"classification": "unknown", "messages": [HumanMessage(content="Error: Symptom missing for classification.")]}

    prompt_text = f"""
    You are a helpful medical assistant. Classify the following symptom into one of these broad categories:
    Emergency, Mental Issue, General.

    Symptom: "{symptom}"

    Provide only the category name (e.g., "Emergency", "Mental Issue", "General").
    Example:
    Input: I have a fever and cough.
    Output: General
    """

    if llm is None:
        return {"classification": "error_llm_not_initialized", "messages": [HumanMessage(content="Error: LLM not available.")]}

    try:
        response = llm.invoke(prompt_text)
        classification = response.content.strip().lower()

        if "emergency" in classification:
            classification = "emergency"
        elif "mental issue" in classification or "mental" in classification:
            classification = "mental_issue"
        elif "general" in classification:
            classification = "general"
        else:
            classification = "unknown"
        
        return {"classification": classification, "messages": [HumanMessage(content=f"Symptom classified as: {classification.upper()}.")]}

    except Exception as e:
        return {"classification": "error", "messages": [HumanMessage(content="Error during symptom classification.")]}

def router(state: AgentState) -> str:
    classification = state.get("classification")

    if classification == "emergency":
        return "emergency_node"
    elif classification == "mental_issue":
        return "mental_issue_node"
    elif classification == "general":
        return "general_node"
    else:
        return "general_node"

def emergency_node(state: AgentState) -> AgentState:
    return {"messages": [HumanMessage(content="Immediate medical attention required. Please call emergency services or visit the nearest hospital.")]}

def mental_issue_node(state: AgentState) -> AgentState:
    return {"messages": [HumanMessage(content="We recommend seeking professional mental health support. Here are some resources for mental well-being: [Link to resources]")]}

def general_node(state: AgentState) -> AgentState:
    return {"messages": [HumanMessage(content="Please provide more details or consult a general practitioner for further assessment of your symptom.")]}

# --- Build and Compile the LangGraph Workflow (once globally) ---
hospital_chatbot = None
try:
    workflow = StateGraph(AgentState)
    workflow.add_node("classify_symptom", classify_symptom)
    workflow.add_node("emergency_node", emergency_node)
    workflow.add_node("mental_issue_node", mental_issue_node)
    workflow.add_node("general_node", general_node)

    workflow.set_entry_point("classify_symptom")

    workflow.add_conditional_edges(
        "classify_symptom",
        router,
        {
            "emergency_node": "emergency_node",
            "mental_issue_node": "mental_issue_node",
            "general_node": "general_node",
        }
    )

    workflow.add_edge("emergency_node", END)
    workflow.add_edge("mental_issue_node", END)
    workflow.add_edge("general_node", END)

    hospital_chatbot = workflow.compile()
    print("LangGraph workflow compiled successfully for Django app.")
except Exception as e:
    print(f"Error compiling LangGraph workflow for Django app: {e}")

# --- Django View Function ---
def symptom_classifier_view(request: HttpRequest):
    form = SymptomForm()
    symptom_text = None
    classification = None
    response_message = None
    conversation_messages = []
    error_message = None

    if request.method == 'POST':
        form = SymptomForm(request.POST)
        if form.is_valid():
            symptom_text = form.cleaned_data['symptom_text']

            if hospital_chatbot is None:
                error_message = "Symptom classifier backend not initialized. Check server logs for API key or graph compilation errors."
            else:
                try:
                    initial_state = get_symptom_initial_state(symptom_text)
                    final_state = hospital_chatbot.invoke(initial_state)

                    classification = final_state.get('classification', 'N/A')
                    messages = final_state.get('messages', [])
                    if messages:
                        response_message = messages[-1].content
                        conversation_messages = [f"{msg.type.capitalize()}: {msg.content}" for msg in messages]
                    else:
                        response_message = "No specific response generated."

                    SymptomEntry.objects.create(
                        symptom_text=symptom_text,
                        classification=classification,
                        response_message=response_message
                    )

                except Exception as e:
                    error_message = f"An error occurred during symptom classification: {e}"
                    print(f"Django view error: {error_message}")

    context = {
        'form': form,
        'symptom_text': symptom_text,
        'classification': classification,
        'response_message': response_message,
        'conversation_messages': conversation_messages,
        'error_message': error_message,
    }
    return render(request, 'classifier_app/symptom_form.html', context)