import pandas as pd
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Load the CSV file
df = pd.read_csv('news_articles.csv')

# Sample training data for categorization (for demonstration)
training_data = [
    ("German far right hails 'historic' election victory in east", "Politics"),
    ("Striking images reveal depths of Titanic's slow decay", "Science"),
    ("Handler attacked by tiger at Australian theme park", "Animal"),
    ("Row over Olympic rings on Eiffel Tower plan", "Politics"),
    ("Russian 'spy whale' found dead off Norway", "Science"),
    ("Tens of thousands rally in Israel calling for hostage release deal", "Politics"),
    ("Meeting the Ukrainian recruits preparing for new battle", "Politics"),
    ("Defending champion Coco Gauff crashes out of US Open", "Sports"),
    ("Record-breaking super Sunday for GB at Paralympics", "Sports"),
    ("Paralympics triathlon postponed because of water quality", "Sports"),
    ("Pregnant para-archer Grinham secures Paris bronze", "Sports"),
    ("'The howls were terrifying': Imprisoned in the notorious 'House of Mirrors'", "Crime"),
    ("Málaga tourism: 'People feel the city is collapsing'", "Travel"),
    ("Thailand wages war against 'alien' tilapia fish", "Environment"),
    ("The earliest pictures capturing the art and beauty of Indian monuments", "Culture"),
    ("'A tech firm stole our voices - then cloned and sold them'", "Technology"),
    ("Will more stars boycott Dubai after rapper Macklemore?", "Entertainment"),
    ("A £400m reunion? The potential risks and rewards of Oasis tour", "Entertainment"),
    ("UK and EU airports are sticking with 100ml liquid rule - but why?", "Travel"),
    ("Kamala Harris criticises Trump over Arlington Cemetery dispute", "Politics"),
    ("Publishers and authors sue over Florida book ban law", "Politics"),
    ("China and Philippines trade blame as ships collide", "International"),
    ("Norway's Princess Märtha Louise weds American shaman", "Entertainment"),
    ("'Provided leaked paper': Rajasthan PSC ex-official held for helping his kids 'top' exam", "Crime"),
    ("Why its ‘love for sisters’ can help NDA win Maharashtra", "Politics"),
    ("I won't forgive Dhoni': Yuvraj's father Yograj criticizes former India captain", "Sports"),
    ("Telangana rain: How quick-thinking cops saved man from drowning", "Local"),
    ("'Like a sonar ping': Stranded Nasa astronaut hears 'strange noises' from Boeing Starliner", "Science"),
    ("Will J&K govt meet the same fate as that of Delhi's after polls?", "Politics"),
    ("SBI launches new FASTag to reduce travel time on highways: Who can use", "Finance"),
    ("Paris Paralympics September 2: India's Full Schedule", "Sports"),
    ("Chitale Bandhu’s 75th with Sachin Tendulkar", "Entertainment"),
    ("Shopping: Intel Laptops Sale! Discounts up to 35% on High Performance Laptops", "Technology"),
    ("ISB Product Management with AI and GenAI", "Education"),
    ("After a tirade against Dhoni, Yograj Singh criticizes Kapil Dev", "Sports"),
    ("'ED team has reached my house to arrest me,' claims AAP MLA Amanatullah Khan", "Crime"),
    ("HDFC Bank takes 'temporary break' from its Apple iPhone partnership", "Finance"),
    ("Best Collagen Powders: Top Picks For Health and Beauty", "Health"),
    ("BSE Sensex hits lifetime high of above 82,700; Nifty50 crosses 25,300", "Finance"),
    ("Latest poll data: Kamala gains upper hand in key swing states, Trump trails", "Politics"),
    ("India's call whether to hand over Hasina or not: Bangladesh interim govt", "International"),
    ("Veteran journalist Umesh Upadhyay dies in freak mishap", "Local"),
    ("Kolkata rape-murder: Prime accused Sanjay Roy wants to plead not guilty, says lawyer", "Crime"),
    ("Trump feels left out as wife Melania and son Barron speak in secret code: 'It annoys him'", "Entertainment"),
    ("Flipkart Big Billion Days 2024 Sale Date Leaks", "Technology"),
    ("Garena Free Fire Max Redeem Codes for September 2", "Gaming"),
    ("Best Cargo Pants for Men: Comfort Meets Versatility", "Fashion"),
    ("Best Watches for Women Under 5000: Stylish Statements to Make Every Second Count", "Fashion"),
    ("Telangana schools to remain closed tomorrow amid heavy rainfall alert", "Local"),
    ("CISF Constable Recruitment 2024: Registrations Open for 1130 Fireman Posts", "Education"),
    ("Big B on re-release of old movies in theatres", "Entertainment"),
    ("Aadar Jain gets engaged to Alekha Advani", "Entertainment"),
]


# Prepare training data
train_texts, train_labels = zip(*training_data)

# Create a text classification pipeline
model = make_pipeline(CountVectorizer(), MultinomialNB())
model.fit(train_texts, train_labels)

# Function to categorize text
def categorize_text(text):
    return model.predict([text])[0]

# Apply categorization to each article
df['Category'] = df['Summary'].apply(categorize_text)

# Save updated DataFrame to CSV
df.to_csv('news_articles_with_categories.csv', index=False)

print("Categorization completed. Updated file saved as news_articles_with_categories.csv")
