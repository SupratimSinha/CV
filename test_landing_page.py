import html.parser

class LandingPageTestParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.found_header = False
        self.found_nav = False
        self.found_main = False
        self.found_footer = False
        self.found_h1_supratim_sinha = False
        self.in_h1 = False
        self.found_nav_hobbies_link = False
        self.found_nav_contact_link = False
        self.in_nav = False
        self.found_h2_work_experience = False
        self.found_h2_skills = False
        self.in_h2 = False
        self.current_h2_text = ""
        self.found_todo_comment = False

    def handle_starttag(self, tag, attrs):
        if tag == "header":
            self.found_header = True
        elif tag == "nav":
            self.found_nav = True
            self.in_nav = True
        elif tag == "main":
            self.found_main = True
        elif tag == "footer":
            self.found_footer = True
        elif tag == "h1":
            self.in_h1 = True
        elif tag == "a" and self.in_nav:
            for attr_name, attr_value in attrs:
                if attr_name == "href" and attr_value == "hobbies.html":
                    self.found_nav_hobbies_link = True
                elif attr_name == "href" and attr_value == "contact.html":
                    self.found_nav_contact_link = True
        elif tag == "h2":
            self.in_h2 = True
            self.current_h2_text = "" # Reset for current h2

    def handle_endtag(self, tag):
        if tag == "h1":
            self.in_h1 = False
        elif tag == "nav":
            self.in_nav = False
        elif tag == "h2":
            if self.current_h2_text == "Work Experience":
                self.found_h2_work_experience = True
            elif self.current_h2_text == "Skills":
                self.found_h2_skills = True
            self.in_h2 = False
            self.current_h2_text = ""


    def handle_data(self, data):
        if self.in_h1 and "Supratim Sinha" in data:
            self.found_h1_supratim_sinha = True
        if self.in_h2:
            self.current_h2_text += data.strip()

    def handle_comment(self, data):
        if "TODO: Replace this with a meaningful bio" in data.strip():
            self.found_todo_comment = True

def run_tests():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        print("ERROR: index.html not found.")
        return

    parser = LandingPageTestParser()
    parser.feed(html_content)

    errors = []

    if not parser.found_header:
        errors.append("Missing <header> tag.")
    if not parser.found_nav:
        errors.append("Missing <nav> tag.")
    if not parser.found_main:
        errors.append("Missing <main> tag.")
    if not parser.found_footer:
        errors.append("Missing <footer> tag.")
    if not parser.found_h1_supratim_sinha:
        errors.append("Main heading <h1> with 'Supratim Sinha' not found or incorrect.")
    if not parser.found_nav_hobbies_link:
        errors.append("Navigation link to 'hobbies.html' not found in <nav>.")
    if not parser.found_nav_contact_link:
        errors.append("Navigation link to 'contact.html' not found in <nav>.")
    if not parser.found_h2_work_experience:
        errors.append("<h2>Work Experience</h2> section heading not found.")
    if not parser.found_h2_skills:
        errors.append("<h2>Skills</h2> section heading not found.")
    if not parser.found_todo_comment:
        errors.append("Placeholder comment '<!-- TODO: Replace this with a meaningful bio -->' not found.")

    if not errors:
        print("All checks passed! index.html structure is valid.")
    else:
        print("Landing page verification failed:")
        for error in errors:
            print(f"- {error}")

if __name__ == "__main__":
    run_tests()
    print("\nTo run this test script:")
    print("1. Ensure index.html is in the same directory as this script.")
    print("2. Execute the script using: python test_landing_page.py")
