import delacruz_bank_transactions


def analyze_transactions(
    account_number=None
):

    transactions = (
        delacruz_bank_transactions
        .get_transactions()
    )

    if account_number is not None:

        transactions = [
            transaction
            for transaction in transactions
            if transaction.get(
                "account_number"
            ) == account_number
        ]


    # ==========================================
    # ANALYSIS 1
    # TRANSACTION SUMMARY
    # ==========================================

    total_transactions = len(
        transactions
    )

    deposits = 0
    withdrawals = 0


    # ==========================================
    # ANALYSIS 2
    # MONEY FLOW
    # ==========================================

    total_deposited = 0.0
    total_withdrawn = 0.0


    # ==========================================
    # ANALYSIS 3
    # ACCOUNT ACTIVITY
    # ==========================================

    largest_transaction = 0.0
    average_transaction = 0.0

    latest_transaction = "None"
    latest_timestamp = "None"


    for transaction in transactions:

        transaction_type = transaction.get(
            "transaction",
            ""
        )

        amount = transaction.get(
            "amount",
            0.0
        )

        if transaction_type == "Deposit":

            deposits += 1
            total_deposited += amount

        elif transaction_type == "Withdraw":

            withdrawals += 1
            total_withdrawn += amount


        if amount > largest_transaction:

            largest_transaction = amount


        latest_transaction = (
            transaction_type
        )

        latest_timestamp = (
            transaction.get(
                "timestamp",
                "None"
            )
        )


    if total_transactions > 0:

        total_transaction_amount = (
            total_deposited
            +
            total_withdrawn
        )

        average_transaction = (
            total_transaction_amount
            /
            total_transactions
        )


    net_cash_flow = (
        total_deposited
        -
        total_withdrawn
    )


    return {

        # Analysis 1
        "total_transactions":
            total_transactions,

        "deposits":
            deposits,

        "withdrawals":
            withdrawals,


        # Analysis 2
        "total_deposited":
            total_deposited,

        "total_withdrawn":
            total_withdrawn,

        "net_cash_flow":
            net_cash_flow,


        # Analysis 3
        "largest_transaction":
            largest_transaction,

        "average_transaction":
            average_transaction,

        "latest_transaction":
            latest_transaction,

        "latest_timestamp":
            latest_timestamp
    }