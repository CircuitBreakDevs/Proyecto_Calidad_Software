import http from 'k6/http';
import { check, sleep } from 'k6';

// Spike Test: Simula un golpe masivo y súbito de tráfico, de 0 al máximo en poco tiempo.
// Se usa para avaluar si el sistema aguanta un pico inesperado (ej. se vuelve viral).
export const options = {
    stages: [
        { duration: '10s', target: 100 }, // Pico extremo de 0 a 100 usuarios en 10 seg
        { duration: '30s', target: 100 }, // Sostener el pico intenso
        { duration: '10s', target: 0 },   // Disipar
    ],
};

export default function () {
    const API_URL = __ENV.API_URL || 'http://localhost:8000';

    let res = http.get(`${API_URL}/`);

    check(res, {
        'home page is 200': (r) => r.status === 200
    });

    sleep(0.5); // Sleeps pequeños para saturar la API más rápido
}
