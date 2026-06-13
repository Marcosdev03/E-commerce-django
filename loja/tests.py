from django.test import SimpleTestCase
from django.urls import reverse


class HealthRouteTest(SimpleTestCase):
    def test_health_endpoint(self):
        response = self.client.get(reverse("health"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "healthy"})

    def test_state_changing_routes_reject_get(self):
        self.assertEqual(
            self.client.get(reverse("carrinho_de_compras:adicionaraocarrinho")).status_code,
            405,
        )
        self.assertEqual(
            self.client.get(reverse("carrinho_de_compras:remover")).status_code,
            405,
        )
        self.assertEqual(
            self.client.get(reverse("perfil:logout")).status_code,
            405,
        )
