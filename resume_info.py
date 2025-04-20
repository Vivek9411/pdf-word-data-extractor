import re
import spacy
import fitz
from collections import defaultdict



# Load spaCy English model
nlp = spacy.load("person_only_model")

skills_list = [
    # Programming Languages
    'Python', 'Java', 'C++', 'C', 'C#', 'JavaScript', 'TypeScript', 
    'Go', 'Rust', 'Kotlin', 'Swift', 'Dart', 'Scala', 'Ruby', 'PHP',
    'Perl', 'R', 'MATLAB', 'Objective-C', 'Groovy', 'Julia', 'Haskell',
    'Elixir', 'Clojure', 'Lua', 'Erlang', 'F#', 'OCaml', 'Scheme', 'Bash',
    
    # Web Development
    'HTML5', 'CSS3', 'SASS', 'LESS', 'Bootstrap', 'Tailwind CSS', 'jQuery',
    'React', 'Angular', 'Vue.js', 'Svelte', 'Next.js', 'Nuxt.js', 'Gatsby',
    'Django', 'Flask', 'FastAPI', 'Spring', 'Laravel', 'Ruby on Rails',
    'Express.js', 'NestJS', 'ASP.NET', 'Phoenix', 'GraphQL', 'REST API',
    'WebSockets', 'WebRTC', 'WebAssembly', 'Progressive Web Apps',
    
    # Mobile Development
    'React Native', 'Flutter', 'Android Development', 'iOS Development',
    'SwiftUI', 'Kotlin Multiplatform', 'Xamarin', 'Ionic', 'Cordova',
    
    # Database Technologies
    'SQL', 'MySQL', 'PostgreSQL', 'SQLite', 'Oracle', 'Microsoft SQL Server',
    'MongoDB', 'Redis', 'Cassandra', 'Elasticsearch', 'Neo4j', 'Firebase',
    'DynamoDB', 'Cosmos DB', 'MariaDB', 'HBase', 'CouchDB', 'InfluxDB',
    'ArangoDB', 'RethinkDB', 'Amazon Redshift', 'Snowflake', 'BigQuery',
    
    # DevOps & Cloud
    'AWS', 'Azure', 'Google Cloud', 'Docker', 'Kubernetes', 'Terraform',
    'Ansible', 'Puppet', 'Chef', 'Jenkins', 'GitLab CI/CD', 'GitHub Actions',
    'CircleCI', 'Travis CI', 'ArgoCD', 'Helm', 'Istio', 'Prometheus',
    'Grafana', 'ELK Stack', 'Splunk', 'Nagios', 'Zabbix', 'Pulumi',
    'OpenStack', 'Serverless', 'CloudFormation', 'Azure DevOps',
    
    # Data Science & AI/ML
    'Machine Learning', 'Deep Learning', 'Natural Language Processing',
    'Computer Vision', 'TensorFlow', 'PyTorch', 'Keras', 'Scikit-learn',
    'Pandas', 'NumPy', 'SciPy', 'Matplotlib', 'Seaborn', 'Plotly',
    'OpenCV', 'NLTK', 'spaCy', 'HuggingFace', 'Apache Spark', 'Hadoop',
    'Hive', 'Pig', 'Flink', 'Kafka', 'Airflow', 'MLflow', 'DVC',
    'Tableau', 'Power BI', 'Looker', 'Dataiku', 'Alteryx', 'RapidMiner',
    
    # Cybersecurity
    'Ethical Hacking', 'Penetration Testing', 'OWASP', 'Burp Suite',
    'Metasploit', 'Kali Linux', 'Wireshark', 'Nmap', 'SIEM', 'Splunk',
    'Cryptography', 'Blockchain Security', 'Zero Trust', 'IAM',
    'Firewalls', 'VPN', 'IDS/IPS', 'SOC', 'Threat Intelligence',
    
    # Blockchain
    'Solidity', 'Ethereum', 'Hyperledger', 'Smart Contracts', 'Web3',
    'Truffle', 'Hardhat', 'IPFS', 'DeFi', 'NFTs', 'DApp Development',
    
    # Game Development
    'Unity', 'Unreal Engine', 'CryEngine', 'Godot', 'DirectX', 'OpenGL',
    'Vulkan', 'AR/VR Development', 'Blender', 'Maya', '3D Modeling',
    
    # Embedded & IoT
    'Embedded C', 'Arduino', 'Raspberry Pi', 'RTOS', 'VxWorks',
    'Microcontroller Programming', 'IoT Protocols', 'MQTT', 'CoAP',
    'Industrial IoT', 'Robotics', 'ROS', 'FPGA', 'Verilog', 'VHDL',
    
    # Networking
    'TCP/IP', 'DNS', 'HTTP/HTTPS', 'BGP', 'OSPF', 'MPLS', 'VPN',
    'SD-WAN', 'VoIP', '5G', 'WiFi', 'Bluetooth', 'Zigbee',
    
    # Software Engineering Practices
    'Agile', 'Scrum', 'Kanban', 'SAFe', 'DevOps', 'CI/CD', 'TDD',
    'BDD', 'DDD', 'Microservices', 'Monolith Architecture', 'SOA',
    'Design Patterns', 'Clean Code', 'Refactoring', 'Code Review',
    'Pair Programming', 'Extreme Programming', 'Git Flow',
    
    # Testing
    'Unit Testing', 'Integration Testing', 'E2E Testing', 'Selenium',
    'Cypress', 'Jest', 'Mocha', 'JUnit', 'TestNG', 'Pytest',
    'Load Testing', 'JMeter', 'Gatling', 'Security Testing',
    'Accessibility Testing', 'Usability Testing',
    
    # Soft Skills
    'Problem Solving', 'Critical Thinking', 'Communication', 'Teamwork',
    'Leadership', 'Time Management', 'Project Management', 'Mentoring',
    'Public Speaking', 'Technical Writing', 'Negotiation',
    
    # Emerging Technologies
    'Quantum Computing', 'Edge Computing', 'Serverless Computing',
    'Digital Twins', 'Metaverse Development', 'Generative AI',
    'Large Language Models', 'AI Ethics', 'Explainable AI',
    'Autonomous Systems', 'Computer Vision', 'Robotic Process Automation',
    
    # Enterprise Technologies
    'SAP', 'Salesforce', 'Oracle ERP', 'Microsoft Dynamics', 'Workday',
    'ServiceNow', 'MuleSoft', 'TIBCO', 'IBM WebSphere', 'Mainframe',
    'COBOL', 'Fortran', 'PowerShell', 'Active Directory', 'Exchange Server',
    
    # Miscellaneous
    'Technical Documentation', 'UX/UI Design', 'Figma', 'Adobe XD',
    'Sketch', 'Jira', 'Confluence', 'Trello', 'Asana', 'Slack',
    'Microsoft Teams', 'Zoom', 'Webex', 'Virtual Collaboration',
    'Remote Work Tools', 'Low-Code Platforms', 'No-Code Platforms'
]


