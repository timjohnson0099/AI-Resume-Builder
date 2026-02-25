import argparse
import json
from builder import generate_summary, generate_structured_resume
from parser import parse_resume
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import re

def save_outputs(resume, raw_json_path, md_path, pdf_path):
    # 1) JSON + MD as before...
    raw_json = resume.json()
    with open(raw_json_path, 'w') as f:
        f.write(raw_json)
    with open(md_path, 'w') as f:
        f.write(f"# {resume.personal_info.name}\n\n")
        f.write(f"**Email:** {resume.personal_info.email}  \n")
        if resume.personal_info.phone:
            f.write(f"**Phone:** {resume.personal_info.phone}  \n")
        f.write("---\n\n")
        f.write(f"## Summary\n{resume.summary}\n\n")
        f.write("## Skills\n" + "\n".join(f"- {s}" for s in resume.skills) + "\n\n")
        if resume.experience:
            f.write("## Experience\n")
            for e in resume.experience:
                f.write(f"**{e.role}**, {e.company} ({e.start_date} - {e.end_date or 'Present'})\n\n")
                f.write(f"{e.description}\n\n")

    # 2) Pretty PDF generation (adapted from generate_pdfs.py) :contentReference[oaicite:2]{index=2}
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    margin = 50
    y = height - margin
    first_page = True

    def draw_line():
        nonlocal y
        c.line(margin, y, width - margin, y)
        y -= 20

    def add_wrapped_text(prefix=None, text="", font="Helvetica", size=10,
                         bold_prefix=False, indent=0):
        nonlocal y, first_page
        # Paginate if needed
        if y < margin + size + 10:
            c.showPage()
            y = height - margin
            first_page = False
            # no header on later pages

        c.setFont(font, size)
        full_text = f"{prefix}: {text}" if prefix else text
        words = full_text.split(" ")
        lines = []
        current = ""
        for w in words:
            test = (current + " " + w).strip()
            if c.stringWidth(test, font, size) <= (width - 2*margin - indent):
                current = test
            else:
                lines.append(current)
                current = w
        if current:
            lines.append(current)

        for line in lines:
            x = margin + indent
            if prefix and bold_prefix and line.startswith(f"{prefix}:"):
                # draw the prefix in bold, rest in normal
                c.setFont("Helvetica-Bold", size)
                prefix_text = f"{prefix}: "
                pw = c.stringWidth(prefix_text, "Helvetica-Bold", size)
                c.drawString(x, y, prefix_text)
                c.setFont(font, size)
                c.drawString(x + pw, y, line[len(prefix_text):])
            else:
                c.drawString(x, y, line)
            y -= size + 2

    def add_contact_info():
        nonlocal y
        c.setFont("Helvetica", 10)
        # phone | LinkedIn | Email
        contact = f"Phone: {resume.personal_info.phone or ''} | LinkedIn | Email"
        tw = c.stringWidth(contact, "Helvetica", 10)
        x = (width - tw) / 2

        # Phone
        c.drawString(x, y, f"Phone: {resume.personal_info.phone or ''}")
        x += c.stringWidth(f"Phone: {resume.personal_info.phone or ''} | ", "Helvetica", 10)

        # LinkedIn
        c.setFillColor(colors.blue)
        c.drawString(x, y, "LinkedIn")
        # assuming resume.personal_info.linkedin exists
        c.linkURL('https://www.linkedin.com/', 
                  (x, y-2, x + c.stringWidth("LinkedIn", "Helvetica", 10), y+10), 
                  relative=0)
        x += c.stringWidth("LinkedIn | ", "Helvetica", 10)

        # Email
        c.drawString(x, y, "Email")
        c.linkURL(f"mailto:{resume.personal_info.email}",
                  (x, y-2, x + c.stringWidth("Email", "Helvetica", 10), y+10),
                  relative=0)
        c.setFillColor(colors.black)
        y -= 15

    # First‐page header
    c.setFont("Helvetica-Bold", 16)
    header_x = (width - c.stringWidth(resume.personal_info.name, "Helvetica-Bold", 16)) / 2
    c.drawString(header_x, y, resume.personal_info.name)
    y -= 30

    # Contact line + divider
    add_contact_info()
    draw_line()

    # Summary
    add_wrapped_text("Summary", resume.summary, size=12, bold_prefix=True)
    draw_line()

    # (Skip Education section if you haven’t modeled it; otherwise:)
    # add_wrapped_text("Education", "", size=12, bold_prefix=True)
    # for edu in resume.education or []:
    #     add_wrapped_text(f"{edu.degree} - {edu.university}", 
    #                      f"GPA: {edu.gpa} ({edu.graduation_date})")
    # draw_line()

    # Technical Skills
    add_wrapped_text("Technical Skills", "", size=12, bold_prefix=True)
    add_wrapped_text("Skills", ", ".join(resume.skills), bold_prefix=True)
    draw_line()

    # Work Experience
    add_wrapped_text("Work Experience", "", size=12, bold_prefix=True)
    for exp in resume.experience or []:
        title = f"{exp.role} - {exp.company} ({exp.start_date} - {exp.end_date or 'Present'})"
        add_wrapped_text(title, "", bold_prefix=True)
        for bullet in exp.description.split(". "):
            if bullet.strip():
                add_wrapped_text("-", bullet.strip(), indent=10)
    draw_line()

    # Project Experience (if present)
    # add_wrapped_text("Project Experience", "", size=12, bold_prefix=True)
    # for proj in getattr(resume, "projects", []) or []:
    #     add_wrapped_text(proj.name, proj.description, bold_prefix=True)

    # Finish up
    c.save()
    print(f"Generated: {raw_json_path}, {md_path}, {pdf_path}")

