from tidy import TidyStructure


def main():
    tidier = TidyStructure(rand=False)
    tidier.tidy()
    tidier.open_tidy_dir()
    choice = input("Ready to clean up?(y/[n]) ")
    if choice == "y":
        tidier.clean_up()
        print("Cleaned")
    tidier.clear_tidy()
    

if __name__ == '__main__':
    main()
