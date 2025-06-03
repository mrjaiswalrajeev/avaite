from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Candidate

class CandidateAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test candidates
        cls.candidate1 = Candidate.objects.create(
            name="Ajay Kumar Yadav",
            age=30,
            gender='M',
            email="ajay.yadav@example.com",
            phone_number="1111111111"
        )
        cls.candidate2 = Candidate.objects.create(
            name="Ajay Kumar",
            age=28,
            gender='M',
            email="ajay.kumar@example.com",
            phone_number="2222222222"
        )
        cls.candidate3 = Candidate.objects.create(
            name="Ajay Singh",
            age=32,
            gender='M',
            email="ajay.singh@example.com",
            phone_number="3333333333"
        )
        cls.candidate4 = Candidate.objects.create(
            name="Ramesh Yadav",
            age=35,
            gender='M',
            email="ramesh.yadav@example.com",
            phone_number="4444444444"
        )

    # CRUD Tests
    def test_create_candidate(self):
        url = reverse('candidate-list')
        data = {
            "name": "New Candidate",
            "age": 25,
            "gender": "F",
            "email": "new@example.com",
            "phone_number": "5555555555"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Candidate.objects.count(), 5)

    def test_update_candidate(self):
        url = reverse('candidate-detail', args=[self.candidate1.id])
        data = {"name": "Updated Name", "age": 31}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.candidate1.refresh_from_db()
        self.assertEqual(self.candidate1.name, "Updated Name")

    def test_delete_candidate(self):
        url = reverse('candidate-detail', args=[self.candidate1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Candidate.objects.count(), 3)


    def test_empty_search(self):
        url = reverse('candidate-list')
        response = self.client.get(url, {'search': ''})
        self.assertEqual(len(response.data), 4)

    def test_special_characters(self):
        url = reverse('candidate-list')
        response = self.client.get(url, {'search': 'Ajay@Kumar#Yadav'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_results(self):
        url = reverse('candidate-list')
        response = self.client.get(url, {'search': 'Nonexistent Name'})
        self.assertEqual(len(response.data), 0)

    def test_search_relevancy_ordering(self):
        url = reverse('candidate-list')
        response = self.client.get(url, {'search': 'Ajay Kumar yadav'})
        names = [candidate['name'] for candidate in response.data]
        
        self.assertEqual(names, [
            "Ajay Kumar Yadav",  # Exact match (3 points)
            "Ajay Kumar",        # Contains all words (2 points)
            "Ajay Singh",      # 1 word match (sorted alphabetically)
            "Ramesh Yadav"         # 1 word match
        ])

def test_case_insensitivity(self):
    url = reverse('candidate-list')
    response = self.client.get(url, {'search': 'aJaY kuMAr'})
    names = [candidate['name'] for candidate in response.data]
    
    self.assertEqual(names, [
        "Ajay Kumar",        # Contains both words (higher word_count)
        "Ajay Kumar Yadav",  # Contains both words
        "Ajay Singh"         # Contains one word
    ])

def test_partial_matches(self):
    url = reverse('candidate-list')
    response = self.client.get(url, {'search': 'Kumar Yadav'})
    names = [candidate['name'] for candidate in response.data]
    
    self.assertEqual(names, [
        "Ajay Kumar Yadav",  # Contains both words
        "Ajay Kumar",        # Contains "Kumar"
        "Ramesh Yadav"       # Contains "Yadav"
    ])