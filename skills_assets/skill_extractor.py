class SkillExtractor:
    import pathlib
    import re
    import nltk
    import pickle
    from nltk.stem import WordNetLemmatizer
    from nltk.corpus import stopwords
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('punkt')
    nltk.download('omw-1.4')
    curr_dir = str(pathlib.Path(__file__).parent.resolve())+"/skill.pylist"
    skills_list = pickle.load(open(curr_dir, "rb"))

    def get_skills(self, data):
        try:
            text = self.re.sub('<[^>]*>',' ',data)
            #Tokenization
            word_tokens = [self.re.sub('[^a-zA-Z]','',word.lower()) for word in self.nltk.word_tokenize(text) if len(self.re.sub('[^a-zA-Z]','',word.lower())) > 0]
            #Lammetization
            lemmatizer = self.WordNetLemmatizer()
            words = [lemmatizer.lemmatize(word) for word in word_tokens if word not in set(self.stopwords.words('english'))]
            skills = set([skill for skill in words if skill in self.skills_list])
            return list(skills)
        except Exception as e:
            err_msg = e.args
            print(e)
            #TODO: Add Nodemailer and log files
            return ['Error in Skill Extractor'+str(e)]