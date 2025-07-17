# classifier_app/views.py

# --- Imports ---
import os
import os
from dotenv import load_dotenv
load_dotenv()  # loads from .env into os.environ

from typing import TypedDict, Annotated
from django.shortcuts import render
from django.http import HttpRequest
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

from .forms import SymptomForm
from .models import SymptomEntry

# --- Global LLM Initialization ---
llm = None
try:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
    print("Gemini LLM initialized successfully for Django app.")
except Exception as e:
    print(f"Error initializing Gemini LLM for Django app: {e}")
    print("Please ensure GOOGLE_API_KEY is set as an environment variable.")

# --- Define the AgentState for LangGraph ---
class AgentState(TypedDict):
    symptom: str
    classification: str
    messages: Annotated[list, add_messages]
    detailed_info: str
    follow_up_questions: list[str]
    initial_advice: str
    conversation_summary: str

# --- LangGraph Node Definitions (ALL NODES DEFINED HERE) ---
# Ensure all these functions are defined BEFORE build_and_compile_chatbot

def get_symptom_initial_state(symptom_text: str) -> AgentState:
    return {
        "symptom": symptom_text,
        "messages": [HumanMessage(content=symptom_text)],
        "detailed_info": "",
        "follow_up_questions": [],
        "initial_advice": "",
        "conversation_summary": ""
    }

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
            classification = "general"
        
        return {"classification": classification, "messages": [HumanMessage(content=f"Symptom classified as: {classification.upper()}.")]}

    except Exception as e:
        return {"classification": "error", "messages": [HumanMessage(content="Error during symptom classification.")]}
# --- Add these placeholder node functions BEFORE build_and_compile_chatbot() ---

def emergency_node(state: AgentState) -> AgentState:
    print("\nNew Node: Emergency category processing...")
    state['messages'].append(HumanMessage(content="This symptom may indicate an emergency. Please seek immediate medical attention."))
    return state

def mental_issue_node(state: AgentState) -> AgentState:
    print("\nNew Node: Mental Issue category processing...")
    state['messages'].append(HumanMessage(content="This symptom may be related to a mental health concern. Please consider consulting a mental health professional."))
    return state

def general_node(state: AgentState) -> AgentState:
    print("\nNew Node: General category processing...")
    state['messages'].append(HumanMessage(content="This appears to be a general health concern. Let's proceed with more details."))
    return state

def detailed_info_node(state: AgentState) -> AgentState:
    
    print("\nNew Node: Generating detailed info...")
    classification = state.get("classification", "general")
    symptom = state.get("symptom", "a health concern")

    prompt_text = f"""
    You are a helpful assistant providing general information.
    Given the symptom '{symptom}' was classified as '{classification}',
    provide a very brief (1-2 sentences) general overview of what this category typically involves.
    Do NOT give medical advice or diagnosis. Start with "Generally, this category involves...".
    """
    if llm is None:
        return {"detailed_info": "Could not retrieve detailed information (LLM not available)."}
    try:
        response = llm.invoke(prompt_text)
        info = response.content.strip()
        return {"detailed_info": info, "messages": [HumanMessage(content=f"Detailed Info: {info}")]}
    except Exception as e:
        print(f"Error generating detailed info: {e}")
        return {"detailed_info": "Could not retrieve detailed information."}

def ask_followup_questions_node(state: AgentState) -> AgentState:
    print("\nNew Node: Asking follow-up questions...")
    symptom = state.get("symptom", "a general health concern")
    
    prompt_text = f"""
    You are a helpful assistant. Based on the symptom: "{symptom}",
    generate 2-3 concise, clarifying questions a medical professional might ask to get more details.
    Format them as a numbered list. Do NOT provide diagnosis or advice.
    """
    if llm is None:
        return {"follow_up_questions": ["Could not generate follow-up questions (LLM not available)."]}
    try:
        response = llm.invoke(prompt_text)
        questions_raw = response.content.strip()
        questions = [q.strip() for q in questions_raw.split('\n') if q.strip()]
        return {"follow_up_questions": questions, "messages": [HumanMessage(content=f"Follow-up Questions: {questions_raw}")]}
    except Exception as e:
        print(f"Error generating follow-up questions: {e}")
        return {"follow_up_questions": ["Could not generate follow_up_questions."]}

