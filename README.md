# AI Resume Builder

A modern, AI-powered resume builder that creates professional resumes from free-form text input. Built with Python Flask backend, React frontend, and powered by Groq's LLM API.

![AI Resume Builder](https://img.shields.io/badge/AI-Powered-blue?style=for-the-badge&logo=openai)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![React](https://img.shields.io/badge/React-18.2.0-blue?style=for-the-badge&logo=react)
![Flask](https://img.shields.io/badge/Flask-3.1.1-green?style=for-the-badge&logo=flask)

## ✨ Features

- **AI-Powered Content Generation**: Uses Groq's LLM to generate professional summaries and structure resume content
- **Multiple Output Formats**: Generate resumes in PDF, Markdown, and JSON formats
- **Interactive Web Interface**: Modern React frontend with Material-UI components
- **Professional PDF Generation**: Clean, formatted PDF output with proper styling
- **Flexible Input**: Accept free-form text descriptions and convert them into structured resume data
- **Real-time Processing**: Instant resume generation with live preview

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Groq API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/resume-builder.git
   cd resume-builder
   ```

2. **Set up Python environment**
   ```bash
   python -m venv resume_builder_env
   # On Windows
   resume_builder_env\Scripts\activate
   # On macOS/Linux
   source resume_builder_env/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install flask flask-cors langchain-groq pydantic reportlab python-dotenv
   ```

4. **Set up frontend**
   ```bash
   cd frontend
   npm install
   ```

5. **Configure environment variables**
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

### Running the Application

1. **Start the Flask backend**
   ```bash
   python app.py
   ```
   The backend will run on `http://localhost:5000`

2. **Start the React frontend**
   ```bash
   cd frontend
   npm run dev
   ```
   The frontend will run on `http://localhost:5173`

3. **Access the application**
   Open your browser and navigate to `http://localhost:5173`

## 📖 Usage

### Web Interface

1. Fill in your personal information (name, email, phone)
2. Enter your skills and experience in the text area
3. Click "Generate Resume" to create your professional resume
4. Download the generated resume in PDF, Markdown, or JSON format

### Command Line Interface

The project also supports command-line usage:

#### Interactive Mode
```bash
python main.py --interactive
```

#### File Input Mode
```bash
python main.py --input input_data.json --output-md resume.md --output-pdf resume.pdf
```

Example input JSON:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "raw_text": "Experienced software engineer with 5 years in Python development..."
}
```

## 🏗️ Project Structure

```
resume-builder/
├── app.py                 # Flask web server
├── main.py               # Command-line interface
├── builder.py            # AI content generation
├── parser.py             # Resume data parsing
├── models/
│   └── resume_schema.json # JSON schema for resume structure
├── frontend/
│   ├── App.jsx           # React main component
│   ├── main.jsx          # React entry point
│   ├── package.json      # Frontend dependencies
│   └── *.css            # Styling files
└── resume_builder_env/   # Python virtual environment
```

## 🔧 Technical Details

### Backend Architecture

- **Flask**: Web server and API endpoints
- **LangChain**: LLM integration and prompt management
- **Groq API**: AI model for content generation
- **ReportLab**: PDF generation
- **Pydantic**: Data validation and parsing

### Frontend Architecture

- **React 18**: Modern UI framework
- **Material-UI**: Component library
- **Vite**: Build tool and development server

### AI Integration

The application uses Groq's LLM API with two main prompts:

1. **Summary Generation**: Creates concise professional summaries
2. **Structured Resume**: Converts free-form text into structured JSON data

### Output Formats

- **PDF**: Professional formatted document with proper styling
- **Markdown**: Clean, readable format for version control
- **JSON**: Structured data for further processing

## 🛠️ Development

### Adding New Features

1. **Backend Changes**: Modify `builder.py` for AI logic, `app.py` for API endpoints
2. **Frontend Changes**: Update `App.jsx` for UI changes
3. **Schema Updates**: Modify `models/resume_schema.json` for data structure changes

### Testing

```bash
# Test backend
python main.py --interactive

# Test frontend
cd frontend
npm run dev
```

## 📝 API Endpoints

### POST /generate
Generates a resume from input data.

**Request Body:**
```json
{
  "name": "string",
  "email": "string",
  "phone": "string (optional)",
  "raw_text": "string"
}
```

**Response:**
```json
{
  "summary": "string",
  "resume_json": "object",
  "resume_md": "string",
  "pdf_url": "string",
  "md_url": "string",
  "json_url": "string"
}
```

### GET /download/{filetype}
Downloads generated files (pdf, md, json).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Groq](https://groq.com/) for providing the LLM API
- [LangChain](https://langchain.com/) for AI integration tools
- [Material-UI](https://mui.com/) for the component library
- [ReportLab](https://www.reportlab.com/) for PDF generation

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/resume-builder/issues) page
2. Create a new issue with detailed information
3. Include your Python version, Node.js version, and error messages

---

**Made with ❤️ by Salman Ali** 
