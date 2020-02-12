# from pyarcade.mastermind import Mastermind
# from pyarcade.input_system import InputSystem


def run_pyarcade():
    """ This will effectively become our program entrypoint.
    """
    # Interaction demo
    """
    input_sys = InputSystem()

    while True:
        print(f"Game {input_sys.game}, Round {input_sys.round}")

        cmd = input("> ")

        if cmd == "exit":
            print("Exiting...")
            break

        win, valid = input_sys.take_input(cmd)

        if valid:
            if win:
                print("Correct guess!")
            else:
                print(f"Previous guess: {input_sys.get_last_guess()}")
        else:
            print("Invalid command.")
    """
    pass


if __name__ == "__main__":
    run_pyarcade()
