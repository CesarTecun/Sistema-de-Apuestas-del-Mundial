"""
Cliente HTTP para consumir el microservicio Marcador (FastAPI).
Expone métodos para consultar partidos en vivo, selecciones y actualizar marcadores.
"""

import requests
from django.conf import settings


class MarcadorClientError(Exception):
    """Error genérico del cliente del microservicio marcador."""
    pass


class MarcadorClient:
    """
    Cliente para interactuar con el microservicio de marcador en vivo.
    """

    def __init__(self):
        self.base_url = settings.MARCADOR_SERVICE_URL.rstrip("/")
        self.timeout = getattr(settings, "MARCADOR_SERVICE_TIMEOUT", 5)

    def _request(self, method, path, **kwargs):
        """Ejecuta una petición HTTP al microservicio."""
        url = f"{self.base_url}{path}"
        try:
            response = requests.request(
                method,
                url,
                timeout=self.timeout,
                **kwargs
            )
            response.raise_for_status()
            return response
        except requests.exceptions.ConnectionError as exc:
            raise MarcadorClientError(
                "No se pudo conectar al microservicio marcador. "
                "Verifica que esté corriendo en el puerto 8001."
            ) from exc
        except requests.exceptions.Timeout as exc:
            raise MarcadorClientError(
                "El microservicio marcador no respondió a tiempo."
            ) from exc
        except requests.exceptions.HTTPError as exc:
            raise MarcadorClientError(
                f"Error del microservicio marcador: {exc.response.status_code} - {exc.response.text}"
            ) from exc

    # ------------------------------------------------------------------
    # Selecciones
    # ------------------------------------------------------------------
    def listar_selecciones(self):
        """Obtiene todas las selecciones del microservicio."""
        response = self._request("GET", "/api/selecciones/")
        return response.json()

    def obtener_seleccion(self, id_seleccion):
        """Obtiene una selección por ID."""
        response = self._request("GET", f"/api/selecciones/{id_seleccion}")
        return response.json()

    # ------------------------------------------------------------------
    # Partidos
    # ------------------------------------------------------------------
    def listar_partidos(self, estado=None, fk_id_liga=None):
        """Obtiene la lista de partidos del microservicio."""
        params = {}
        if estado:
            params["estado"] = estado
        if fk_id_liga is not None:
            params["fk_id_liga"] = fk_id_liga
        response = self._request("GET", "/api/partidos/", params=params)
        return response.json()

    def partidos_en_vivo(self):
        """Obtiene los partidos en juego con detalle de equipos."""
        response = self._request("GET", "/api/partidos/en-vivo")
        return response.json()

    def obtener_partido(self, id_partido):
        """Obtiene un partido específico con detalle de equipos."""
        response = self._request("GET", f"/api/partidos/{id_partido}")
        return response.json()

    def partidos_por_equipo(self, equipo_id):
        """Obtiene los partidos de un equipo específico."""
        response = self._request("GET", "/api/partidos/por-equipo", params={"equipo_id": equipo_id})
        return response.json()

    def crear_partido(self, data):
        """Crea un nuevo partido en el microservicio."""
        response = self._request("POST", "/api/partidos/", json=data)
        return response.json()

    def actualizar_partido(self, id_partido, data):
        """Actualiza un partido en el microservicio."""
        response = self._request("PATCH", f"/api/partidos/{id_partido}", json=data)
        return response.json()

    def actualizar_marcador(self, id_partido, data):
        """
        Actualiza el marcador de un partido.
        data: dict con gol_local, gol_visitante, estado, resultado, ganador_penales
        """
        response = self._request("PATCH", f"/api/partidos/{id_partido}/marcador", json=data)
        return response.json()

    def eliminar_partido(self, id_partido):
        """Elimina un partido del microservicio."""
        self._request("DELETE", f"/api/partidos/{id_partido}")

    # ------------------------------------------------------------------
    # Health check
    # ------------------------------------------------------------------
    def health_check(self):
        """Verifica si el microservicio está disponible."""
        try:
            response = self._request("GET", "/health")
            return response.json()
        except (MarcadorClientError, requests.exceptions.RequestException):
            return {"status": "unavailable"}

    # ------------------------------------------------------------------
    # Sincronización (Django -> Marcador)
    # ------------------------------------------------------------------
    def sync_seleccion(self, data: dict):
        """Replica una selección de Django al microservicio marcador."""
        response = self._request("POST", "/api/sync/selecciones/", json=data)
        return response.json()

    def sync_partido(self, data: dict):
        """Replica un partido de Django al microservicio marcador."""
        response = self._request("POST", "/api/sync/partidos/", json=data)
        return response.json()

    def delete_partido_sync(self, id_partido: int):
        """Elimina un partido del microservicio marcador (hard delete)."""
        self._request("DELETE", f"/api/partidos/{id_partido}")

    def controlar_partido(self, id_partido: int, data: dict):
        """Controla un partido en el microservicio marcador (iniciar, pausar, etc.)."""
        response = self._request("PATCH", f"/api/partidos/{id_partido}/control", json=data)
        return response.json()


# Instancia global para uso directo
marcador_client = MarcadorClient()