def clean_raw_json(s: str) -> str:
    # Remove markdown fences and any leading/trailing text
    s = s.strip()
    # Remove ```json header/footer if present
    if s.startswith("```"):
        s = "\n".join(s.splitlines()[1:-1])
    return s

def interactive_mode(md_path, raw_json_path, pdf_path):
    name = input('Name: ')
    email = input('Email: ')
    phone = input('Phone (optional): ')
    print('Enter skills & experience paragraphs. End with blank line:')
    lines=[]
    while True:
        l = input()
        if not l.strip(): break
        lines.append(l)
    raw_text='\n'.join(lines)

    summary = generate_summary(raw_text)
    profile={'personal_info':{'name':name,'email':email,'phone':phone},'skills':[], 'experience':[]}
    # skills & experience are parsed from the structured JSON
    raw_json_str = generate_structured_resume(profile, summary, raw_text)
    raw_json_str = re.sub(r'<think>.*?</think>', '', raw_json_str, flags=re.DOTALL).strip()
    clean_json = clean_raw_json(raw_json_str)
    resume = parse_resume(clean_json)
    save_outputs(resume, raw_json_path, md_path, pdf_path)
    print(f"Outputs: {md_path}, {raw_json_path}, {pdf_path}")


def file_mode(input_path, md_path, raw_json_path, pdf_path):
    data = json.load(open(input_path))
    raw_text = data.pop('raw_text','')
    summary = data.get('summary') or generate_summary(raw_text)
    raw_json_str = generate_structured_resume(data, summary, raw_text)
    raw_json_str = re.sub(r'<think>.*?</think>', '', raw_json_str, flags=re.DOTALL).strip()
    clean_json = clean_raw_json(raw_json_str)
    resume = parse_resume(clean_json)
    save_outputs(resume, raw_json_path, md_path, pdf_path)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--interactive',action='store_true')
    group.add_argument('--input',type=str)
    parser.add_argument('--output-md',default='resume.md')
    parser.add_argument('--output-json',default='raw_resume.json')
    parser.add_argument('--output-pdf',default='resume.pdf')
    args=parser.parse_args()

    if args.interactive:
        interactive_mode(args.output_md, args.output_json, args.output_pdf)
    else:
        file_mode(args.input, args.output_md, args.output_json, args.output_pdf)