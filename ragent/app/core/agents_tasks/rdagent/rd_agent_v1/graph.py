from langgraph.graph import StateGraph, END
from .state import RedditAgentState
from .nodes.validate_goals import validate_input_node
from .nodes.search_posts_directly import search_posts_directly_node
from .nodes.search_subreddits import search_subreddits_node
from .nodes.fetch_posts import fetch_posts_node, fetch_basic_post_nodes
from .nodes.generate_queries import generate_queries_node
import asyncio

# Advanced Reddit Agent Call


def create_reddit_graph() -> StateGraph:
    graph = StateGraph(RedditAgentState)
    graph.add_node("validate_input", validate_input_node)
    graph.add_node("generate_queries_node", generate_queries_node)
    graph.add_node("search_posts_directly_node", search_posts_directly_node)
    graph.add_node("search_subreddits_node", search_subreddits_node)
    graph.add_node("fetch_posts_node", fetch_posts_node)
    graph.set_entry_point("validate_input")
    graph.add_edge("validate_input", "generate_queries_node")
    graph.add_edge("generate_queries_node", "search_posts_directly_node")
    graph.add_edge("search_posts_directly_node", "search_subreddits_node")
    graph.add_edge("search_subreddits_node", "fetch_posts_node")
    graph.add_edge("fetch_posts_node", END)
    return graph.compile()

# Basic Reddit Agent Call -

def create_basic_reddit_graph() -> StateGraph:
    graph = StateGraph(RedditAgentState)
    graph.add_node("validate_input", validate_input_node)
    graph.add_node("generate_queries_node", generate_queries_node)
    graph.add_node("search_posts_directly_node", search_posts_directly_node)
    graph.add_node("search_subreddits_node", search_subreddits_node)
    graph.add_node("fetch_basic_post_node", fetch_basic_post_nodes)
    graph.set_entry_point("validate_input")
    graph.add_edge("validate_input", "generate_queries_node")
    graph.add_edge("generate_queries_node", "search_posts_directly_node")
    graph.add_edge("search_posts_directly_node", "search_subreddits_node")
    graph.add_edge("search_subreddits_node", "fetch_basic_post_node")
    graph.add_edge("fetch_basic_post_node", END)
    return graph.compile()

# Parallel Reddit Agent Call (true parallel using asyncio.gather in a node)
async def parallel_reddit_node(state):
    async def direct_search_branch():
        result_state = await search_posts_directly_node(state.copy())
        return {"direct_posts": result_state.get("direct_posts", [])}
        
    async def subreddit_branch():
        sub_state = await search_subreddits_node(state.copy())
        fetch_state = await fetch_basic_post_nodes(sub_state)
        return {"subreddit_posts": fetch_state.get("subreddit_posts", [])}
    result1, result2 = await asyncio.gather(direct_search_branch(), subreddit_branch())
    state.update(result1)
    state.update(result2)
    return state

# Parallel Reddit Agent Call (true parallel using asyncio.gather in a node)
async def parallel_advanced_reddit_node(state):
    async def direct_search_branch():
        result_state = await search_posts_directly_node(state.copy())
        return {"direct_posts": result_state.get("direct_posts", [])}
        
    async def subreddit_branch():
        sub_state = await search_subreddits_node(state.copy())
        fetch_state = await fetch_posts_node(sub_state)
        return {"subreddit_posts": fetch_state.get("posts", [])}
    result1, result2 = await asyncio.gather(direct_search_branch(), subreddit_branch())
    state.update(result1)
    state.update(result2)
    return state

def create_parallel_advanced_reddit_graph() -> StateGraph:
    graph = StateGraph(RedditAgentState)
    graph.add_node("validate_input", validate_input_node)
    graph.add_node("generate_queries_node", generate_queries_node)
    graph.add_node("parallel_advanced_reddit_node", parallel_advanced_reddit_node)
    graph.set_entry_point("validate_input")
    graph.add_edge("validate_input", "generate_queries_node")
    graph.add_edge("generate_queries_node", "parallel_advanced_reddit_node")
    graph.add_edge("parallel_advanced_reddit_node", END)
    return graph.compile()

def create_parallel_reddit_graph() -> StateGraph:
    graph = StateGraph(RedditAgentState)
    graph.add_node("validate_input", validate_input_node)
    graph.add_node("generate_queries_node", generate_queries_node)
    graph.add_node("parallel_reddit_node", parallel_reddit_node)
    graph.set_entry_point("validate_input")
    graph.add_edge("validate_input", "generate_queries_node")
    graph.add_edge("generate_queries_node", "parallel_reddit_node")
    graph.add_edge("parallel_reddit_node", END)
    return graph.compile()

reddit_graph = create_reddit_graph()
basic_redit_agent = create_basic_reddit_graph()
parallel_reddit_graph = create_parallel_reddit_graph() 
parallel_advanced_reddit_graph = create_parallel_advanced_reddit_graph() 