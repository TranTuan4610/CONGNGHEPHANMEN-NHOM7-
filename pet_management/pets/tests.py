from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from pets.models import User, Pet

class PetManagementTestCase(TestCase):
    def setUp(self):
        """Tạo dữ liệu trước khi chạy test"""
        self.client = Client()
        
        # Tạo user test
        self.user = User.objects.create(username="testuser", password=make_password("Testpassword123!"))
        
        # Tạo thú cưng test
        self.pet = Pet.objects.create(name="Lucky", species="Dog", is_available_for_adoption=True)

    def test_register_user(self):
        """✅ Kiểm tra đăng ký"""
        response = self.client.post(reverse('register_user'), {
            'username': 'newuser',
            'password1': 'Testpassword123!',
            'password2': 'Testpassword123!'
        })
        self.assertEqual(response.status_code, 302)  # Chuyển hướng sau đăng ký

    def test_login_user(self):
        """✅ Kiểm tra đăng nhập"""
        response = self.client.post(reverse('login_user'), {
            'username': 'testuser',
            'password': 'Testpassword123!'
        })
        self.assertEqual(response.status_code, 302)

    def test_add_pet(self):
        """✅ Kiểm tra thêm thú cưng"""
        self.client.session['user_id'] = self.user.id
        response = self.client.post(reverse('add_pet'), {
            'name': 'Bella',
            'species': 'Cat',
        })
        self.assertEqual(response.status_code, 302)

    def test_view_pets(self):
        """✅ Kiểm tra danh sách thú cưng & thú cưng có tồn tại"""
        self.client.session['user_id'] = self.user.id
        response = self.client.get(reverse('view_pets'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lucky")  # Kiểm tra xem thú cưng "Lucky" có xuất hiện không

    def test_adopt_pet(self):
        """✅ Kiểm tra nhận nuôi thú cưng"""
        self.client.session['user_id'] = self.user.id
        response = self.client.post(reverse('adopt_pet'), {'pet_id': self.pet.id})
        self.assertEqual(response.status_code, 302)

    def test_donate_to_fund(self):
        """✅ Kiểm tra đóng góp quỹ có thành công không"""
        self.client.session['user_id'] = self.user.id
        response = self.client.post(reverse('donate_to_fund'), {'amount': '50'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Đóng góp thành công.")  # Kiểm tra thông báo thành công

    def test_edit_pet(self):
        """✅ Kiểm tra chỉnh sửa thú cưng"""
        self.client.session['user_id'] = self.user.id
        response = self.client.post(reverse('edit_pet', args=[self.pet.id]), {'name': 'Lucky Updated'})
        self.assertEqual(response.status_code, 302)

    def test_delete_pet(self):
        """✅ Kiểm tra xóa thú cưng"""
        self.client.session['user_id'] = self.user.id
        response = self.client.post(reverse('delete_pet', args=[self.pet.id]))
        self.assertEqual(response.status_code, 302)

    def test_home_page(self):
        """✅ Kiểm tra trang chủ"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_about_us_page(self):
        """✅ Kiểm tra trang giới thiệu"""
        response = self.client.get(reverse('about_us'))
        self.assertEqual(response.status_code, 200)

    def test_news_page(self):
        """✅ Kiểm tra trang tin tức"""
        response = self.client.get(reverse('news'))
        self.assertEqual(response.status_code, 200)
