import uvicorn


def main() -> None:
    # Sin reload: en Windows el reloader duplica procesos y CLIPS puede colgar o resetear conexiones.
    uvicorn.run(
        "pricing_expert.api.main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
    )


if __name__ == "__main__":
    main()
