import http from 'k6/http';
import { check, sleep } from 'k6';

// Stress Test: Sube usuarios de manera progresiva hasta un nivel alto
// Sirve para determinar el punto en el que el servidor empieza a fallar o volverse lento.
export const options = {
    stages: [
        { duration: '30s', target: 20 },  // Rampa de subida a 20 usuarios en 30 segundos
        { duration: '1m', target: 20 },   // Mantener 20 usuarios por 1 minuto
        { duration: '30s', target: 50 },  // Rampa hacia 50 usuarios
        { duration: '1m', target: 50 },   // Mantener 50 usuarios
        { duration: '30s', target: 0 },   // Bajar a 0 (recuperación)
    ],
};

export default function () {
    const API_URL = __ENV.API_URL || 'http://localhost:8000';

    const payload = JSON.stringify({ nombre_jugador: 'StressTester' });
    const params = { headers: { 'Content-Type': 'application/json' } };

    let res = http.post(`${API_URL}/solo/nuevo`, payload, params);

    check(res, {
        'game creation is 200': (r) => r.status === 200
    });

    sleep(1);
}
