import streamlit as st
from delacruz_bank_account import BankAccount
import delacruz_bank_auth
import delacruz_bank_storage
import delacruz_bank_transactions
import delacruz_bank_analysis
from datetime import datetime

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="delacruz BANK",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== CUSTOM STYLING ==========
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    h1 {
        color: #fbbf24 !important;
        font-weight: 800;
        font-size: 2.8rem;
    }
    h2, h3 {
        color: #e2e8f0 !important;
    }
    .stButton > button {
        background: linear-gradient(90deg, #f59e0b, #d97706);
        color: #000;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.4rem 2rem;
        border: none;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #fbbf24, #f59e0b);
        transform: scale(1.02);
        transition: 0.2s;
    }
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stPasswordInput > div > div > input {
        background-color: #1e293b;
        border: 1px solid #475569;
        border-radius: 8px;
        color: white;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #334155;
        border-radius: 8px 8px 0 0;
        padding: 0.5rem 1.5rem;
        color: #cbd5e1;
    }
    .stTabs [aria-selected="true"] {
        background-color: #f59e0b;
        color: #000;
        font-weight: bold;
    }
    .stMetric {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #f59e0b;
    }
    </style>
""", unsafe_allow_html=True)

# ========== HEADER WITH REAL-TIME CLOCK ==========
st.title("🏦 delacruz BANK")
current_time = datetime.now().strftime("%B %d, %Y • %I:%M:%S %p")
st.caption(f"🔒 Secure Digital Banking System • Fast • Safe • Reliable • {current_time}")
st.divider()

# ========== SESSION SETUP ==========
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("account", None)
if "savings_goal" not in st.session_state:
    st.session_state.savings_goal = 0.0

# ========== LOGIN / REGISTER ==========
if not st.session_state.logged_in:
    tab_login, tab_register = st.tabs(["🔐 Login", "📝 Register"])

    with tab_login:
        st.subheader("👋 Welcome Back")
        account_number = st.text_input("Account Number", placeholder="Enter your account number")
        pin = st.text_input("PIN", type="password", placeholder="Enter your 4-digit PIN")
        
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            if st.button("🔓 Login", type="primary"):
                account, message = delacruz_bank_auth.login_account(account_number, pin)
                if account:
                    st.session_state.logged_in = True
                    st.session_state.account = account
                    st.success(f"✅ {message}")
                    st.rerun()
                else:
                    st.error(f"❌ {message}")

    with tab_register:
        st.subheader("🆕 Create New Account")
        st.info("Fill in details to create your account")
        acc_name = st.text_input("Full Name")
        new_acc_num = st.text_input("Account Number")
        new_pin = st.text_input("Set PIN (4 digits)", type="password")
        confirm_pin = st.text_input("Confirm PIN", type="password")
        acc_type = st.selectbox("Account Type", ["Savings Account", "Student Account"])
        initial_deposit = st.number_input("Initial Deposit (₱)", min_value=0.0, step=100.0)
        
        if st.button("✅ Register", type="primary"):
            account, message = delacruz_bank_auth.register_account(
                acc_name,
                new_acc_num,
                new_pin,
                confirm_pin,
                acc_type,
                initial_deposit
            )
            if account:
                st.success(f"✅ {message} Please Login.")
            else:
                st.error(f"❌ {message}")

# ========== LOGGED IN AREA ==========
else:
    account = st.session_state.account

    # Dashboard
    st.subheader("📊 Account Dashboard")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 Current Balance", f"₱{account.check_balance():,.2f}")
    with col2:
        st.metric("👤 Account Name", account.account_name)
    with col3:
        st.metric("📅 Last Updated", datetime.now().strftime("%H:%M:%S"))
    st.divider()

    # Sidebar Menu
    st.sidebar.title("📋 ATM MENU")
    st.sidebar.divider()
    choice = st.sidebar.radio(
        "Select Transaction",
        [
            "📥 Deposit Funds",
            "📤 Withdraw Funds",
            "🔐 Change PIN",
            "📱 Buy Mobile Load",
            "💸 Money Transfer",
            "🎯 Savings Goal Tracker",
            "📊 Transaction History",
            "📈 Account Analysis",
            "🚪 Logout"
        ]
    )
    st.sidebar.divider()
    st.sidebar.markdown("💳 Secure Banking • delacruz BANK")

    # ========== DEPOSIT ==========
    if choice == "📥 Deposit Funds":
        st.header("📥 Deposit Funds")
        st.info(f"Account: {account.account_name}")
        amount = st.number_input("Enter Deposit Amount (₱)", min_value=0.0, step=100.0)
        if st.button("✅ Deposit Now", type="primary"):
            success = account.deposit(amount)
            if success:
                delacruz_bank_transactions.log_transaction(account.account_number, "Deposit", amount)
                st.success(f"✅ Deposited ₱{amount:,.2f} successfully!")
                st.metric("New Balance", f"₱{account.check_balance():,.2f}")

    # ========== WITHDRAW ==========
    elif choice == "📤 Withdraw Funds":
        st.header("📤 Withdraw Funds")
        balance = account.check_balance()
        st.info(f"Available Balance: ₱{balance:,.2f}")
        amount = st.number_input("Enter Withdrawal Amount (₱)", min_value=0.0, step=100.0)
        if st.button("✅ Withdraw Now", type="primary"):
            if amount > balance:
                st.error("❌ Insufficient balance!")
            else:
                success = account.withdraw(amount)
                if success:
                    delacruz_bank_transactions.log_transaction(account.account_number, "Withdrawal", amount)
                    st.success(f"✅ Withdrew ₱{amount:,.2f} successfully!")
                    st.metric("New Balance", f"₱{account.check_balance():,.2f}")

    # ========== CHANGE PIN — ✅ FIXED: ANY 4-DIGIT PIN WORKS ==========
    elif choice == "🔐 Change PIN":
        st.header("🔐 Change Your PIN")
        current_pin = st.text_input("Current PIN", type="password")
        new_pin = st.text_input("New PIN (4 digits)", type="password")
        confirm_pin = st.text_input("Confirm New PIN", type="password")

        if st.button("🔄 Update PIN", type="primary"):
            new_pin_clean = new_pin.strip()
            confirm_clean = confirm_pin.strip()
            current_clean = current_pin.strip()

            if not account.verify_pin(current_clean):
                st.error("❌ Current PIN is incorrect")
            elif len(new_pin_clean) != 4 or not new_pin_clean.isdigit():
                st.error("❌ New PIN must be exactly 4 digits")
            elif new_pin_clean != confirm_clean:
                st.error("❌ PINs do not match")
            elif current_clean == new_pin_clean:
                st.warning("⚠️ New PIN must be different from current PIN")
            else:
                # ✅ Direct save — NO "only 1111" restriction!
                account._pin = new_pin_clean
                delacruz_bank_storage.save_account(account)
                st.success(f"✅ PIN changed successfully to {new_pin_clean}!")
                st.balloons()

    # ========== MOBILE LOAD ==========
    elif choice == "📱 Buy Mobile Load":
        st.header("📱 Buy Mobile Load")
        balance = account.check_balance()
        st.info(f"Available Balance: ₱{balance:,.2f}")

        network = st.selectbox("Network Provider", ["Globe", "Smart", "DITO", "TM", "Sun"])
        phone = st.text_input("Mobile Number", placeholder="e.g. 09171234567")
        preset = st.selectbox("Load Amount", ["-- Select --", "₱50", "₱100", "₱300", "₱500", "₱1000", "Custom"])
        
        if preset == "Custom":
            amount = st.number_input("Enter Amount (₱)", min_value=10.0, step=10.0)
        elif preset != "-- Select --":
            amount = float(preset.replace("₱", ""))
        else:
            amount = 0.0

        if st.button("📲 Purchase Load", type="primary"):
            if not phone.startswith("09") or len(phone) != 11:
                st.error("❌ Enter a valid PH number starting with 09")
            elif amount <= 0:
                st.error("❌ Select a valid amount")
            elif amount > balance:
                st.error("❌ Insufficient balance")
            else:
                account.withdraw(amount)
                delacruz_bank_transactions.log_transaction(account.account_number, f"Mobile Load - {network}", amount)
                st.success(f"✅ ₱{amount:,.2f} load sent to {phone}")
                st.metric("New Balance", f"₱{account.check_balance():,.2f}")

    # ========== MONEY TRANSFER ==========
    elif choice == "💸 Money Transfer":
        st.header("💸 Transfer to Another Account")
        balance = account.check_balance()
        st.info(f"Your Balance: ₱{balance:,.2f}")

        target_acc = st.text_input("Recipient Account Number")
        amount = st.number_input("Transfer Amount (₱)", min_value=50.0, step=50.0)
        FEE = 15.00
        total_deduct = amount + FEE
        st.info(f"Service Fee: ₱{FEE:.2f} → Total: ₱{total_deduct:,.2f}")

        if st.button("📤 Send Money", type="primary"):
            if target_acc == account.account_number:
                st.error("❌ Cannot send to yourself")
            elif not delacruz_bank_storage.account_exists(target_acc):
                st.error("❌ Recipient not found")
            elif total_deduct > balance:
                st.error(f"❌ Need ₱{total_deduct:,.2f} total")
            else:
                account.withdraw(total_deduct)
                recipient = delacruz_bank_storage.find_account(target_acc)
                if recipient:
                    recipient.deposit(amount)
                    delacruz_bank_storage.save_account(recipient)
                delacruz_bank_transactions.log_transaction(account.account_number, f"Transfer → {target_acc}", total_deduct)
                st.success(f"✅ Sent ₱{amount:,.2f} to {target_acc}")
                st.metric("New Balance", f"₱{account.check_balance():,.2f}")

    # ========== SAVINGS GOAL ==========
    elif choice == "🎯 Savings Goal Tracker":
        st.header("🎯 Savings Goal Tracker")
        balance = account.check_balance()
        goal = st.number_input("Set Savings Goal (₱)", min_value=0.0, step=500.0, value=st.session_state.savings_goal)
        st.session_state.savings_goal = goal

        if goal > 0:
            progress = min(100.0, (balance / goal) * 100)
            remaining = max(0.0, goal - balance)
            st.progress(progress / 100)
            col1, col2, col3 = st.columns(3)
            col1.metric("💵 Saved", f"₱{balance:,.2f}")
            col2.metric("📊 Progress", f"{progress:.1f}%")
            col3.metric("🎯 Remaining", f"₱{remaining:,.2f}")
            if progress >= 100:
                st.balloons()
                st.success("🎉 GOAL REACHED!")
        else:
            st.info("ℹ️ Set a goal above to track progress.")

    # ========== TRANSACTION HISTORY ==========
    elif choice == "📊 Transaction History":
        st.header("📊 Transaction History")
        lines = delacruz_bank_transactions.view_history(account.account_number)
        if lines and len(lines) > 0 and lines[0] != "No transactions found.":
            st.text("\n".join(lines))
        else:
            st.info("📭 No transactions found.")

    # ========== ACCOUNT ANALYSIS ==========
    elif choice == "📈 Account Analysis":
        st.header("📈 Account Analysis")
        
        balance = account.check_balance()
        acc_num = account.account_number
        
        total_deposit = 0.0
        total_withdraw = 0.0
        total_transfers = 0.0
        total_load = 0.0
        
        lines = delacruz_bank_transactions.view_history(acc_num)
        if lines and len(lines) > 0 and lines[0] != "No transactions found.":
            i = 0
            while i < len(lines):
                line = lines[i]
                if "Transaction:" in line:
                    trans_type = line.split("Transaction: ")[-1].strip()
                    amount = 0.0
                    if i + 1 < len(lines) and "Amount: ₱" in lines[i+1]:
                        try:
                            amount = float(lines[i+1].split("₱")[-1])
                        except:
                            amount = 0.0
                    
                    if "Deposit" in trans_type:
                        total_deposit += amount
                    elif "Withdrawal" in trans_type:
                        total_withdraw += amount
                    elif "Transfer" in trans_type:
                        total_transfers += amount
                    elif "Mobile Load" in trans_type:
                        total_load += amount
                i += 1
        
        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Current Balance", f"₱{balance:,.2f}")
        col2.metric("📥 Total Deposits", f"₱{total_deposit:,.2f}")
        col3.metric("📤 Total Withdrawals", f"₱{total_withdraw:,.2f}")
        
        col4, col5, col6 = st.columns(3)
        col4.metric("💸 Transfers Sent", f"₱{total_transfers:,.2f}")
        col5.metric("📱 Mobile Load", f"₱{total_load:,.2f}")
        net_savings = total_deposit - total_withdraw - total_transfers - total_load
        col6.metric("📊 Net Savings", f"₱{net_savings:,.2f}")
        
        total_in = total_deposit
        total_out = total_withdraw + total_transfers + total_load
        if total_in > 0:
            savings_pct = max(0, min(100, ((total_in - total_out) / total_in) * 100))
            st.subheader(f"📊 Savings Rate: {savings_pct:.1f}%")
            st.progress(savings_pct / 100)
        else:
            st.info("ℹ️ Make a deposit first to see your analysis.")

    # ========== LOGOUT ==========
    elif choice == "🚪 Logout":
        st.session_state.logged_in = False
        st.session_state.account = None
        st.rerun()