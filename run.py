import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        "app.asgi:app", host="0.0.0.0", port=9000, workers=4, timeout_keep_alive=65,
        headers=[("server", "BTT")], forwarded_allow_ips="*"
    )
