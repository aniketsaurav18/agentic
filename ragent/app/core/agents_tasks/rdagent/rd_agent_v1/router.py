from fastapi import APIRouter, HTTPException, Depends
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import AgentPlatformEnum
from .state import RedditAgentInput, RedditAgentState
from .graph import reddit_graph, parallel_reddit_graph, basic_redit_agent, parallel_advanced_reddit_graph
from app.database import get_db
import structlog

router = APIRouter()
logger = structlog.get_logger()

@router.post("/reddit/reddit-agent", dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def run_reddit_agent(input: RedditAgentInput, db: AsyncSession = Depends(get_db)):
    try:
        initial_state = RedditAgentState(
            agent_name=input.agent_name,
            agent_id=1,               # agent id from agents table
            agent_platform=AgentPlatformEnum.reddit,         # reddit, twitter, linkedin
            project_id="1",             # project id from projects table
            execution_id=1, 
            goals=input.goals,
            instructions=input.instructions,
            description=input.description,
            expectation=input.expectation,
            target_audience=input.target_audience,
            company_keywords=input.company_keywords,
            keywords=input.keywords,
            min_upvotes=input.min_upvotes,
            max_age_days=input.max_age_days,
            restrict_to_goal_subreddits=input.restrict_to_goal_subreddits,
            subreddits=[],
            generated_queries=[],
            posts=[],
            seen_post_ids=set(),
            subreddit_posts=[],
            direct_posts=[],
            retries=0,
            error=None,
            db=db,
            llm=None
        )
        result = await basic_redit_agent.ainvoke(initial_state)
        return result
    except Exception as e:
        # add a way to trace the error stack
        import traceback
        logger.error("Reddit agent processing failed", agent_name=input.agent_name, error=str(e), traceback=traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

# ---------------------- Advanced Reddit Agent ----------------------
@router.post("/reddit/advanced-reddit-agent", dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def run_advanced_reddit_agent(input: RedditAgentInput, db: AsyncSession = Depends(get_db)):
    """Run the *advanced* Reddit agent (full graph with semantic ranking)."""
    try:
        initial_state = RedditAgentState(
            agent_name=input.agent_name,
            agent_id=1,               
            agent_platform=AgentPlatformEnum.reddit, 
            project_id="1",             
            execution_id=1, 
            goals=input.goals,
            instructions=input.instructions,
            description=input.description,
            expectation=input.expectation,
            target_audience=input.target_audience,
            company_keywords=input.company_keywords,
            keywords=input.keywords,
            min_upvotes=input.min_upvotes,
            max_age_days=input.max_age_days,
            restrict_to_goal_subreddits=input.restrict_to_goal_subreddits,
            subreddits=[],
            generated_queries=[],
            posts=[],
            seen_post_ids=set(),
            subreddit_posts=[],
            direct_posts=[],
            retries=0,
            error=None,
            db=db,
            llm=None,
        )
        result = await parallel_advanced_reddit_graph.ainvoke(initial_state)
        return result
    except Exception as e:
        import traceback
        logger.error(
            "Advanced Reddit agent processing failed",
            agent_name=input.agent_name,
            error=str(e),
            traceback=traceback.format_exc(),
        )
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}") 