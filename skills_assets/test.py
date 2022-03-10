from skill_extractor import SkillExtractor

text = "I am a web developer and a teacher living in chennai"

s = SkillExtractor()
print(s.get_skills(text))