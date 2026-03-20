import http from 'k6/http';
import { check, sleep } from 'k6';

// Smoke Test: Una prueba básica y de corta duración con una carga mínima
// para asegurar que el sistema está disponible y los endpoints cruciales funcionan.
export const options = {
  vus: 1, // 1 Usuario Virtual
  duration: '30s', // 30 segundos
};

export default function () {
  const API_URL = __ENV.API_URL || 'http://localhost:8000';

  // Probar Health check
  let resHealth = http.get(`${API_URL}/health`);
  check(resHealth, { 'health check responds with 200': (r) => r.status === 200 });

  // Crear un juego en modo solo
  let payload = JSON.stringify({ nombre_jugador: 'SmokeTester' });
  let params = { headers: { 'Content-Type': 'application/json' } };
  let resSolo = http.post(`${API_URL}/solo/nuevo`, payload, params);
  
  check(resSolo, { 
    'game creation responds with 200': (r) => r.status === 200,
    'receives a session id': (r) => r.json('sesion_id') !== undefined
  });

  sleep(1);
}
