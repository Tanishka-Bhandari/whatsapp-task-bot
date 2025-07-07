from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

# In-memory storage for tasks and expenses
tasks = []
expenses = []

@app.route("/whatsapp", methods=['POST'])
def whatsapp_bot():
    incoming_msg = request.values.get('Body', '').strip()
    response = MessagingResponse()
    msg = response.message()

    if incoming_msg.lower().startswith('add task'):
        task = incoming_msg[8:].strip()
        if task:
            tasks.append(task)
            msg.body(f"✅ Task added: {task}")
        else:
            msg.body("⚠️ Please provide a task description after 'Add task'.")

    elif incoming_msg.lower().startswith('add expense'):
        parts = incoming_msg[11:].strip().split()
        if len(parts) >= 2:
            try:
                amount = float(parts[0])
                category = ' '.join(parts[1:])
                expenses.append((amount, category))
                msg.body(f"💰 Expense added: ₹{amount} for {category}")
            except ValueError:
                msg.body("⚠️ Invalid amount. Please use the format: Add expense <amount> <category>")
        else:
            msg.body("⚠️ Please provide both amount and category. Example: Add expense 200 food")

    elif incoming_msg.lower() == 'show tasks':
        if tasks:
            task_list = '\n'.join([f"{i+1}. {t}" for i, t in enumerate(tasks)])
            msg.body(f"📝 Your Tasks:\n{task_list}")
        else:
            msg.body("📭 No tasks found.")

    elif incoming_msg.lower() == 'show expenses':
        if expenses:
            expense_list = '\n'.join([f"₹{amt} - {cat}" for amt, cat in expenses])
            msg.body(f"💸 Your Expenses:\n{expense_list}")
        else:
            msg.body("📭 No expenses recorded.")

    else:
        msg.body("🤖 I can help you track tasks and expenses.\n\nCommands:\n- Add task <task>\n- Add expense <amount> <category>\n- Show tasks\n- Show expenses")

    return str(response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
