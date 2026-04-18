from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from prompt_library.prompt import SYSTEM_PROMPT
from utils.model_loader import ModelLoader, ConfigLoader




class GraphBuilder:
    def __init__(self):
        self.tools = []
        self.graph = None 

        self.system_prompt = SYSTEM_PROMPT

        self.config = ConfigLoader()
        self.model = ModelLoader(self.config)
        self.llm = self.model.load_llm()
        self.llm_with_tools = self.llm.bind_tools(tools=self.tools)
        pass

    def agent_function(self, state:MessagesState):
        """main agent function that """
        user_question = state["messages"]
        input_question = [self.system_prompt] + user_question
        response = self.llm_with_tools.invoke(input_question)
        return {"messages": [response]}
    
    def build_graph(self):
       """builds a complied graph api"""
       graph_builder = StateGraph(MessagesState)
       graph_builder.add_node("agent", self.agent_function)
       graph_builder.add_node("tools", ToolNode(tools=self.tools))
       graph_builder.add_edge(START, "agent")
       graph_builder.add_conditional_edges("agent", tools_condition)
       graph_builder.add_edge("tools", "agent")
       graph_builder.add_edge("agent", END)
       self.graph = graph_builder.compile()
       return self.graph
    
    def __call__(self):
        return self.build_graph()

       