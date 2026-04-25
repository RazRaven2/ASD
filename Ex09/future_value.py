def calculate_future_value(monthly_payment, years, annual_interest_rate):
    months = years * 12
    monthly_interest_rate = annual_interest_rate / 12 / 100
    future_value = 0

    for _ in range(months):
        future_value = (
            future_value + monthly_payment
        ) * (1 + monthly_interest_rate)

    return future_value

def main():
    print("Future Value Calculator\n")
    while True:
        try:
            monthly_payment = float(
                input("Enter monthly investment:   ").strip()
            )
            years = int(
                input("Enter number of years:      ").strip()
            )
            annual_interest_rate = float(
                input("Enter yearly interest rate: ").strip()
            )
            
            future_value = calculate_future_value(
                monthly_payment, years, annual_interest_rate
            )
            print(
                f"Future value:               {future_value:.2f}\n"
            )
            
            continue_calculation = input(
                "Continue? (y/n): "
            ).strip().lower()
            print()
            if continue_calculation != 'y':
                print("Bye!")
                break
        except ValueError:
            print(
                "Invalid input. Please enter numeric values for the payment, years, "
                "and interest rate."
            )

if __name__ == "__main__":
    main()