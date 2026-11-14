import os

from dotenv import load_dotenv
from tavily import TavilyClient


# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# TAVILY API KEY
# --------------------------------------------------

TAVILY_API_KEY = os.getenv(
    "TAVILY_API_KEY"
)


# --------------------------------------------------
# TAVILY CLIENT
# --------------------------------------------------

tavily_client = None


if TAVILY_API_KEY:

    tavily_client = TavilyClient(
        api_key=TAVILY_API_KEY
    )


# --------------------------------------------------
# WEB SEARCH
# --------------------------------------------------

def search_web(
    query,
    max_results=5
):

    # Check API key
    if not TAVILY_API_KEY:

        raise ValueError(
            "TAVILY_API_KEY is not set in .env"
        )


    try:

        response = tavily_client.search(

            query=query,

            search_depth="advanced",

            max_results=max_results

        )


        results = []


        for result in response.get(
            "results",
            []
        ):

            results.append({

                "title":
                    result.get(
                        "title",
                        ""
                    ),

                "url":
                    result.get(
                        "url",
                        ""
                    ),

                "content":
                    result.get(
                        "content",
                        ""
                    )

            })


        return results


    except Exception as e:

        raise RuntimeError(
            f"Web search failed: {e}"
        )