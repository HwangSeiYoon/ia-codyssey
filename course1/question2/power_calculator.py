def main():
    try:
        base = float(input("Enter number: "))
    except ValueError:
        print("Invalid number input.")
        return

    while True:
        try:
            exponent = int(input("Enter exponent (must be greater than 0): "))
            if exponent <= 0:
                print("Exponent must be greater than 0. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid exponent input. Please enter an integer.")

    result = 1.0
    for _ in range(abs(exponent)):
        result *= base

    if exponent < 0:
        result = 1 / result

    print(f"Result: {result}")

if __name__ == "__main__":
    main()
