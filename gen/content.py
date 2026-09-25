"""Every fact about Hari Priya, written once.

build.py and panels.py fill these into the artboard: the sidebar, the contact
panel, the bulletin board, the projects terminal, the skills archive, the studio
wall and the resume panel. Change something here, run python3 gen/build.py, and
nothing else holds a second copy.

Values starting /_blob/<id> are files in static/_blob/, named <id>.<ext>.
"""

# ---- who ----
NAME = "HARI PRIYA"
ROLE = "Software Engineer"
EMAIL = "itsharipriya8919@gmail.com"
LINKEDIN_URL = "https://www.linkedin.com/in/haripriya-pb/"
LINKEDIN_TEXT = "linkedin.com/in/haripriya-pb"

# ---- the resume panel ----
#: resume/resume.pdf, served by DOWNLOAD PDF
RESUME_PDF_BLOB = "/_blob/0d752e1888e7dacdc88dd106a17362fb"
#: out/resume-page-N.png, the same PDF's pages as images (gen/resume_pages.js)
RESUME_PAGES = [
    "/_blob/55930142619d0ddabc69451c241e762f",
    "/_blob/3df64a6d88fe4f43c3836fb9e775d86e",
]

# ---- the cavern panels ----
#: the bulletin board, newest first
EXPERIENCE = [{'title': 'SOFTWARE DEVELOPMENT ENGINEER',
  'where': 'Tata 1mg · Bangalore',
  'dates': 'Oct 2022 to Jun 2025',
  'card': '#fdf8ec',
  'pin': '#dc2626',
  'bullets': ['Built backend workflows and integrations for ODIN, a warehouse platform covering inventory, '
              'order fulfilment, procurement and supply chain',
              'Kafka event-driven integration with the Purchasing Service, automating purchase-order '
              'status sync across distributed services',
              'Picker-to-Packer handover for scanned orders, one manual step removed, ₹6 lakh/month saved '
              '(~£4,600)',
              'SKU barcoding across warehouse operations, cutting manpower cost by ₹20 lakh (~£15,000)',
              'Automated the Re-GRN workflow: 40%+ less manual effort, 15+ minutes saved per GRN',
              'Vendor-level financial segregation across 50+ vendors, lifting reconciliation accuracy 25%+',
              'Scaled the SKU Audit app to 10K+ SKUs/month; cut Patient Support Program turnaround 50%',
              'On-call for 15+ production incidents a month; mentored 3+ junior engineers']},
 {'title': 'SOFTWARE ENGINEER',
  'where': 'Tata Digital Health · Bangalore',
  'dates': 'Jul 2021 to Oct 2022',
  'card': '#e6f1fb',
  'pin': '#2563eb',
  'bullets': ['Backend REST APIs for a patient- and doctor-facing telemedicine platform running 1,000+ '
              'consultations a day, including digital prescriptions',
              'Demographic-based symptom prompts and language matching across 4+ languages, 15%+ faster '
              'setup, wider access',
              'Single Sign-On across platforms, plus push notifications for appointments and consultation '
              'updates']},
 {'title': 'SOFTWARE ENGINEERING INTERN',
  'where': 'Cognizant · India',
  'dates': 'Feb 2021 to Jun 2021',
  'card': '#fdeef3',
  'pin': '#dc2626',
  'bullets': ['Backend services in Java, Spring Boot, Spring Data JPA and Hibernate, test-driven with '
              'JUnit',
              'Led a 4-member project team and earned a return offer as Programmer Analyst Trainee']}]

#: the green card at the bottom of the board
EDUCATION_CARD = {'card': '#e8f7ea',
 'pin': '#16a34a',
 'title': 'EDUCATION',
 'org': 'Manchester, UK · Tamil Nadu, India'}
EDUCATION = [{'degree': 'MSc Advanced Computer Science',
  'where': 'University of Manchester',
  'dates': 'Sep 2025 to Sep 2026',
  'note': 'Global Future Scholarship'},
 {'degree': 'BTech Information Technology',
  'where': 'Sona College of Technology',
  'dates': '2017 to 2021',
  'note': 'CGPA 8.92 / 10'}]

