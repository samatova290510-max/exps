import unittest
import random
import string

class TestPasswordGenerator(unittest.TestCase):
    
    def test_password_generation(self):
        """
        Тест: Проверка генерации пароля
        - Длина 12 символов
        - Только цифры и буквы (без спецсимволов)
        """
      
        length = 12
        use_digits = True
        use_letters = True
        use_symbols = False
        
        chars = ""
        if use_digits:
            chars += string.digits
        if use_letters:
            chars += string.ascii_letters
        if use_symbols:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        password = ''.join(random.choice(chars) for _ in range(length))
      
        print("\n" + "="*50)
        print("РЕЗУЛЬТАТ ТЕСТА")
        print("="*50)
        print(f"Сгенерированный пароль: {password}")
        print(f"Длина пароля: {len(password)}")
        print(f"Содержит цифры: {'да' if any(c.isdigit() for c in password) else 'нет'}")
        print(f"Содержит буквы: {'да' if any(c.isalpha() for c in password) else 'нет'}")
        print(f"Содержит спецсимволы: {'да' if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password) else 'нет'}")
        print("="*50)
        
        self.assertEqual(len(password), 12, "❌ Ошибка: длина пароля должна быть 12 символов")
        self.assertTrue(any(c.isdigit() for c in password), "❌ Ошибка: пароль должен содержать хотя бы одну цифру")
        self.assertTrue(any(c.isalpha() for c in password), "❌ Ошибка: пароль должен содержать хотя бы одну букву")
        self.assertFalse(any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password), 
                        "❌ Ошибка: пароль не должен содержать специальные символы")
        
        print("\n✅ ТЕСТ ПРОЙДЕН УСПЕШНО!")

if __name__ == "__main__":
    unittest.main()
