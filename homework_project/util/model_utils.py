import re

def check_password_valid(password1, password2):

        tests = {
            'Şifre ve şifre tekrarı eşleşmeli': password1 != password2,
            'Şifre uzunluğu 8 karakterden uzun olmalıdır': len(password1) < 8,
            'Bütün karakterler rakam olamaz': re.search(r"\d", password1) is None,
            'Şifre en az bir tane büyük harf içermelidir': re.search(r"[A-Z]", password1) is None,
            'Şifre en az bir tane küçük harf içermelidir': re.search(r"[a-z]", password1) is None,
            'Şifre en az bir tane sembol içermelidir': re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password1) is None,
        }
        
        return [name for name,res in tests.items() if res]