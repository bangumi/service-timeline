import uvicorn


def main():
    uvicorn.run("chii.server:app", port=3000, env_file=".env")
