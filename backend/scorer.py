from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel
import spacy
import torch

nlp = spacy.load("en_core_web_sm")

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

def get_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(text)
    return sentiment['compound']

def extract_skills(text):
    doc = nlp(text)

    cs_skills = set([
        # Programming Languages
        "python", "java", "c++", "javascript", "html", "css", "sql", "ruby", "r", "swift", "typescript", 
        "go", "dart", "php", "kotlin", "bash", "perl", "matlab", "haskell", "rust", "objective-c", "scala", 
        "lua", "clojure", "julia", "elixir", "f#", "sql", "vhdl", "c", "actionscript", "solidity",
        
        # Web Development
        "html", "css", "javascript", "react", "angular", "vue.js", "node.js", "express", "next.js", "svelte", 
        "graphql", "webassembly", "ember.js", "bootstrap", "tailwind", "ajax", "api", "rest api", "web sockets", 
        "json", "xml", "http", "https", "sass", "less", "babel", "webpack", "parcel", "grunt", "gulp",
        
        # Frontend Frameworks and Libraries
        "react", "vue.js", "angular", "svelte", "ember.js", "backbone.js", "redux", "material-ui", "bootstrap", 
        "tailwind", "jquery", "d3.js", "three.js", "threejs", "chart.js", "p5.js", "leaflet.js",
        
        # Backend Technologies
        "node.js", "express", "django", "flask", "spring", "rails", "laravel", "asp.net", "play framework", 
        "hibernate", "spring boot", "tornado", "gin", "actix", "koa.js", "micronaut", "graphql", "graphql server", 
        "redis", "mongodb", "postgresql", "mysql", "oracle", "couchdb", "cassandra", "redis", "elasticsearch", 
        "firebase", "sqlite", "neo4j", "db2", "riak", "cockroachdb", "dynamoDB", "amazon rds", "mssql",
        
        # Cloud Platforms
        "aws", "azure", "google cloud", "digitalocean", "ibm cloud", "oracle cloud", "alibaba cloud", "vultr", 
        "heroku", "docker", "kubernetes", "terraform", "ansible", "chef", "puppet", "gitlab", "jenkins", "ci/cd", 
        "cloudformation", "cloudfront", "cloudwatch", "lambda", "ec2", "s3", "elasticsearch", "bigquery", "cloudflare",
        
        # DevOps Tools
        "docker", "kubernetes", "jenkins", "ansible", "terraform", "vagrant", "chef", "puppet", "gitlab", "bitbucket", 
        "circleci", "travis ci", "azure devops", "jira", "confluence", "bitbucket", "github actions", "nagios", 
        "prometheus", "grafana", "maven", "gradle", "crons", "saltstack", "etcd", "fluentd", "syslog", "zabbix",
        
        # Version Control and Collaboration
        "git", "github", "gitlab", "bitbucket", "svn", "mercurial", "tfs", "perforce", "jira", "trello", "asana", 
        "slack", "confluence", "notion", "zoom", "microsoft teams", "google drive", "dropbox", "box", "sharepoint",
        
        # Databases & Data Management
        "mysql", "postgresql", "mongodb", "cassandra", "redis", "sqlite", "oracle", "dynamoDB", "neo4j", "elasticsearch", 
        "hbase", "cockroachdb", "firebase", "db2", "mariadb", "apache kafka", "rabbitmq", "zookeeper", "etcd",
        
        # Data Science & Machine Learning
        "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn", "keras", "pandas", "numpy", 
        "matplotlib", "seaborn", "xgboost", "lightgbm", "nlp", "reinforcement learning", "computer vision", "keras", 
        "tensorflow", "opencsv", "fastai", "mlflow", "azure ml", "google ai", "openai", "huggingface", "pytorch-lightning",
        
        # Data Visualization & Analysis
        "tableau", "power bi", "matplotlib", "seaborn", "d3.js", "plotly", "ggplot2", "pandas", "numpy", "spss", "sas",
        "excel", "sql", "powerquery", "jq", "logstash", "elasticsearch", "splunk", "hadoop", "spark", "kafka", "apache flink", 
        "databricks", "apache hive", "redshift", "bigquery", "google analytics", "powerpivot", "plotly", "grafana",
        
        # Operating Systems & Environments
        "linux", "unix", "windows", "macos", "ios", "android", "docker", "virtualization", "bash", "powershell", 
        "cygwin", "vagrant", "qemu", "hyper-v", "vmware", "aws ec2", "azure vm", "lxc", "lxd", "raspberry pi", 
        "ubuntu", "centos", "debian", "redhat", "fedora", "arch", "mint", "manjaro", "kali", "ubuntu server", "fedora", 
        "opensuse", "gentoo", "homebrew",
        
        # Algorithms & Data Structures
        "data structures", "algorithms", "graphs", "binary trees", "hashmaps", "queues", "stacks", "sorting", "searching", 
        "dynamic programming", "greedy algorithms", "divide and conquer", "backtracking", "recursion", "hashing", 
        "bit manipulation", "combinatorics", "probability", "mathematics", "big O notation", "complexity analysis",
        
        # Cybersecurity
        "cybersecurity", "network security", "penetration testing", "firewalls", "encryption", "hashing", "cryptography", 
        "ssl", "tls", "http headers", "csrf", "xss", "sql injection", "ddos", "ethical hacking", "malware analysis", 
        "red team", "blue team", "security audit", "incident response", "osint", "hacking", "phishing", "social engineering",
        
        # Software Engineering & Methodologies
        "software engineering", "agile", "scrum", "kanban", "devops", "test-driven development", "bdd", "sdlc", "uml", 
        "design patterns", "solid principles", "microservices", "restful api", "soap", "swagger", "junit", "mocks", 
        "ci/cd", "jpa", "clean code", "pair programming", "gitflow", "kanban", "waterfall", "lean",
        
        # Testing and QA
        "unit testing", "integration testing", "end-to-end testing", "selenium", "cypress", "jest", "mocha", "chai", 
        "junit", "pytest", "testng", "mockito", "cucumber", "appium", "tox", "katalon", "load testing", "performance testing", 
        "security testing", "regression testing", "manual testing", "automated testing", "test automation", "junit",
        
        # Blockchain and Cryptocurrency
        "blockchain", "ethereum", "bitcoin", "smart contracts", "solidity", "web3", "nft", "cryptocurrency", "decentralized", 
        "consensus", "ipfs", "hyperledger", "ripple", "smart contract security", "erc20", "erc721", "decentralized apps", 
        "icos", "staking", "mining", "defi", "cryptography",
        
        # Game Development
        "unity", "unreal engine", "gamedev", "game design", "cocos2d", "godot", "blender", "directx", "opengl", 
        "game physics", "shader programming", "game optimization", "multiplayer", "game engine", "vr", "ar",
        
        # Other
        "api design", "openapi", "swagger", "graphql", "json", "xml", "yaml", "protobuf", "webhooks", "cloud-native", 
        "serverless", "load balancing", "microservices", "service mesh", "api gateway", "oauth", "jwt", "identity management"
    ])

    
    skills = set()
    
    skills.update([token.text.lower() for token in doc if token.text.lower() in cs_skills])
    skills.update([ent.text.lower() for ent in doc.ents if ent.label_ in ["ORG", "PRODUCT"] and ent.text.lower() in cs_skills])

    return list(skills)

def get_bert_embeddings(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings

def calculate_semantic_similarity(text1, text2):
    emb1 = get_bert_embeddings(text1)
    emb2 = get_bert_embeddings(text2)
    
    similarity = cosine_similarity(emb1, emb2)[0][0]
    return similarity

def get_resume_score_with_llm(resume_text, job_description):
    job_skills = extract_skills(job_description)
    
    resume_skills = extract_skills(resume_text)
    
    similarity = calculate_semantic_similarity(resume_text, job_description)
    
    resume_sentiment = get_sentiment(resume_text)
    job_sentiment = get_sentiment(job_description)
    
    sentiment_alignment = 1 - abs(resume_sentiment - job_sentiment)
    
    common_skills = set(resume_skills) & set(job_skills)
    skill_match_score = len(common_skills) / len(job_skills) if len(job_skills) > 0 else 0
    
    final_score = (similarity * 0.65 + sentiment_alignment * 0.1 + skill_match_score * 0.25) * 100
    
    return {
        "similarity": int(similarity * 100),
        "skill_match_score": int(skill_match_score * 100), 
        "final_score": int(final_score),
        "common_skills": list(common_skills)
    }

def get_resume_score(resume_text, job_description):
    return get_resume_score_with_llm(resume_text, job_description)
