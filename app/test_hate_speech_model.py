from api.topic_manager.hate_speech_model import hate_speech_model


def main() -> None:
    model = hate_speech_model()

    test_inputs = [
        "I hate you and you are disgusting.",
        "Thank you for your help, I really appreciate it.",
    ]

    for text in test_inputs:
        result = model.predict(text)
        is_hate = result.get("label") == "hate"
        print(f"text: {text}")
        print(f"prediction: {result}")
        print(f"is_hate: {is_hate}")
        print("-" * 50)


if __name__ == "__main__":
    main()