def extract_text_from_pdf(pdf_path):
    """Extract text with inline links using PyMuPDF"""
    doc = fitz.open(pdf_path)
    full_text = ""

    for page in doc:
        words = page.get_text("words")
        links = page.get_links()

        link_map = []
        for link in links:
            if 'uri' in link:
                rect = fitz.Rect(link['from'])
                link_map.append((rect, link['uri']))

        for w in words:
            word_rect = fitz.Rect(w[:4])
            word_text = w[4]
            linked = False

            for rect, uri in link_map:
                if rect.intersects(word_rect):
                    full_text += f"{word_text} ({uri}) "
                    linked = True
                    break

            if not linked:
                full_text += word_text + " "

        full_text += "\n\n"
    return full_text.strip()



def extract_name(text):
    # Get the first 3 lines to look for the name
    lines = text.strip().split('\n')[:5]
    name_candidates = []

    # Fallback to spaCy
    # print(text)
    doc = nlp(text)
    for i in doc.ents:
        print(i.text, i.label_)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text

    return "Name not found"


def extract_github_links(text):
    """Extract GitHub profile URLs and remove any additional paths"""
    pattern = r'https?://(?:www\.)?github\.com/([a-zA-Z0-9_-]+)'
    matches = re.findall(pattern, text)
    # Reconstruct full GitHub profile URLs
    return list(set(f"https://github.com/{username}" for username in set(matches)))



def extract_linkedin_links(text):
    """Extract LinkedIn profiles using regex"""
    pattern = r'https?://(?:www\.)?linkedin\.com/in/([a-zA-Z0-9_-]+)'
    matches = re.findall(pattern, text)
    return list(set(f"https://linkedin.com/in/{match}" for match in matches))


def extract_mobile_numbers(text):
    """Extract phone numbers using regex"""
    pattern = r'\b(?:\+91[-\s]?|0)?[6-9]\d{9}\b'
    return list(set(re.findall(pattern, text)))


def extract_email_addresses(text):
    """Extract emails using regex"""
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return list(set(re.findall(pattern, text)))


def extract_skills(text, skills_list=skills_list):
    """Extract skills using NLP and optional skills list"""
    doc = nlp(text.lower())
    skills_found = set()

    # Match against skills list
    for skill in skills_list:
        if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text.lower()):
            skills_found.add(skill)

    # Extract technical nouns
    for token in doc:
        if token.text.istitle() and token.dep_ in ("dobj", "pobj"):
            skills_found.add(token.text)

    return sorted(skills_found)