def provide_initial_advice_node(state: AgentState) -> AgentState:
    print("\nNew Node: Providing initial advice...")
    classification = state.get("classification", "general")
    symptom = state.get("symptom", "a health concern")

    prompt_text = f"""
    You are a helpful assistant providing very general, initial advice.
    Given the symptom '{symptom}' was classified as '{classification}',
    provide 1-2 sentences of very general, non-medical advice (e.g., rest, hydrate, monitor).
    Crucially, always include a disclaimer that this is NOT medical advice and to consult a doctor.
    """
    if llm is None:
        return {"initial_advice": "Could not provide initial advice (LLM not available)."}
    try:
        response = llm.invoke(prompt_text)
        advice = response.content.strip()
        return {"initial_advice": advice, "messages": [HumanMessage(content=f"Initial Advice: {advice}")]}
    except Exception as e:
        print(f"Error generating initial advice: {e}")
        return {"initial_advice": "Could not provide initial advice."}

def summarize_conversation_node(state: AgentState) -> AgentState:
    print("\nNew Node: Summarizing conversation...")
    all_messages = "\n".join([f"{msg.type}: {msg.content}" for msg in state.get("messages", [])])
    symptom = state.get("symptom", "a health concern")
    classification = state.get("classification", "N/A")

    prompt_text = f"""
    Summarize the following interaction about a symptom.
    Focus on the user's symptom, its classification, and the main recommendation given.
    Keep it concise (2-3 sentences).
    Interaction:
    {all_messages}
    """
    if llm is None:
        return {"conversation_summary": "Could not summarize conversation (LLM not available)."}
    try:
        response = llm.invoke(prompt_text)
        summary = response.content.strip()
        return {"conversation_summary": summary, "messages": [HumanMessage(content=f"Summary: {summary}")]}
    except Exception as e:
        print(f"Error summarizing conversation: {e}")
        return {"conversation_summary": "Could not summarize conversation."}

def router(state: AgentState) -> str:
    print("\nSTEP 5: Routing based on classification...")
    classification = state.get("classification")

    if classification == "emergency":
        return "emergency_path"
    elif classification == "mental_issue":
        return "mental_issue_path"
    elif classification == "general":
        return "general_path"
    else:
        return "general_path"

# --- STEP 7: Build and Compile the LangGraph Workflow ---
# This function is now defined AFTER ALL the node functions it uses.
def build_and_compile_chatbot():
    """
    Builds and compiles the LangGraph workflow for the symptom classifier.
    This function is called once globally to ensure all nodes are defined.
    """
    print("\nSTEP 7: Building LangGraph workflow...")
    workflow = StateGraph(AgentState)

    workflow.add_node("classify_symptom", classify_symptom)
    workflow.add_node("detailed_info_node", detailed_info_node)
    workflow.add_node("ask_followup_questions_node", ask_followup_questions_node)
    workflow.add_node("provide_initial_advice_node", provide_initial_advice_node)
    workflow.add_node("summarize_conversation_node", summarize_conversation_node)
    workflow.add_node("emergency_node", emergency_node) # This node is now defined above
    workflow.add_node("mental_issue_node", mental_issue_node) # This node is now defined above
    workflow.add_node("general_node", general_node) # This node is now defined above

    workflow.set_entry_point("classify_symptom")

    workflow.add_conditional_edges(
        "classify_symptom",
        router,
        {
            "emergency_path": "emergency_node",
            "mental_issue_path": "mental_issue_node",
            "general_path": "general_node",
        }
    )

    workflow.add_edge("emergency_node", "detailed_info_node")
    workflow.add_edge("detailed_info_node", "provide_initial_advice_node")
    workflow.add_edge("provide_initial_advice_node", "summarize_conversation_node")
    workflow.add_edge("summarize_conversation_node", END)

    workflow.add_edge("mental_issue_node", "detailed_info_node")
    workflow.add_edge("detailed_info_node", "provide_initial_advice_node")
    workflow.add_edge("provide_initial_advice_node", "summarize_conversation_node")
    workflow.add_edge("summarize_conversation_node", END)

    workflow.add_edge("general_node", "ask_followup_questions_node")
    workflow.add_edge("ask_followup_questions_node", "detailed_info_node")
    workflow.add_edge("detailed_info_node", "provide_initial_advice_node")
    workflow.add_edge("provide_initial_advice_node", "summarize_conversation_node")
    workflow.add_edge("summarize_conversation_node", END)

    app = workflow.compile()
    print("LangGraph workflow compiled successfully for Django app.")
    return app

