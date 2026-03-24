from app.services import SiteBuilderRuntime


def main() -> None:
    runtime = SiteBuilderRuntime()
    session_id = "demo-session"
    messages = [
        "我要做一个珠宝站",
        "英文，高级极简",
        "确认",
        "ds，home decor，美区，20-80 USD，30款",
        "确认",
    ]
    for idx, msg in enumerate(messages, start=1):
        result = runtime.handle_message(session_id, msg)
        print(f"\n[{idx}] user: {msg}")
        print(f"assistant: {result['reply']}")
        print(f"stage: {result['stage']}")
        if result.get("task"):
            print(f"task: {result['task']}")


if __name__ == "__main__":
    main()