# in next task 
def extract_work_experience(text):
    """Extract work experience using NLP and pattern matching"""
    doc = nlp(text)
    experiences = []
    current_exp = {}
    
    # Look for section headers
    exp_section = ""
    for sent in sent_tokenize(text):
        if re.search(r'(work|professional|employment) (experience|history)', sent, re.I):
            exp_section = text[text.find(sent):]
            break
    
    if not exp_section:
        return experiences
    
    # Process with spaCy
    exp_doc = nlp(exp_section)
    
    # Extract organizations and dates
    orgs = [ent.text for ent in exp_doc.ents if ent.label_ == "ORG"]
    dates = [ent.text for ent in exp_doc.ents if ent.label_ == "DATE"]
    
    # Find job titles (heuristic)
    titles = []
    for token in exp_doc:
        if token.text.istitle() and token.dep_ in ("compound", "nsubj", "dobj"):
            titles.append(token.text)
    
    # Simple pattern matching for job entries
    pattern = r'(?i)(.*?)\s*(?:at|in|,)\s*(.*?)\s*(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|\d).*?\s*-\s*(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|\d|present)'
    for match in re.finditer(pattern, exp_section):
        title, company = match.groups()
        if title.strip() and company.strip():
            experiences.append({
                'position': clean_text(title),
                'company': clean_text(company),
                'duration': extract_duration(match.group(0))
            })
    
    return experiences

# in next task
def extract_duration(text):
    """Extract duration dates from text"""
    dates = re.findall(r'(\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s*\d{4}\b|\d{1,2}/\d{4})', text, re.I)
    if len(dates) >= 2:
        return f"{dates[0]} - {dates[1]}"
    elif dates:
        return dates[0]
    return ""


# in next task
def extract_education(text):
    """Extract education using NLP"""
    doc = nlp(text)
    education = []
    
    # Look for education section
    edu_section = ""
    for sent in sent_tokenize(text):
        if re.search(r'(education|academic background|qualifications)', sent, re.I):
            edu_section = text[text.find(sent):]
            break
    
    if not edu_section:
        return education
    
    # Process with spaCy
    edu_doc = nlp(edu_section)
    
    # Extract organizations and degrees
    for sent in edu_doc.sents:
        if any(word.text.lower() in ['university', 'college', 'institute', 'school'] for word in sent):
            education.append({
                'degree': extract_degree(sent.text),
                'institution': extract_institution(sent.text),
                'duration': extract_duration(sent.text)
            })
    
    return education


# in next task
def extract_degree(text):
    """Extract degree from education text"""
    doc = nlp(text)
    for token in doc:
        if token.text.istitle() and token.dep_ in ("compound", "nsubj"):
            return token.text
    return ""
# in next task
def extract_institution(text):
    """Extract institution from education text"""
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "ORG":
            return ent.text
    return ""
# in next task
def extract_projects(text):
    """Extract projects using NLP and pattern matching"""
    doc = nlp(text)
    projects = []
    
    # Look for projects section
    proj_section = ""
    for sent in sent_tokenize(text):
        if re.search(r'(projects|personal projects)', sent, re.I):
            proj_section = text[text.find(sent):]
            break
    
    if not proj_section:
        return projects
    
    # Simple pattern matching for projects
    pattern = r'(?i)^\s*(.*?)\s*(?:\(([^)]*)\))?\s*[-•·∙]\s*(.*?)(?=\n\s*(?:\w|\d))'
    for match in re.finditer(pattern, proj_section, re.MULTILINE | re.DOTALL):
        title, tech, desc = match.groups()
        projects.append({
            'title': clean_text(title),
            'technologies': clean_text(tech) if tech else "",
            'description': clean_text(desc)
        })
    
    return projects


# final function to be imported in app.py 

def extract_resume_data(file_name:str):
    ''' This function first extracts the text from the given file then take returns the infromation like name , mobile_number, email, githublink, linkedin_link, skills'''
    results = []
    # file_name name of file upladed

    text = extract_text_from_pdf(file_name)
    name = extract_name((' ').join(text.split('\n')[:5]))
    if name=='Name not found':
        name = extract_name(text)
    print(text.split('\n')[:5])
    mobile_number= extract_mobile_numbers(text)
    email = extract_email_addresses(text)
    linked = extract_linkedin_links(text)
    github = extract_github_links(text)
    skills = extract_skills(text)
    print(name)
    print(mobile_number)
    print( email)
    print( linked)
    print( github)
    print( skills)
    return {
        'name':name, 
        'mobile_number':mobile_number,
        'email':email,
        'linkedin_link':linked,
        'github_link':github,
        'skills':skills
        }


