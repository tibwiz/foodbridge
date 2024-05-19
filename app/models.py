import json
import os


class User:
    def __init__(self, username, email, password, category):
        self.username = username
        self.email = email
        self.password = password
        self.category = category

    def to_json(self):
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'category': self.category
        }

    @classmethod
    def from_json(cls, json_data):
        return cls(**json_data)

    def save(self):
        filename = f'db/users/{self.username}.json'
        with open(filename, 'w') as file:
            json.dump(self.to_json(), file)

    @classmethod
    def load(cls, identifier):
        filename = f'db/users/{identifier}.json'
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                data = json.load(file)
                return cls.from_json(data)
        else:
            return None

    def validate_password(self, password):
        return self.password == password


class DonationItem:
    def __init__(self, item_id, posted_by, title, description, category, quantity, location, contact, expiry_date,
                 image,
                 claimed_by=None):
        self.item_id = item_id
        self.posted_by = posted_by
        self.title = title
        self.description = description
        self.category = category
        self.quantity = quantity
        self.location = location
        self.contact = contact
        self.expiry_date = expiry_date
        self.image = image
        self.claimed_by = claimed_by




    def to_json(self):
        return {
            'item_id': self.item_id,
            'posted_by': self.posted_by,
            'claimed_by': self.claimed_by,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'quantity': self.quantity,
            'location': self.location,
            'contact': self.contact,
            'expiry_date': self.expiry_date,
            'image': self.image
        }

    def __repr__(self):
        return f"Item ID: {self.item_id}, Title: {self.title}, Category: {self.category}, Quantity: {self.quantity}, Location: {self.location}, Contact: {self.contact}, Expiry Date: {self.expiry_date}, Image: {self.image}, Posted By: {self.posted_by}, Claimed By: {self.claimed_by}"

    def __str__(self):
        return f"Item ID: {self.item_id}, Title: {self.title}, Category: {self.category}, Quantity: {self.quantity}, Location: {self.location}, Contact: {self.contact}, Expiry Date: {self.expiry_date}, Image: {self.image}, Posted By: {self.posted_by}, Claimed By: {self.claimed_by}"

    @classmethod
    def from_json(cls, json_data):
        return cls(**json_data)

    def save(self):
        filename = f'db/items/{self.item_id}.json'
        with open(filename, 'w') as file:
            json.dump(self.to_json(), file)

    @classmethod
    def load(cls, identifier):
        filename = f'db/items/{identifier}.json'
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                data = json.load(file)
                return cls.from_json(data)
        else:
            return None

    def delete(self):
        filename = f'db/items/{self.item_id}.json'
        os.remove(filename)

    @classmethod
    def load_all(cls):
        items = []
        for filename in os.listdir('db/items'):
            with open(f'db/items/{filename}', 'r') as file:
                data = json.load(file)
                items.append(cls.from_json(data))
        return items

    @staticmethod
    def get_next_id():
        item_files = os.listdir('db/items/')
        if not item_files:
            return 1
        item_ids = [int(file.split('.')[0]) for file in item_files]
        return max(item_ids) + 1