# --- Global Instance of the Chatbot ---
# Initialize as None. Compilation will happen on first request.
hospital_chatbot = None 

# --- Django View Function ---
def symptom_classifier_view(request: HttpRequest):
    # Use a global keyword to modify the global variable hospital_chatbot
    global hospital_chatbot 

    form = SymptomForm()
    symptom_text = None
    classification = None
    response_message = None
    conversation_messages = []
    detailed_info = None
    follow_up_questions = []
    initial_advice = None
    conversation_summary = None
    error_message = None

    # Lazy initialization of the chatbot:
    # Compile the chatbot only if it hasn't been compiled yet.
    if hospital_chatbot is None:
        try:
            hospital_chatbot = build_and_compile_chatbot()
        except Exception as e:
            error_message = f"Error during chatbot compilation: {e}"
            print(f"Error during chatbot compilation: {e}")
            # If compilation fails, ensure hospital_chatbot remains None
            hospital_chatbot = None 

    if request.method == 'POST':
        form = SymptomForm(request.POST)
        if form.is_valid():
            symptom_text = form.cleaned_data['symptom_text']

            if hospital_chatbot is None:
                # This check is still valid if compilation failed on first attempt
                error_message = "Symptom classifier backend is not available. Please contact support."
            else:
                try:
                    initial_state = get_symptom_initial_state(symptom_text)
                    final_state = hospital_chatbot.invoke(initial_state)

                    classification = final_state.get('classification', 'N/A')
                    response_message = final_state.get('messages', [])[-1].content if final_state.get('messages') else "No specific response."
                    conversation_messages = [f"{msg.type.capitalize()}: {msg.content}" for msg in final_state.get('messages', [])]
                    
                    detailed_info = final_state.get('detailed_info', '')
                    follow_up_questions = final_state.get('follow_up_questions', [])
                    initial_advice = final_state.get('initial_advice', '')
                    conversation_summary = final_state.get('conversation_summary', '')

                    # Save to database (ensure your models.py has these fields if you want to save them)
                    SymptomEntry.objects.create(
                        symptom_text=symptom_text,
                        classification=classification,
                        response_message=response_message,
                        # If you added detailed_info, etc. to models.py, uncomment and add them here:
                        # detailed_info=detailed_info,
                        # follow_up_questions_json=json.dumps(follow_up_questions), # Remember to import json
                        # initial_advice=initial_advice,
                        # conversation_summary=conversation_summary,
                    )

                except Exception as e:
                    error_message = f"An unexpected error occurred during symptom classification: {e}"
                    print(f"Django view runtime error: {error_message}")

    context = {
        'form': form,
        'symptom_text': symptom_text,
        'classification': classification,
        'response_message': response_message,
        'conversation_messages': conversation_messages,
        'detailed_info': detailed_info,
        'follow_up_questions': follow_up_questions,
        'initial_advice': initial_advice,
        'conversation_summary': conversation_summary,
        'error_message': error_message,
    }
    return render(request, 'classifier_app/symptom_form.html', context)
