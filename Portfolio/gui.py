import os
import mysql.connector
import customtkinter as ctk
from dotenv import load_dotenv

# Load configurations from .env
load_dotenv()

# Set dark theme and custom color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")  # Using built-in blue theme, customized with exact styling

class PortfolioContactApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Lohesvar | Connect Desktop")
        self.geometry("600x700")
        self.resizable(False, False)
        
        # Configure layout grids
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create main background card frame (Dark Slate color palette)
        self.main_frame = ctk.CTkFrame(
            self,
            fg_color="#0F172A",
            border_color="#1E293B",
            border_width=2,
            corner_radius=15
        )
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Header Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Let's build something extraordinary.",
            font=ctk.CTkFont(family="Outfit", size=24, weight="bold"),
            text_color="#F8FAFC"
        )
        self.title_label.grid(row=0, column=0, pady=(40, 5), padx=20, sticky="w")

        # Header Subtitle
        self.subtitle_label = ctk.CTkLabel(
            self.main_frame,
            text="Save your contact inquiry directly to the database.",
            font=ctk.CTkFont(family="Inter", size=13),
            text_color="#94A3B8"
        )
        self.subtitle_label.grid(row=1, column=0, pady=(0, 30), padx=20, sticky="w")

        # Name Field
        self.name_label = ctk.CTkLabel(
            self.main_frame,
            text="Name",
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
            text_color="#CBD5E1"
        )
        self.name_label.grid(row=2, column=0, pady=(10, 2), padx=20, sticky="w")
        
        self.name_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="John Doe",
            height=40,
            fg_color="#1E293B",
            border_color="#334155",
            text_color="#F8FAFC",
            placeholder_text_color="#64748B",
            corner_radius=8
        )
        self.name_entry.grid(row=3, column=0, padx=20, pady=(0, 15), sticky="ew")

        # Email Field
        self.email_label = ctk.CTkLabel(
            self.main_frame,
            text="Email",
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
            text_color="#CBD5E1"
        )
        self.email_label.grid(row=4, column=0, pady=(10, 2), padx=20, sticky="w")
        
        self.email_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="john@example.com",
            height=40,
            fg_color="#1E293B",
            border_color="#334155",
            text_color="#F8FAFC",
            placeholder_text_color="#64748B",
            corner_radius=8
        )
        self.email_entry.grid(row=5, column=0, padx=20, pady=(0, 15), sticky="ew")

        # Subject Field
        self.subject_label = ctk.CTkLabel(
            self.main_frame,
            text="Subject",
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
            text_color="#CBD5E1"
        )
        self.subject_label.grid(row=6, column=0, pady=(10, 2), padx=20, sticky="w")
        
        self.subject_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Project Inquiry",
            height=40,
            fg_color="#1E293B",
            border_color="#334155",
            text_color="#F8FAFC",
            placeholder_text_color="#64748B",
            corner_radius=8
        )
        self.subject_entry.grid(row=7, column=0, padx=20, pady=(0, 15), sticky="ew")

        # Message Field
        self.message_label = ctk.CTkLabel(
            self.main_frame,
            text="Message",
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
            text_color="#CBD5E1"
        )
        self.message_label.grid(row=8, column=0, pady=(10, 2), padx=20, sticky="w")
        
        self.message_text = ctk.CTkTextbox(
            self.main_frame,
            height=120,
            fg_color="#1E293B",
            border_color="#334155",
            border_width=1,
            text_color="#F8FAFC",
            corner_radius=8,
            font=ctk.CTkFont(family="Inter", size=12)
        )
        self.message_text.grid(row=9, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Feedback/Status Label
        self.feedback_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=ctk.CTkFont(family="Inter", size=12, weight="normal"),
            text_color="#E2E8F0"
        )
        self.feedback_label.grid(row=10, column=0, pady=(0, 10), padx=20, sticky="ew")

        # Submit Button
        self.submit_btn = ctk.CTkButton(
            self.main_frame,
            text="Send Message 🚀",
            font=ctk.CTkFont(family="Inter", size=14, weight="bold"),
            height=45,
            corner_radius=8,
            fg_color="#3B82F6",
            hover_color="#1D4ED8",
            text_color="#F8FAFC",
            command=self.submit_form
        )
        self.submit_btn.grid(row=11, column=0, padx=20, pady=(10, 30), sticky="ew")

    def validate_inputs(self, name, email, subject, message):
        """Validate form inputs."""
        if not name or name.strip() == "":
            return False, "Please enter your name."
        if not email or "@" not in email or "." not in email:
            return False, "Please enter a valid email address."
        if not subject or subject.strip() == "":
            return False, "Please enter a subject."
        if not message or message.strip() == "":
            return False, "Please enter a message."
        return True, ""

    def save_to_database(self, name, email, subject, message):
        """Insert the form submission into MySQL."""
        try:
            conn = mysql.connector.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', 'lohesvar'),
                database=os.getenv('DB_NAME', 'portfolio_db'),
                connect_timeout=3  # Fail fast if DB server is offline
            )
            cursor = conn.cursor()
            query = "INSERT INTO messages (name, email, subject, message) VALUES (%s, %s, %s, %s)"
            values = (name, email, subject, message)
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()
            return True, "Success"
        except mysql.connector.Error as err:
            print(f"Database error details: {err}")
            return False, str(err)

    def submit_form(self):
        # Retrieve form input values
        name = self.name_entry.get()
        email = self.email_entry.get()
        subject = self.subject_entry.get()
        message = self.message_text.get("1.0", "end-1c")

        # Validate inputs
        is_valid, err_msg = self.validate_inputs(name, email, subject, message)
        if not is_valid:
            self.feedback_label.configure(text=err_msg, text_color="#EF4444")
            return

        # Show loading/processing state
        self.feedback_label.configure(text="Processing...", text_color="#3B82F6")
        self.update_idletasks()

        # Step 1: Save to database
        db_success, db_err = self.save_to_database(name, email, subject, message)

        if db_success:
            self.feedback_label.configure(
                text="Message saved to database successfully!",
                text_color="#10B981"
            )
            # Clear inputs
            self.name_entry.delete(0, 'end')
            self.email_entry.delete(0, 'end')
            self.subject_entry.delete(0, 'end')
            self.message_text.delete('1.0', 'end')
        else:
            self.feedback_label.configure(
                text=f"Database save failed: {db_err[:40]}",
                text_color="#EF4444"
            )

if __name__ == "__main__":
    app = PortfolioContactApp()
    app.mainloop()