#: the terminal in the projects hub
PROJECTS = [{'num': '01',
  'slug': 'nutrivision',
  'name': 'NUTRIVISION',
  'tag': 'MSc project',
  'desc': 'Adapted BLIP-2 for automated dietary assessment using LoRA fine-tuning, benchmarked across five '
          'tasks on the Nutrition5K dataset.',
  'desc2': 'Added a zero-cost inference-time pipeline that improved dietary reasoning with no extra '
           'training or parameters.',
  'stack': ['PyTorch', 'Hugging Face PEFT', 'BLIP-2', 'LoRA']},
 {'num': '02',
  'slug': 'health-monitor',
  'name': 'HEALTHCARE MONITORING',
  'tag': 'Published · IJPRSE',
  'desc': "Full-stack app predicting a patient's health-risk level from biometrics: age, BMI, blood "
          'pressure, pulse and temperature.',
  'desc2': 'Decision Tree classifier with Pandas/NumPy preprocessing, served behind a Bootstrap interface '
           'for real-time classification.',
  'stack': ['Python', 'Flask', 'scikit-learn', 'Pandas']},
 {'num': '03',
  'slug': 'sentiment-lens',
  'name': 'SENTIMENT ANALYSIS',
  'tag': 'AFINN & WordNet',
  'desc': 'Desktop app pulling live tweets and classifying them positive, negative or neutral with AFINN '
          'and SentiWordNet.',
  'desc2': 'NLTK tokenising, POS tagging, lemmatising and stemming, with the split charted in Matplotlib.',
  'stack': ['Python', 'Tkinter', 'Tweepy', 'NLTK']},
 {'num': '04',
  'slug': 'healdroid',
  'name': 'HEALDROID',
  'tag': 'IoT',
  'desc': 'Arduino/ESP8266 rig streaming heart rate and body temperature to ThingSpeak over WiFi.',
  'desc2': 'Companion Android app in Java for real-time remote patient monitoring through the ThingSpeak '
           'API.',
  'stack': ['Arduino', 'ESP8266', 'Java', 'Android']}]

#: the skills archive panel: one shelf per group, one book per skill.
#: every book on a shelf shares the shelf's colour, so colour means group.
SKILL_SHELVES = [
    ("LANGUAGES", "#9f2b2b", ["Ruby", "Java", "Python", "SQL", "JavaScript"]),
    ("FRAMEWORKS", "#1e4f8a", ["Ruby on Rails", "Spring Boot", "Spring MVC", "Spring Data JPA", "Hibernate"]),
    ("DATA & MESSAGING", "#2f6b3f", ["PostgreSQL", "MySQL", "MongoDB", "Redis", "Apache Kafka", "SNS / SQS", "Sidekiq"]),
    ("ARCHITECTURE", "#8a5a12", ["Microservices", "Event-driven", "Distributed systems", "REST APIs", "SOLID"]),
    ("CLOUD & DEVOPS", "#1f6b6b", ["AWS", "Docker", "Kubernetes", "Jenkins", "CI/CD", "Linux", "Bash"]),
    ("TESTING", "#6b3fa0", ["JUnit", "RSpec", "Mockito", "TDD"]),
    ("ML & AI", "#8a2f5e", ["PyTorch", "Hugging Face", "LLMs & VLMs", "PEFT / LoRA", "scikit-learn", "Pandas", "NumPy"]),
]
#: the line under the last shelf
SKILL_EXTRAS = ["Sentry", "New Relic", "Kibana", "CloudWatch", "Postman", "Swagger", "Git",
                "Agile & Scrum", "NLTK", "Matplotlib"]

#: spines on the bookshelf
SKILL_BOOKS = ['RUBY',
 'RAILS',
 'JAVA',
 'SPRING',
 'PYTHON',
 'KAFKA',
 'REDIS',
 'SQL',
 'AWS',
 'DOCKER',
 'K8S',
 'TORCH',
 'LINUX',
 'GIT',
 'REST',
 'TDD']

#: the studio wall. alt text describes each piece for anyone using a screen reader.
ARTWORKS = [
    {"blob": "/_blob/8dfeba9369e2654443af72428647b461",
     "alt": "Profile of a girl in a ribbed beanie and scarf, ink and pencil"},
    {"blob": "/_blob/7115d2fdb7fceaaa9b9a22e98b719f94",
     "alt": "A pug resting its head, graphite"},
    {"blob": "/_blob/d1b099a003622ad9dccdd2227f59f0e8",
     "alt": "Study of a neck and collarbone, graphite"},
    {"blob": "/_blob/cd799374d79c52c6b97c58ecf61efe7a",
     "alt": "Portrait of a woman looking to one side, graphite"},
    {"blob": "/_blob/1ba8a0057014a2a677da5d85e5df0775",
     "alt": "Baby Groot, ballpoint pen"},
    {"blob": "/_blob/f380847db4e0dcbb98d90a901d2aa3d3",
     "alt": "Sun and moon in facing triangles, watercolour"},
    {"blob": "/_blob/67a33b0efd81125a2d56326bd232a0bc",
     "alt": "Four face studies on one sketchbook page, pencil"},
    {"blob": "/_blob/ee5745887b8fae37ecd557113ecb8e19",
     "alt": "Portrait with hair falling across the face, graphite"},
    {"blob": "/_blob/436c6c596e8e0ad7e8c4198c81331372",
     "alt": "A bird on a street lamp beneath a swirling sky, after Van Gogh, graphite"},
]
