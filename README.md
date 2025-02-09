# alfredAI

**alfredAI** is an AI-driven financial model update agent that automates Excel updates based on real-time email instructions. It processes incoming Gmail messages containing financial model edits, intelligently parses the instructions via an LLM-powered system, automates updates in Microsoft Excel, and cross-validates figures using real-time financial data from sec.gov. Designed to run locally, alfredAI prioritizes security and efficiency, making it ideal for high-stakes investment banking environments.

---

## Table of Contents

- [Features](#features)
- [Project Architecture](#project-architecture)
- [Installation & Environment Setup](#installation--environment-setup)
- [Configuration](#configuration)
- [Usage](#usage)
- [Testing](#testing)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Email Processing & Instruction Extraction:**  
  - Connects to Gmail via the Gmail API  
  - Parses email content with an LLM to extract structured financial model edit instructions

- **Excel Automation:**  
  - Automates updates in Microsoft Excel using libraries like xlwings and/or openpyxl  
  - Handles multiple edits, formulas, and formatting reliably

- **Real-Time Financial Data Retrieval:**  
  - Fetches current financial data from sec.gov (and can be extended to Bloomberg/Refinitiv)
  - Validates and cross-references Excel data for accuracy

- **Validation & Feedback:**  
  - Provides a user control layer for review/override before finalizing changes  
  - Implements robust error handling and logging

- **Local Operation:**  
  - Ensures data security and compliance with banking confidentiality standards

---

## Project Architecture

The project is divided into the following modules:

- **Email Processing (`src/email_processor/`):**  
  - `gmail_connector.py`: Manages Gmail API authentication and email retrieval.  
  - `instruction_parser.py`: Uses an LLM to extract actionable instructions from emails.

- **Excel Automation (`src/excel_automation/`):**  
  - `excel_handler.py`: Contains functions for opening and modifying Excel workbooks.  
  - `validation.py` & `error_handler.py`: Implement error handling and data validation.

- **Real-Time Financial Data Retrieval (`src/data_retrieval/`):**  
  - `sec_fetcher.py`: Fetches financial data from sec.gov.  
  - `data_validator.py`: Validates data before updates are committed.

- **UI & User Control (`src/ui_control/`):**  
  - `user_interface.py`: Provides a GUI for manual review and override of automated changes.

- **Utilities (`src/utils/`):**  
  - `logger.py`: Handles logging throughout the project.

Test cases are provided under the `tests/` directory for each module.

---

## Installation & Environment Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/alfredAI.git
   cd alfredAI
   ```

2. **Create a Virtual Environment:**

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment:**

   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```

4. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

1. **Gmail API Credentials:**

   - Place your OAuth2 credentials file in `config/gmail_credentials.json`.
   - Follow the [Google API documentation](https://developers.google.com/gmail/api/quickstart/python) to obtain your credentials.

2. **General Configuration:**

   - Edit `config/config.yaml` to set up any additional parameters (e.g., API keys, file paths, and other settings).

---

## Usage

1. **Start the Application:**

   - Run the main entry point from the terminal:

     ```bash
     python src/main.py
     ```

2. **Workflow Overview:**

   - **Email Processing:**  
     alfredAI fetches and processes relevant emails from Gmail.
     
   - **Excel Automation:**  
     The agent opens the target Excel workbook, applies parsed instructions, and validates changes.
     
   - **Real-Time Data Retrieval:**  
     Concurrently, it fetches real-time financial data from sec.gov and validates Excel figures.
     
   - **User Control:**  
     A simple GUI (or CLI) will prompt you to review and approve the changes before finalizing.

3. **Using Cursor:**

   - Utilize Cursor’s integrated terminal, debugging tools, and file explorer to navigate and modify the code as needed.  
   - Refer to the inline documentation and comments throughout the codebase for further guidance.

---

## Testing

- **Unit Tests:**
  
  - Test modules can be found in the `tests/` directory.
  - Run tests using a testing framework like `pytest`:

    ```bash
    pytest tests/
    ```

- **Integration Tests:**
  
  - Simulate end-to-end workflows with sample emails and Excel files to ensure all modules interact correctly.

---

## Future Enhancements

- **Enhanced AI Reasoning:**  
  - Integrate more advanced LLM models for deeper financial modeling decisions.

- **Additional Data Sources:**  
  - Extend support for Bloomberg/Refinitiv APIs for comprehensive data validation.

- **Voice-Command Capabilities:**  
  - Explore integrating voice commands using libraries such as `SpeechRecognition`.

- **Improved UI:**  
  - Consider developing a web-based dashboard for a richer user experience.

---

## Contributing

Contributions are welcome! If you have ideas for improvements or find issues, please create an issue or submit a pull request. Make sure to follow the project’s code style and include appropriate tests.

---

## License

[MIT License](LICENSE)

---

## Acknowledgements

- **Google APIs:** For Gmail integration.
- **xlwings/openpyxl:** For Excel automation.
- **Sec.gov & Financial APIs:** For real-time data retrieval.
- **Cursor:** For providing a streamlined development environment.
