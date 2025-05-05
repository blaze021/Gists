import random
from textual.app import App, ComposeResult
from textual.widgets import Static, Button, Footer
from textual.containers import Horizontal, Grid, Vertical
from textual.reactive import reactive
from textual.timer import Timer

# ASCII Art header
ASCII_ART = r"""
___  ___ _   __ _____             _   ________  _____
|  \/  || | / //  ___|           | | / /| ___ \/  __ \
| .  . || |/ / \ `--.            | |/ / | |_/ /| /  \/
| |\/| ||    \  `--. \           |    \ | ___ \| |
| |  | || |\  \/\__/ /           | |\  \| |_/ /| \__/\
\_|  |_/\_| \_/\____/            \_| \_/\____/  \____/


          Kubernetes QUIz 2025
"""

# List of quiz questions
QUIZ_QUESTIONS = [
    {
        "question": "Which component schedules pods in Kubernetes?",
        "options": ["kube-apiserver", "kube-scheduler", "kubelet", "etcd"],
        "answer": "B"
    },
    {
        "question": "Which object exposes services externally?",
        "options": ["Service", "Ingress", "ConfigMap", "Deployment"],
        "answer": "B"
    },
    {
        "question": "How do you view pods in all namespaces?",
        "options": [
            "kubectl get all",
            "kubectl get pods",
            "kubectl get pods --all",
            "kubectl get pods --all-namespaces"
        ],
        "answer": "D"
    },
]

class KBCApp(App):
    CSS = """
    #ascii {
        height: 7;
        content-align: center middle;
    }

    #question-box {
        height: 3;
        content-align: left middle;
        padding: 1 2;
    }

    #timer-box {
        height: 3;
        content-align: center middle;
        padding: 1 2;
        color: red;
    }

    #countdown-box {
        height: 3;
        content-align: center middle;
        padding: 1 2;
        color: blue;
    }

    .option-button {
        width: 100%;
        height: 3;
        margin: 1;
        border: solid gray;
        text-align: center;
    }

    #button-grid {
        grid-size: 2;
        grid-columns: 1fr 1fr;
        padding: 1 4;
    }
    """

    current_question = reactive({})
    seconds_remaining = reactive(15)
    timer: Timer | None = None

    def on_mount(self):
        """Initialize the first question and start the timer"""
        self.load_question()
        self.timer = self.set_interval(1, self.update_timer)

    def compose(self) -> ComposeResult:
        """Compose the layout of the app"""
        yield Static(ASCII_ART, id="ascii")

        # Stack the countdown on top of the question
        yield Vertical(
            Static("", id="countdown-box"),  # Countdown box at the top
            Horizontal(
                Static("", id="question-box"),  # Question box
                Static("", id="timer-box")       # Timer box (for countdown)
            ),
        )

        yield Grid(
            Button("", id="A", classes="option-button"),
            Button("", id="B", classes="option-button"),
            Button("", id="C", classes="option-button"),
            Button("", id="D", classes="option-button"),
            id="button-grid"
        )
        yield Footer()

    def load_question(self):
        """Load a random question"""
        self.seconds_remaining = 15  # Reset the timer to 15 seconds for each question
        self.current_question = random.choice(QUIZ_QUESTIONS)  # Select random question
        qtext = self.current_question["question"]
        options = self.current_question["options"]

        # Update the question and initial timer
        self.query_one("#question-box", Static).update(f"❓ {qtext}")
        self.query_one("#timer-box", Static).update(f"⏳ {self.seconds_remaining}s")
        self.query_one("#countdown-box", Static).update(f"⏳ {self.seconds_remaining}s")  # Countdown shown on top

        # Update the options on buttons
        for idx, label in enumerate(["A", "B", "C", "D"]):
            btn = self.query_one(f"#{label}", Button)
            btn.label = f"{label}: {options[idx]}"
            btn.disabled = False
            btn.variant = "default"

    def update_timer(self):
        """Update the countdown timer"""
        if self.seconds_remaining > 0:
            self.seconds_remaining -= 1
            # Update both the timer and countdown box
            self.query_one("#timer-box", Static).update(f"⏳ {self.seconds_remaining}s")
            self.query_one("#countdown-box", Static).update(f"⏳ {self.seconds_remaining}s")  # Update countdown separately
        else:
            self.disable_buttons("⏱️ Time's up!")
            self.set_timer(2, self.load_question)  # Show next question after 2 seconds

    def disable_buttons(self, msg):
        """Disable all option buttons"""
        for btn in self.query(".option-button"):
            btn.disabled = True
        if msg:
            self.query_one("#question-box", Static).update(msg)

    def on_button_pressed(self, event: Button.Pressed):
        """Handle option button press event"""
        selected = event.button.id
        correct = self.current_question["answer"]

        if selected == correct:
            event.button.variant = "success"
            self.query_one("#question-box", Static).update("✅ Correct!")
        else:
            event.button.variant = "error"
            self.query_one("#question-box", Static).update(f"❌ Wrong! Correct: {correct}")
            self.query_one(f"#{correct}", Button).variant = "success"

        self.disable_buttons("")  # Disable buttons after answer
        self.set_timer(2, self.load_question)  # Next question after 2 seconds

if __name__ == "__main__":
    KBCApp().run()
