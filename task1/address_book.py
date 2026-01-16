from collections import UserDict
from typing import List, Optional


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        # Повертає людино-зрозуміле рядкове представлення значення поля
        # Викликається при print(obj), str(obj) та форматуванні f-рядками
        return str(self.value)


class Name(Field):
    def __init__(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string")
        super().__init__(value.strip())


class Phone(Field):
    def __init__(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Phone must be a string of 10 digits")
        digits = ''.join(ch for ch in value if ch.isdigit())
        # Строга вимога: рівно 10 цифр
        if len(digits) != 10 or not digits.isdigit():
            raise ValueError("Phone number must contain exactly 10 digits")
        super().__init__(digits)


class Record:
    def __init__(self, name: str):
        self.name: Name = Name(name)
        self.phones: List[Phone] = []

    def add_phone(self, phone: str) -> None:
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> bool:
        """Видаляє перше входження номера. Повертає True, якщо видалено, інакше False."""
        for idx, p in enumerate(self.phones):
            if p.value == Phone(phone).value:
                del self.phones[idx]
                return True
        return False

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """Замінює old_phone на new_phone. Підіймає ValueError, якщо старий не знайдено або новий некоректний."""
        # Спочатку валідуємо новий номер (може спричинити ValueError)
        new_p = Phone(new_phone)
        for p in self.phones:
            if p.value == Phone(old_phone).value:
                p.value = new_p.value
                return
        # Якщо виконання сюди дійшло — старий номер не знайдено
        raise ValueError("Old phone number not found")

    def find_phone(self, phone: str) -> Optional[Phone]:
        try:
            phone_normalized = Phone(phone).value
        except ValueError:
            return None
        for p in self.phones:
            if p.value == phone_normalized:
                return p
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        return self.data.get(name)

    def delete(self, name: str) -> bool:
        if name in self.data:
            del self.data[name]
            return True
        return False

    def __str__(self) -> str:
        if not self.data:
            return "AddressBook is empty"
        return "\n".join(str(record) for record in self.data.values())
