import argparse

from src.qa_system.expert_system import ChemicalQAExpert


def main():
    # 初始化系统
    expert = ChemicalQAExpert()

    # 命令行界面
    parser = argparse.ArgumentParser(description="Organic Electrocatalysis QA Expert System")
    parser.add_argument("-q", "--question", help="Your research question about organic electrocatalysis")
    args = parser.parse_args()

    if args.question:
        # 命令行模式
        response = expert.answer_query(args.question)
        print("\n" + response)
    else:
        # 交互模式
        print("Organic Electrocatalysis QA Expert System (Type 'exit' to quit)")
        while True:
            question = input("\nYour question: ")
            if question.lower() in ['exit', 'quit']:
                break

            response = expert.answer_query(question)
            print("\n" + response)
            print("\n" + "=" * 80)


if __name__ == "__main__":
    main()

# What is Electrocatalysis?
