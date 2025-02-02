import json
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Create the FastAPI app.
app = FastAPI()

# Enable CORS for GET requests from any origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Load the JSON data at startup and build a lookup dictionary.
try:
    with open("q-vercel-python.json", "r") as f:
        items = json.load(f)
    # Create a dictionary mapping names to marks.
    marks_lookup = {item["name"]: item["marks"] for item in items}
except Exception as e:
    raise RuntimeError(f"Failed to load data file: {e}")


@app.get("/api")
async def get_marks(
    name: list[str] = Query(..., description="List of names to lookup marks for"),
):
    """
    Accepts one or more 'name' query parameters. Looks up and returns
    a JSON object with a list of marks that correspond to the provided names.
    """
    result = []
    for n in name:
        # If a name is not found, you could choose to return an error.
        # Here, we simply return None for any unknown name.
        if n in marks_lookup:
            result.append(marks_lookup[n])
        else:
            # Alternatively, raise an HTTP exception if strict matching is desired.
            raise HTTPException(status_code=404, detail=f"Name '{n}' not found")
    return {"marks": result}


if __name__ == "__main__":
    # For local testing, you can run with Uvicorn.
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
