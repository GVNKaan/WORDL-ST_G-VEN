import os
import json
import random
import string
from datetime import datetime
from typing import List, Dict, Set
import hashlib
import itertools
from collections import Counter
import threading
from concurrent.futures import ThreadPoolExecutor
import time

class UltimatePasswordGenerator:
    def __init__(self):
        self.total_generated = 0
        self.password_file = "WORLD_ULTIMATE_PASSWORDS.txt"
        self.all_passwords = set()
        self.stats = {
            'global_passwords': 0,
            'turkish_passwords': 0,
            'personal_passwords': 0,
            'leet_passwords': 0,
            'random_passwords': 0,
            'date_based': 0,
            'phone_based': 0,
            'common_patterns': 0
        }
        
        # Dünya çapında en çok kullanılan şifreler
        self.global_top_passwords = [
            "123456", "password", "12345678", "qwerty", "123456789", "12345", "1234", 
            "111111", "1234567", "dragon", "123123", "baseball", "abc123", "football", 
            "monkey", "letmein", "shadow", "master", "666666", "qwertyuiop", "123321",
            "mustang", "1234567890", "michael", "654321", "superman", "1qaz2wsx",
            "7777777", "fuckyou", "121212", "000000", "qazwsx", "123qwe", "killer",
            "trustno1", "jordan", "jennifer", "zxcvbnm", "asdfgh", "hunter", "buster",
            "soccer", "harley", "batman", "andrew", "tigger", "sunshine", "iloveyou",
            "fuckme", "2000", "charlie", "robert", "thomas", "hockey", "ranger",
            "daniel", "starwars", "klaster", "112233", "george", "asshole", "computer",
            "michelle", "jessica", "pepper", "1111", "zxcvbn", "555555", "11111111",
            "131313", "freedom", "777777", "pass", "fuck", "maggie", "159753", "aaaaaa",
            "ginger", "princess", "joshua", "cheese", "amanda", "summer", "love", "ashley",
            "6969", "nicole", "chelsea", "biteme", "matthew", "access", "yankees",
            "987654321", "dallas", "austin", "thunder", "taylor", "matrix", "minecraft"
        ]
        
        # Türkiye'de en çok kullanılan şifreler
        self.turkish_top_passwords = [
            "123456", "password", "123456789", "12345678", "111111", "123123", "000000",
            "12345", "112233", "1234567", "qwerty", "mustafa", "ahmet", "mehmet", "ayse",
            "fatma", "ali", "istanbul", "ankara", "izmir", "fenerbahce", "galatasaray",
            "besiktas", "trabzonspor", "bursaspor", "seniseviyorum", "askim", "canim",
            "allah", "muhammed", "merve", "berna", "elif", "zeynep", "burak", "onur",
            "serkan", "volkan", "yasemin", "deniz", "emre", "okan", "umut", "kadir",
            "kemal", "orhan", "selin", "pinar", "esra", "gizem", "rabia", "huseyin",
            "ibrahim", "osman", "hakan", "metin", "yusuf", "omer", "caner", "tolga",
            "levent", "samsun", "trabzon", "adana", "antalya", "bursa", "konya", "kayseri",
            "mersin", "diyarbakir", "gaziantep", "eskisehir", "malatya", "sivas", "erzurum"
        ]
        
        # Türk isimleri veritabanı
        self.turkish_names = {
            'male': ['ahmet', 'mehmet', 'mustafa', 'ali', 'huseyin', 'hasan', 'ibrahim', 
                    'osman', 'muhammed', 'kadir', 'kemal', 'can', 'cem', 'deniz', 'berk',
                    'emre', 'yusuf', 'omer', 'burak', 'onur', 'serkan', 'volkan', 'okan',
                    'umut', 'kadir', 'orhan', 'hakan', 'metin', 'caner', 'tolga', 'levent'],
            'female': ['ayse', 'fatma', 'elif', 'zeynep', 'merve', 'berna', 'esra', 'selin',
                      'pinar', 'yasemin', 'gizem', 'rabia', 'sema', 'dilek', 'aylin', 'burcu',
                      'ceren', 'derya', 'eda', 'figen', 'gamze', 'hulya', 'sibel', 'aysegul',
                      'fatma', 'hande', 'ilknur', 'jale', 'kubra', 'leyla']
        }
        
        # Türk şehirleri
        self.turkish_cities = [
            'istanbul', 'ankara', 'izmir', 'bursa', 'adana', 'antalya', 'konya', 'mersin',
            'kayseri', 'samsun', 'trabzon', 'erzurum', 'eskisehir', 'diyarbakir', 'gaziantep',
            'kocaeli', 'kutahya', 'malatya', 'ordu', 'sakarya', 'denizli', 'balikesir', 'manisa',
            'hatay', 'van', 'mardin', 'urfa', 'batman', 'agri', 'sivas', 'corum', 'amasya'
        ]
        
        # Takımlar
        self.turkish_teams = [
            'fenerbahce', 'galatasaray', 'besiktas', 'trabzonspor', 'bursaspor', 'goztepe',
            'konyaspor', 'ankaragucu', 'sivasspor', 'antalyaspor', 'kasimpasa', 'alanyaspor',
            'kayserispor', 'giresunspor', 'hatayspor', 'adana', 'samsunspor', 'rizespor'
        ]
        
        # Leet speak mapping
        self.leet_map = {
            'a': ['4', '@'],
            'e': ['3'],
            'i': ['1', '!'],
            'o': ['0'],
            's': ['5', '$'],
            't': ['7'],
            'b': ['8'],
            'g': ['9'],
            'l': ['1', '|']
        }
        
        # Özel karakterler
        self.special_chars = "!@#$%&*?_-+=."
        
        # Yaygın ekler
        self.common_suffixes = ['123', '1234', '12345', '1', '12', '00', '01', '99', '007', '88', '69', '21']

    def show_banner(self):
        banner = """
╔══════════════════════════════════════════════════════════════════════════════════╗
║                  🌍 KAAN GÜVEN - ULTIMATE PASSWORD GENERATOR 🌍                ║
║                         DÜNYANIN EN GELİŞMİŞ ŞİFRE ÜRETİCİSİ                   ║
║                              PYTHON EDİSYONU v2.0                              ║
╚══════════════════════════════════════════════════════════════════════════════════╝
        """
        print(banner)

    def get_user_options(self) -> Dict:
        """Kullanıcıdan üretim ayarlarını al"""
        print("\n🔧 ÜRETİM AYARLARINI SEÇİN:")
        print("=" * 50)
        
        options = {
            'include_global': self.get_yes_no("Global şifreler eklensin mi?"),
            'include_turkish': self.get_yes_no("Türk şifreleri eklensin mi?"),
            'include_personal': self.get_yes_no("Kişisel şifreler eklensin mi?"),
            'include_leet': self.get_yes_no("Leet speak dönüşümleri eklensin mi?"),
            'include_random': self.get_yes_no("Rastgele şifreler eklensin mi?"),
            'include_dates': self.get_yes_no("Tarih bazlı şifreler eklensin mi?"),
            'include_phones': self.get_yes_no("Telefon bazlı şifreler eklensin mi?"),
            'include_patterns': self.get_yes_no("Özel pattern'ler eklensin mi?"),
            'include_advanced': self.get_yes_no("Gelişmiş kombinasyonlar eklensin mi?"),
            'max_passwords': self.get_integer("Maksimum şifre sayısı", 100000),
            'thread_count': self.get_integer("Thread sayısı (performans için)", 4)
        }
        
        return options

    def get_yes_no(self, question: str) -> bool:
        """Evet/Hayır sorusu sor"""
        response = input(f"{question} (e/h): ").lower().strip()
        return response in ['e', 'evet', 'y', 'yes']

    def get_integer(self, prompt: str, default: int) -> int:
        """Integer değer al"""
        try:
            response = input(f"{prompt} [{default}]: ").strip()
            return int(response) if response else default
        except:
            return default

    def get_person_info(self) -> Dict:
        """Kişisel bilgileri al"""
        print("\n📋 DETAYLI KİŞİSEL BİLGİLER:")
        print("=" * 40)
        
        person = {}
        fields = [
            ('ad', 'Adınız'),
            ('soyad', 'Soyadınız'),
            ('dogum_yili', 'Doğum Yılı'),
            ('dogum_gunu', 'Doğum Günü'),
            ('dogum_ayi', 'Doğum Ayı'),
            ('takim', 'Sevdiğiniz Takım'),
            ('memleket', 'Memleketiniz'),
            ('es_ismi', 'Eş İsmi'),
            ('cocuk_ismi', 'Çocuk İsmi'),
            ('favori_numara', 'Favori Numara'),
            ('takma_ad', 'Takma Ad'),
            ('anne_adi', 'Anne Adı'),
            ('baba_adi', 'Baba Adı'),
            ('telefon', 'Telefon Numaranız'),
            ('plaka', 'Plaka Kodu'),
            ('okul', 'Okul İsmi'),
            ('meslek', 'Meslek'),
            ('evcil_hayvan', 'Evcil Hayvan İsmi'),
            ('spor', 'Sevdiğiniz Spor'),
            ('muzik', 'Sevdiğiniz Müzik Türü'),
            ('renk', 'Favori Renginiz'),
            ('yemek', 'Favori Yemeğiniz'),
            ('film', 'Favori Filminiz'),
            ('kitap', 'Favori Kitabınız')
        ]
        
        for key, prompt in fields:
            if 'yil' in key or 'gunu' in key or 'ayi' in key:
                person[key] = self.get_integer(prompt, 1990 if 'yil' in key else 1)
            else:
                person[key] = input(f"{prompt}: ").strip()
        
        return person

    def generate_all_passwords(self, person: Dict, options: Dict):
        """Tüm şifreleri oluştur"""
        print("\n🌍 ŞİFRE ÜRETİMİ BAŞLIYOR...")
        print("=" * 60)
        
        start_time = time.time()
        
        # Multi-threading için thread pool
        with ThreadPoolExecutor(max_workers=options['thread_count']) as executor:
            futures = []
            
            if options['include_global']:
                futures.append(executor.submit(self.add_global_passwords))
            
            if options['include_turkish']:
                futures.append(executor.submit(self.add_turkish_passwords))
            
            if options['include_personal']:
                futures.append(executor.submit(self.generate_personal_passwords, person, options))
            
            if options['include_leet']:
                futures.append(executor.submit(self.generate_leet_passwords))
            
            if options['include_random']:
                futures.append(executor.submit(self.generate_random_passwords, 10000))
            
            if options['include_dates']:
                futures.append(executor.submit(self.generate_date_based_passwords, person))
            
            if options['include_phones']:
                futures.append(executor.submit(self.generate_phone_based_passwords, person))
            
            if options['include_patterns']:
                futures.append(executor.submit(self.generate_common_patterns, person))
            
            if options['include_advanced']:
                futures.append(executor.submit(self.generate_advanced_combinations, person))
            
            # Tüm thread'lerin bitmesini bekle
            for future in futures:
                future.result()
        
        end_time = time.time()
        print(f"\n✅ Şifre üretimi tamamlandı! Süre: {end_time - start_time:.2f} saniye")

    def add_global_passwords(self):
        """Global şifreleri ekle"""
        print("[1/9] Global şifreler ekleniyor...")
        self._add_passwords(self.global_top_passwords, 'global_passwords')

    def add_turkish_passwords(self):
        """Türk şifrelerini ekle"""
        print("[2/9] Türk şifreleri ekleniyor...")
        self._add_passwords(self.turkish_top_passwords, 'turkish_passwords')
        self._add_passwords(self.turkish_names['male'] + self.turkish_names['female'], 'turkish_passwords')
        self._add_passwords(self.turkish_cities, 'turkish_passwords')
        self._add_passwords(self.turkish_teams, 'turkish_passwords')

    def generate_personal_passwords(self, person: Dict, options: Dict):
        """Kişisel şifreleri oluştur"""
        print("[3/9] Kişisel şifreler oluşturuluyor...")
        
        personal_words = self.get_personal_words(person)
        
        # Temel varyasyonlar
        for word in personal_words:
            if len(self.all_passwords) >= options['max_passwords']:
                break
                
            self._add_password(word, 'personal_passwords')
            self._add_password(word.lower(), 'personal_passwords')
            self._add_password(word.upper(), 'personal_passwords')
            self._add_password(word.capitalize(), 'personal_passwords')

        # Sayı eklemeleri
        for word in personal_words:
            if len(self.all_passwords) >= options['max_passwords']:
                break
                
            for i in range(1000):
                self._add_password(f"{word}{i}", 'personal_passwords')
                self._add_password(f"{word}{i:02d}", 'personal_passwords')
                self._add_password(f"{word}{i:03d}", 'personal_passwords')

        # Özel karakter kombinasyonları
        for word in personal_words:
            if len(self.all_passwords) >= options['max_passwords']:
                break
                
            for char in self.special_chars:
                self._add_password(f"{word}{char}", 'personal_passwords')
                self._add_password(f"{char}{word}", 'personal_passwords')
                self._add_password(f"{word}{char}123", 'personal_passwords')

        # Kelime birleştirmeleri
        for i, word1 in enumerate(personal_words):
            if len(self.all_passwords) >= options['max_passwords']:
                break
                
            for j, word2 in enumerate(personal_words):
                if i == j:
                    continue
                    
                separators = ['', '.', '_', '-', '']
                for sep in separators:
                    self._add_password(f"{word1}{sep}{word2}", 'personal_passwords')

    def generate_leet_passwords(self):
        """Leet speak şifreleri oluştur"""
        print("[4/9] Leet speak şifreleri oluşturuluyor...")
        
        current_passwords = list(self.all_passwords)
        for password in current_passwords:
            if len(self.all_passwords) >= 500000:
                break
                
            leet_variations = self.generate_leet_variations(password)
            for leet in leet_variations:
                self._add_password(leet, 'leet_passwords')

    def generate_random_passwords(self, count: int):
        """Rastgele şifreler oluştur"""
        print("[5/9] Rastgele şifreler oluşturuluyor...")
        
        for _ in range(count):
            if len(self.all_passwords) >= 500000:
                break
                
            length = random.randint(8, 16)
            password = ''.join(random.choices(
                string.ascii_letters + string.digits + self.special_chars, 
                k=length
            ))
            self._add_password(password, 'random_passwords')

    def generate_date_based_passwords(self, person: Dict):
        """Tarih bazlı şifreler oluştur"""
        print("[6/9] Tarih bazlı şifreler oluşturuluyor...")
        
        dates = self.generate_date_patterns(person)
        for date_str in dates:
            self._add_password(date_str, 'date_based')
            self._add_password(f"{person['ad']}{date_str}", 'date_based')
            self._add_password(f"{date_str}{person['ad']}", 'date_based')

    def generate_phone_based_passwords(self, person: Dict):
        """Telefon bazlı şifreler oluştur"""
        print("[7/9] Telefon bazlı şifreler oluşturuluyor...")
        
        if not person.get('telefon'):
            return
            
        phone = person['telefon'].replace(' ', '').replace('-', '')
        patterns = []
        
        for i in range(4, min(8, len(phone) + 1)):
            patterns.append(phone[-i:])
        
        for pattern in patterns:
            self._add_password(pattern, 'phone_based')
            self._add_password(f"{person['ad']}{pattern}", 'phone_based')
            self._add_password(f"{pattern}{person['ad']}", 'phone_based')

    def generate_common_patterns(self, person: Dict):
        """Ortak pattern'leri oluştur"""
        print("[8/9] Ortak pattern'ler oluşturuluyor...")
        
        patterns = []
        
        # İsim + tarih pattern'leri
        base_combinations = [
            f"{person['ad']}{person['dogum_yili']}",
            f"{person['ad']}{person['dogum_gunu']:02d}",
            f"{person['ad']}{person['dogum_ayi']:02d}",
            f"{person['ad']}{person['dogum_gunu']:02d}{person['dogum_ayi']:02d}",
            f"{person['ad']}{person['soyad']}",
            f"{person['ad']}.{person['soyad']}",
            f"{person['ad']}_{person['soyad']}",
            f"{person['ad'][0]}{person['soyad']}",
            f"{person['ad']}{person['favori_numara']}",
            f"{person['takma_ad']}{person['dogum_yili']}",
            f"{person['takim']}{person['dogum_yili']}",
            f"{person['memleket']}{person['dogum_yili']}",
            f"{person['plaka']}{person['ad']}",
            f"{person['ad']}{person['plaka']}",
            f"{person['ad']}!",
            f"{person['ad']}.",
        ]
        
        patterns.extend(base_combinations)
        
        # Eklerle kombinasyonlar
        for pattern in base_combinations:
            for suffix in self.common_suffixes:
                patterns.append(f"{pattern}{suffix}")
        
        for pattern in patterns:
            self._add_password(pattern, 'common_patterns')

    def generate_advanced_combinations(self, person: Dict):
        """Gelişmiş kombinasyonlar oluştur"""
        print("[9/9] Gelişmiş kombinasyonlar oluşturuluyor...")
        
        personal_words = self.get_personal_words(person)
        
        # Üçlü kombinasyonlar
        for combo in itertools.combinations(personal_words[:10], 3):
            if len(self.all_passwords) >= 500000:
                break
            self._add_password(''.join(combo), 'common_patterns')
        
        # Özel formüller
        special_formulas = [
            f"{person['ad']}{person['dogum_yili']}{person['soyad']}",
            f"{person['ad']}{person['dogum_gunu']:02d}{person['dogum_ayi']:02d}{person['dogum_yili']}",
            f"{person['soyad']}{person['ad']}{person['dogum_yili']}",
            f"{person['anne_adi']}{person['baba_adi']}{person['dogum_yili']}",
            f"{person['ad']}{person['es_ismi']}{person['cocuk_ismi']}",
            f"{person['takim']}{person['memleket']}{person['dogum_yili']}",
            f"{person['okul']}{person['meslek']}{person['dogum_yili']}",
        ]
        
        for formula in special_formulas:
            self._add_password(formula, 'common_patterns')

    def get_personal_words(self, person: Dict) -> List[str]:
        """Kişisel kelimeleri listele"""
        words = []
        
        fields = ['ad', 'soyad', 'takma_ad', 'es_ismi', 'cocuk_ismi', 'takim', 
                 'memleket', 'favori_numara', 'anne_adi', 'baba_adi', 'plaka',
                 'okul', 'meslek', 'evcil_hayvan', 'spor', 'muzik', 'renk',
                 'yemek', 'film', 'kitap']
        
        for field in fields:
            value = person.get(field, '')
            if value and str(value).strip():
                words.append(str(value))
        
        # Tarih bilgileri
        words.extend([
            str(person['dogum_yili']),
            str(person['dogum_yili'])[2:],  # Son iki hane
            f"{person['dogum_gunu']:02d}",
            f"{person['dogum_ayi']:02d}"
        ])
        
        return [w for w in words if w and len(w) >= 2]

    def generate_date_patterns(self, person: Dict) -> List[str]:
        """Tarih pattern'leri oluştur"""
        patterns = []
        year = person['dogum_yili']
        month = person['dogum_ayi']
        day = person['dogum_gunu']
        
        date_formats = [
            f"{day:02d}{month:02d}{year}",
            f"{day:02d}{month:02d}{str(year)[2:]}",
            f"{month:02d}{day:02d}{year}",
            f"{month:02d}{day:02d}{str(year)[2:]}",
            f"{year}{month:02d}{day:02d}",
            f"{str(year)[2:]}{month:02d}{day:02d}",
            f"{day:02d}{month:02d}",
            f"{month:02d}{day:02d}",
        ]
        
        return date_formats

    def generate_leet_variations(self, text: str) -> List[str]:
        """Leet speak varyasyonları oluştur"""
        variations = [text.lower()]
        
        for char, replacements in self.leet_map.items():
            new_variations = []
            for variation in variations:
                for replacement in replacements:
                    new_variations.append(variation.replace(char, replacement))
            variations.extend(new_variations)
        
        return list(set(variations))

    def _add_passwords(self, passwords: List[str], category: str):
        """Şifre listesi ekle"""
        for pwd in passwords:
            self._add_password(pwd, category)

    def _add_password(self, password: str, category: str):
        """Tek şifre ekle"""
        if not password or len(password) < 4 or len(password) > 30:
            return
            
        if password not in self.all_passwords:
            self.all_passwords.add(password)
            self.total_generated += 1
            self.stats[category] += 1
            
            if self.total_generated % 1000 == 0:
                print(f"\r🔧 Oluşturulan: {self.total_generated:,} - Son: {password[:30]}", end='', flush=True)

    def save_to_file(self):
        """Şifreleri dosyaya kaydet"""
        print(f"\n\n💾 DOSYAYA YAZILIYOR... ({len(self.all_passwords):,} şifre)")
        
        try:
            with open(self.password_file, 'w', encoding='utf-8') as f:
                # Header
                f.write("╔══════════════════════════════════════════════════════════════════════════════════╗\n")
                f.write("║                  🌍 KAAN GÜVEN - ULTIMATE PASSWORD DATABASE 🌍                ║\n")
                f.write("║                         DÜNYANIN EN KAPSAMLI ŞİFRE LİSTESİ                     ║\n")
                f.write("╚══════════════════════════════════════════════════════════════════════════════════╝\n\n")
                
                # İstatistikler
                f.write(f"Oluşturulma Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
                f.write(f"Toplam Şifre Sayısı: {len(self.all_passwords):,}\n")
                f.write(f"Benzersiz Şifreler: {len(set(self.all_passwords)):,}\n\n")
                
                f.write("📊 İSTATİSTİKLER:\n")
                for category, count in self.stats.items():
                    f.write(f"  {category}: {count:,}\n")
                f.write("\n")
                
                f.write("ŞİFRE LİSTESİ:\n")
                f.write("=" * 50 + "\n")
                
                # Şifreleri yaz
                for i, password in enumerate(sorted(self.all_passwords), 1):
                    f.write(f"{i:8,}: {password}\n")
                    
                    if i % 10000 == 0:
                        print(f"📝 Yazılan şifre: {i:,} / {len(self.all_passwords):,}")
                
                f.write("\n" + "=" * 50 + "\n")
                f.write("🌍 KAAN GÜVEN - Ultimate Password Generator v2.0\n")
                f.write("🎯 Eğitim ve güvenlik testleri amaçlıdır!\n")
            
            print(f"✅ DOSYA BAŞARIYLA KAYDEDİLDİ: {self.password_file}")
            
        except Exception as e:
            print(f"❌ HATA: {e}")

    def show_final_stats(self):
        """Son istatistikleri göster"""
        file_size = os.path.getsize(self.password_file) if os.path.exists(self.password_file) else 0
        
        print("\n\n📊 DETAYLI İSTATİSTİKLER:")
        print("=" * 60)
        print(f"📁 Dosya Adı: {self.password_file}")
        print(f"📦 Dosya Boyutu: {file_size / 1024 / 1024:.2f} MB")
        print(f"🔢 Toplam Şifre: {len(self.all_passwords):,}")
        print(f"🎯 Benzersiz Şifre: {len(set(self.all_passwords)):,}")
        print(f"⏰ Oluşturulma: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        
        print("\n📈 KATEGORİK DAĞILIM:")
        for category, count in self.stats.items():
            percentage = (count / len(self.all_passwords)) * 100 if self.all_passwords else 0
            print(f"  {category:15}: {count:8,} ({percentage:5.1f}%)")
        
        print("\n🚀 KAAN GÜVEN - Python Ultimate Password Generator v2.0")
        print("🌍 Global + Türkiye + Kişiselleştirilmiş Şifre Veritabanı")

    def run(self):
        """Programı çalıştır"""
        self.show_banner()
        
        # Ayarları al
        options = self.get_user_options()
        
        # Kişisel bilgileri al
        person = self.get_person_info()
        
        # Şifreleri oluştur
        self.generate_all_passwords(person, options)
        
        # Dosyaya kaydet
        self.save_to_file()
        
        # İstatistikleri göster
        self.show_final_stats()

# Programı çalıştır
if __name__ == "__main__":
    generator = UltimatePasswordGenerator()
    generator.run()